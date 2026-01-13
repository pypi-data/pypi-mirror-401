import logging
from datetime import datetime
from uuid import UUID

import feedparser
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.auth import Organization
from models.connector import PodcastFeed
from services.transcription import TranscriptionService

logger = logging.getLogger(__name__)


class PodcastService:
    def __init__(self, transcription_service: TranscriptionService):
        self.transcription_service = transcription_service

    async def get_tier_limit(self, tier: str) -> int:
        if tier == "pro":
            return 5
        if tier == "enterprise":
            return 100
        return 1  # Free

    async def add_feed(
        self,
        session: AsyncSession,
        url: str,
        org_id: UUID,
        name: str,
        refresh_interval_minutes: int | None = None,
        max_episodes: int | None = None,
        start_date: datetime | None = None,
        include_keywords: str | None = None,
        exclude_keywords: str | None = None,
    ) -> PodcastFeed:
        # Check tier limits
        org = await session.get(Organization, org_id)
        if not org:
            raise ValueError("Organization not found")

        # Validate Refresh Interval
        if refresh_interval_minutes is not None:
            if org.tier == "free":
                raise ValueError("Free tier does not support custom refresh intervals.")
            if refresh_interval_minutes < 60:
                raise ValueError("Refresh interval must be at least 60 minutes.")

        feeds = await session.exec(select(PodcastFeed).where(PodcastFeed.organization_id == org_id))
        current_count = len(feeds.all())
        limit = await self.get_tier_limit(org.tier)

        if current_count >= limit:
            raise ValueError(f"Feed limit reached for tier '{org.tier}'. Limit: {limit}")

        # Validate Feed
        parsed = feedparser.parse(url)
        if parsed.bozo:
            raise ValueError(f"Invalid RSS feed: {parsed.bozo_exception}")

        # Extract Metadata
        feed_title = parsed.feed.get("title", name)
        feed_description = parsed.feed.get("description", parsed.feed.get("subtitle", ""))
        feed_author = parsed.feed.get("author", parsed.feed.get("itunes_author", ""))
        feed_image = parsed.feed.get("image", {}).get("href", "")
        if not feed_image and "itunes_image" in parsed.feed:
            feed_image = parsed.feed.itunes_image.get("href", "")

        feed = PodcastFeed(
            url=url,
            name=feed_title,
            organization_id=org_id,
            description=feed_description,
            author=feed_author,
            image_url=feed_image,
            refresh_interval_minutes=refresh_interval_minutes,
            max_episodes=max_episodes,
            start_date=start_date,
            include_keywords=include_keywords,
            exclude_keywords=exclude_keywords,
        )
        session.add(feed)
        await session.commit()
        await session.refresh(feed)

        # Trigger Initial Sync (Free sample)
        try:
            await self.sync_feed(session, feed.id, force=True)
        except Exception as e:
            logger.error(f"Failed initial sync for feed {feed.id}: {e}")

        return feed

    async def sync_feed(self, session: AsyncSession, feed_id: UUID, force: bool = False):
        feed = await session.get(PodcastFeed, feed_id)
        if not feed or not feed.is_active:
            return

        # Check Interval
        if not force:
            if not feed.refresh_interval_minutes:
                # Manual sync only
                return

            if feed.last_synced_at:
                delta = datetime.utcnow() - feed.last_synced_at
                if delta.total_seconds() < (feed.refresh_interval_minutes * 60):
                    # Not time yet
                    return

        logger.info(f"Syncing feed: {feed.name} ({feed.url})")
        parsed = feedparser.parse(feed.url)

        from core.entitlements import EntitlementsService
        from models.audio import AudioResource
        from services.queue import QueueService

        queue_service = QueueService()
        entitlements_service = EntitlementsService(session)

        # Safety Limits
        MAX_EPISODES_PER_RUN = 50
        synced_this_run = 0

        # Count existing episodes if limited
        existing_count = 0
        if feed.max_episodes:
            count_stmt = select(AudioResource).where(AudioResource.meta_data["podcast_feed_id"].astext == str(feed.id))
            existing_result = await session.execute(count_stmt)
            existing_count = len(existing_result.all())

        for entry in parsed.entries:
            if feed.max_episodes and existing_count >= feed.max_episodes:
                logger.info(f"Reached max_episodes limit ({feed.max_episodes}) for feed {feed.id}")
                break

            if synced_this_run >= MAX_EPISODES_PER_RUN:
                logger.info(f"Reached safety sync limit ({MAX_EPISODES_PER_RUN}) for feed {feed.id} in this run.")
                break

            # 1. Date Filter
            if feed.start_date:
                # parsed date might need conversion
                published_parsed = entry.get("published_parsed")
                if published_parsed:
                    pub_date = datetime(*published_parsed[:6])
                    if pub_date < feed.start_date:
                        continue

            # 2. Keyword Filter
            title = entry.get("title", "").lower()
            summary = entry.get("summary", "").lower()

            if feed.exclude_keywords:
                excludes = [k.strip().lower() for k in feed.exclude_keywords.split(",")]
                if any(k in title or k in summary for k in excludes):
                    continue

            if feed.include_keywords:
                includes = [k.strip().lower() for k in feed.include_keywords.split(",")]
                if not any(k in title or k in summary for k in includes):
                    continue

            audio_url = None
            for link in entry.links:
                if link.rel == "enclosure" or (link.type and link.type.startswith("audio/")):
                    audio_url = link.href
                    break

            if not audio_url:
                continue

            # Check if episode already exists for this org
            # Use GUID or audio_url
            guid = entry.get("id", audio_url)

            # Check if episode already exists
            existing = await session.execute(select(AudioResource).where(AudioResource.source_url == audio_url))
            if existing.first():
                continue

            # Check Usage Limits before creating the resource or enqueuing
            try:
                # We don't know the duration yet, so we use 0.
                # The entitlements service will apply the capped pending penalty.
                await entitlements_service.check_transcription_limit(feed.organization_id, new_duration_seconds=0)
            except Exception as e:
                logger.warning(f"Limit reached during podcast sync for org {feed.organization_id}: {e}")
                # Stop syncing this feed for now to avoid repeatedly hitting limits
                break

            logger.info(f"Adding new episode: {entry.title}")

            # Create Database Record for the episode
            # We don't have a specific user here, maybe use a "system" user or the one who added the feed?
            # For now, we'll leave user_id as None if it's a platform-level sync, or use the org owner.
            # Let's fetch the first user of the org.
            from models.auth import User

            user_stmt = select(User).where(User.organization_id == feed.organization_id).limit(1)
            user_result = await session.execute(user_stmt)
            user = user_result.scalar_one_or_none()

            audio_resource = AudioResource(
                title=entry.title,
                source_url=audio_url,
                status="pending",
                user_id=user.id if user else None,
                meta_data={
                    "podcast_feed_id": str(feed.id),
                    "guid": guid,
                    "published_at": entry.get("published", ""),
                    "description": entry.get("description", ""),
                },
            )
            session.add(audio_resource)
            await session.commit()
            await session.refresh(audio_resource)

            existing_count += 1

            # Trigger Ingestion
            try:
                queue_service.enqueue_transcription(audio_id=audio_resource.id, audio_url=audio_url, preset="general")
                synced_this_run += 1
            except Exception as e:
                logger.error(f"Failed to enqueue podcast episode {audio_resource.id}: {e}")

        feed.last_synced_at = datetime.utcnow()
        session.add(feed)
        await session.commit()

    async def sync_all_feeds(self, session: AsyncSession):
        logger.info("Running background feed sync...")
        # Join with Organization to check Tiers
        # Use select(PodcastFeed, Organization).join(Organization) ...
        # Actually easier to fetch all active feeds and filter in app or custom query.
        # Let's do a join.

        statement = (
            select(PodcastFeed, Organization)
            .join(Organization)
            .where(PodcastFeed.is_active == True)  # noqa
            .where(Organization.tier != "free")  # Only paid tiers get auto-sync
        )

        results = await session.exec(statement)
        for feed, org in results:
            try:
                await self.sync_feed(session, feed.id)
            except Exception as e:
                logger.error(f"Failed to sync feed {feed.id}: {e}")

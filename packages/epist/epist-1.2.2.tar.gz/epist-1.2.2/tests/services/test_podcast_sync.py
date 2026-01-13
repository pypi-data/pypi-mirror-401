# Tests for Podcast Synchronization Logic
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from models.auth import Organization
from models.connector import PodcastFeed
from services.connector import PodcastService
from services.transcription import TranscriptionService


@pytest.mark.asyncio
async def test_add_feed_refresh_interval_validation(session: AsyncSession):
    # Setup
    mock_transcription = MagicMock(spec=TranscriptionService)
    service = PodcastService(transcription_service=mock_transcription)

    # 1. Free Org should not be able to set refresh_interval_minutes
    free_org = Organization(name="Free Org", tier="free")
    session.add(free_org)
    await session.commit()
    await session.refresh(free_org)

    with patch("services.connector.feedparser.parse") as mock_parse:
        mock_parse.return_value.bozo = False
        with pytest.raises(ValueError) as excinfo:
            await service.add_feed(
                session,
                "http://example.com/rss",
                free_org.id,
                "Free Feed",
                refresh_interval_minutes=60,
            )
    assert "Free tier does not support custom refresh intervals." in str(excinfo.value)

    # 2. Paid Org should not be able to set interval < 60
    pro_org = Organization(name="Pro Org", tier="pro")
    session.add(pro_org)
    await session.commit()
    await session.refresh(pro_org)

    with patch("services.connector.feedparser.parse") as mock_parse:
        mock_parse.return_value.bozo = False
        with pytest.raises(ValueError) as excinfo:
            await service.add_feed(
                session,
                "http://example.com/rss",
                pro_org.id,
                "Pro Feed",
                refresh_interval_minutes=30,
            )
    assert "Refresh interval must be at least 60 minutes." in str(excinfo.value)


@pytest.mark.asyncio
async def test_add_feed_triggers_initial_sync(session: AsyncSession):
    mock_transcription = MagicMock(spec=TranscriptionService)
    service = PodcastService(transcription_service=mock_transcription)

    pro_org = Organization(name="Pro Org", tier="pro")
    session.add(pro_org)
    await session.commit()
    await session.refresh(pro_org)

    # Use patch to verify sync_feed is called
    with patch("services.connector.feedparser.parse") as mock_parse:
        mock_result = MagicMock()
        mock_result.bozo = False
        mock_result.feed = {"title": "Pro Feed", "description": "desc", "author": "auth", "image": {}}
        mock_parse.return_value = mock_result

        with patch.object(PodcastService, "sync_feed") as mock_sync:
            await service.add_feed(
                session,
                "http://example.com/rss",
                pro_org.id,
                "Pro Feed",
                refresh_interval_minutes=60,
            )
            mock_sync.assert_called_once()


@pytest.mark.asyncio
async def test_sync_all_feeds_filtering(session: AsyncSession):
    mock_transcription = MagicMock(spec=TranscriptionService)
    service = PodcastService(transcription_service=mock_transcription)

    # 1. Create Free Org with a feed
    free_org = Organization(name="Free Org", tier="free")
    session.add(free_org)

    # 2. Create Pro Org with 2 feeds: one due for sync, one not
    pro_org = Organization(name="Pro Org", tier="pro")
    session.add(pro_org)
    await session.commit()
    await session.refresh(free_org)
    await session.refresh(pro_org)

    # Feed 1: Free (sync_all_feeds should ignore)
    feed_free = PodcastFeed(name="Free Feed", url="http://free.com", organization_id=free_org.id, is_active=True)

    # Feed 2: Pro, due (last synced 2 hours ago, interval 60m)
    last_synced_due = datetime.utcnow() - timedelta(hours=2)
    feed_pro_due = PodcastFeed(
        name="Pro Due",
        url="http://pro-due.com",
        organization_id=pro_org.id,
        is_active=True,
        refresh_interval_minutes=60,
        last_synced_at=last_synced_due,
    )

    # Feed 3: Pro, NOT due (last synced 30 mins ago, interval 60m)
    last_synced_not_due = datetime.utcnow() - timedelta(minutes=30)
    feed_pro_not_due = PodcastFeed(
        name="Pro Not Due",
        url="http://pro-not-due.com",
        organization_id=pro_org.id,
        is_active=True,
        refresh_interval_minutes=60,
        last_synced_at=last_synced_not_due,
    )

    session.add(feed_free)
    session.add(feed_pro_due)
    session.add(feed_pro_not_due)
    await session.commit()

    # Sync all feeds
    # We need to patch QueueService to avoid missing credentials error
    with (
        patch("services.connector.feedparser.parse") as mock_parse,
        patch("services.queue.QueueService") as mock_queue_service,
    ):
        # Configure the mock to behave like a real feedparser result
        mock_feed_data = MagicMock()
        mock_feed_data.get.return_value = "Mock Title"
        # We need to ensure 'title', 'description', etc are strings

        mock_parsed_result = MagicMock()
        mock_parsed_result.bozo = False
        mock_parsed_result.feed = {
            "title": "Mock Feed Title",
            "description": "Mock Description",
            "author": "Mock Author",
            "image": {"href": "http://image.url"},
        }
        mock_parsed_result.entries = []
        mock_parse.return_value = mock_parsed_result

        await service.sync_all_feeds(session)

    # 3. Verify
    await session.refresh(feed_free)
    await session.refresh(feed_pro_due)
    await session.refresh(feed_pro_not_due)

    # Free feed should NOT have been synced (it's naive now, but let's check)
    assert feed_free.last_synced_at is None

    # Pro Due feed SHOULD have been synced (updated last_synced_at)
    # Check that it was updated to roughly "now"
    assert feed_pro_due.last_synced_at > (datetime.utcnow() - timedelta(minutes=5))
    assert feed_pro_due.last_synced_at != last_synced_due

    # Pro Not Due feed SHOULD NOT have been synced (last_synced_at remains same)
    # Note: Use a small tolerance or just compare exact if not modified
    assert feed_pro_not_due.last_synced_at == last_synced_not_due

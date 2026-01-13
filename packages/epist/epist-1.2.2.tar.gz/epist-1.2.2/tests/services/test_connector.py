# Tests for Connector Service
from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.auth import Organization
from models.connector import PodcastFeed
from services.connector import PodcastService
from services.transcription import TranscriptionService


@patch("services.queue.QueueService")
@pytest.mark.asyncio
async def test_add_feed_free_tier_limit(mock_queue, session: AsyncSession):
    # 1. Setup Connector Service with mock transcription
    mock_transcription = MagicMock(spec=TranscriptionService)
    service = PodcastService(transcription_service=mock_transcription)

    # 2. Create Org (Free Tier by default)
    org = Organization(name="Free Org", tier="free")
    session.add(org)
    await session.commit()
    await session.refresh(org)

    # 3. Add 1st Feed (Should Succeed)
    with patch("services.connector.feedparser.parse") as mock_parse:
        mock_result = MagicMock()
        mock_result.bozo = False
        mock_result.feed = {"title": "Feed 1", "description": "desc", "author": "auth", "image": {}}
        mock_parse.return_value = mock_result

        feed1 = await service.add_feed(session, "http://example.com/rss1", org.id, "Feed 1")
    assert feed1.id is not None

    # 4. Add 2nd Feed (Should Fail - Limit 1)
    with patch("services.connector.feedparser.parse") as mock_parse:
        mock_parse.return_value.bozo = False
        with pytest.raises(ValueError) as excinfo:
            await service.add_feed(session, "http://example.com/rss2", org.id, "Feed 2")
    assert "Feed limit reached" in str(excinfo.value)


@patch("services.queue.QueueService")
@pytest.mark.asyncio
async def test_add_feed_pro_tier_limit(mock_queue, session: AsyncSession):
    # 1. Setup
    mock_transcription = MagicMock(spec=TranscriptionService)
    service = PodcastService(transcription_service=mock_transcription)

    # 2. Create Org (Pro Tier)
    org = Organization(name="Pro Org", tier="pro")
    session.add(org)
    await session.commit()
    await session.refresh(org)

    # 3. Add 2 Feeds (Should Succeed)
    with patch("services.connector.feedparser.parse") as mock_parse:
        mock_result = MagicMock()
        mock_result.bozo = False
        mock_result.feed = {"title": "Feed X", "description": "desc", "author": "auth", "image": {}}
        mock_parse.return_value = mock_result

        await service.add_feed(session, "http://example.com/rss1", org.id, "Feed 1")
        await service.add_feed(session, "http://example.com/rss2", org.id, "Feed 2")

    feeds = await session.exec(select(PodcastFeed).where(PodcastFeed.organization_id == org.id))
    assert len(feeds.all()) == 2


@patch("services.queue.QueueService")
@pytest.mark.asyncio
async def test_sync_feed_logic(mock_queue, session: AsyncSession):
    # 1. Setup
    mock_transcription = MagicMock(spec=TranscriptionService)
    service = PodcastService(transcription_service=mock_transcription)

    org = Organization(name="Test Org", tier="free")
    session.add(org)
    await session.commit()
    await session.refresh(org)

    with patch("services.connector.feedparser.parse") as mock_parse_add:
        mock_result = MagicMock()
        mock_result.bozo = False
        mock_result.feed = {"title": "My Feed", "description": "desc", "author": "auth", "image": {}}
        mock_parse_add.return_value = mock_result

        feed = await service.add_feed(session, "http://example.com/rss", org.id, "My Feed")

    # 2. Mock Feedparser
    mock_rss = MagicMock()
    mock_rss.bozo = False

    # Return real strings for feed metadata
    mock_rss.feed = {
        "title": "Mock Feed Title",
        "description": "Mock Desc",
        "author": "Mock Author",
        "image": {"href": "http://img.url"},
    }

    mock_entry = MagicMock()
    mock_entry.title = "Episode 1"
    mock_entry.get.side_effect = lambda k, d=None: "guid_1" if k == "id" else d
    mock_entry.links = [MagicMock(type="audio/mpeg", href="http://audio.mp3", rel="enclosure")]
    mock_rss.entries = [mock_entry]

    with patch("services.connector.feedparser.parse", return_value=mock_rss):
        await service.sync_feed(session, feed.id)

    # 3. Verify
    await session.refresh(feed)
    assert feed.last_synced_at is not None
    # Verify we found the audio (logic currently just logs it, but verify no crash)

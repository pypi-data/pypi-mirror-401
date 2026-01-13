from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from models.auth import User
from models.connector import PodcastFeed
from services.connector import PodcastService
from services.transcription import TranscriptionService


@pytest.mark.asyncio
async def test_sync_feed_limits():
    # Mock Session
    session = MagicMock(spec=AsyncSession)

    # Setup Service with Mock Transcription
    mock_transcription = MagicMock(spec=TranscriptionService)
    service = PodcastService(transcription_service=mock_transcription)

    # Mock Data
    org_id = uuid4()
    feed_id = uuid4()

    feed = PodcastFeed(
        id=feed_id,
        name="Limit Feed",
        url="http://limit-feed.com",
        organization_id=org_id,
        is_active=True,
        max_episodes=None,  # Unlimited initially for this test
    )

    # Prepare Mock Feed Parser with 60 entries
    class MockEntry(dict):
        def __getattr__(self, name):
            if name in self:
                return self[name]
            return super().__getattribute__(name)

    entries = []
    for i in range(60):
        entry = MockEntry(
            {
                "title": f"Episode {i}",
                "summary": "Summary",
                "published": "Tue, 07 Jan 2025 00:00:00 GMT",
                "links": [MockEntry({"rel": "enclosure", "href": f"http://audio.com/{i}.mp3"})],
                "id": f"guid-{i}",
            }
        )
        entries.append(entry)

    mock_parsed = MagicMock()
    mock_parsed.entries = entries
    mock_parsed.bozo = False

    # Mock session.get to return feed
    session.get.return_value = feed

    # Mock session.execute for existing episode check
    # It returns a result which has .first()
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = None  # No existing episodes
    mock_exec_result.all.return_value = []  # No existing audio resources count

    # Handle Async Mocking for session.execute
    async def async_execute(*args, **kwargs):
        return mock_exec_result

    session.execute = MagicMock(side_effect=async_execute)

    # Mock User Fetch for AudioResource creation
    # It calls session.execute to get user
    user_mock_result = MagicMock()
    user_mock_result.scalar_one_or_none.return_value = User(id=uuid4(), email="test@test.com", full_name="Test User")

    # We need to distinguish calls to session.execute
    # 1. Existing check: select(AudioResource)...
    # 2. User fetch: select(User)...
    # 3. Count check: select(AudioResource)...

    # Let's verify the mocks inside the patches

    with (
        patch("services.connector.feedparser.parse", return_value=mock_parsed),
        patch("services.queue.QueueService") as MockQueue,
        patch("core.entitlements.EntitlementsService") as MockEntitlements,
    ):
        mock_queue = MockQueue.return_value
        mock_entitlements = MockEntitlements.return_value
        # Ensure async methods are AsyncMock
        mock_entitlements.check_transcription_limit = AsyncMock()

        # Scenario 1: Sync with success (Safety Limit Check)
        await service.sync_feed(session, feed.id, force=True)

        # Verify 50 queued tasks (MAX_EPISODES_PER_RUN)
        assert mock_queue.enqueue_transcription.call_count == 50

        # Verify usage check called 50 times
        assert mock_entitlements.check_transcription_limit.call_count == 50

    # Scenario 2: Sync stops when Entitlement fails
    mock_queue.reset_mock()
    mock_entitlements.reset_mock()
    mock_entitlements.check_transcription_limit = AsyncMock()

    # Make entitlements raise error on 5th call
    # side_effect with AsyncMock can be a list of exceptions or return values
    # But for AsyncMock, we need to pass an iterable to side_effect that yields awaitables or exceptions

    # Easier way: define a side_effect function
    call_count = 0

    async def check_limit_side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 5:
            raise Exception("Limit Exceeded")

    mock_entitlements.check_transcription_limit.side_effect = check_limit_side_effect

    with (
        patch("services.connector.feedparser.parse", return_value=mock_parsed),
        patch("services.queue.QueueService", return_value=mock_queue),
        patch("core.entitlements.EntitlementsService", return_value=mock_entitlements),
    ):
        await service.sync_feed(session, feed.id, force=True)

        # Should have queued 4 episodes
        assert mock_queue.enqueue_transcription.call_count == 4
        # Should have called check 5 times
        assert call_count == 5

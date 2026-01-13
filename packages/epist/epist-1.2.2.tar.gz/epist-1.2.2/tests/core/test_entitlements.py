from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from core.entitlements import EntitlementsService


@pytest.mark.asyncio
async def test_check_transcription_limit_cap_penalty():
    # Mock Session
    session = MagicMock(spec=AsyncSession)

    # Mock UsageService to capture checks
    with patch("services.usage_service.UsageService") as MockUsageService:
        mock_usage_service = MockUsageService.return_value
        # Mock the instance methods
        mock_usage_service.check_usage = AsyncMock()

        # Setup Service
        service = EntitlementsService(session)

        # Test Data
        org_id = uuid4()

        # Mock DB Execution for Pending Count
        # The service calls: await self.db.exec(pending_query)
        # It expects a result object that has .one()
        mock_result = MagicMock()
        mock_result.one.return_value = 10  # 10 pending files

        # Async mock for exec
        async def async_exec(*args, **kwargs):
            return mock_result

        session.exec = MagicMock(side_effect=async_exec)

        # Execute Check
        # 10 pending files * 600s = 6000s.
        # Cap is 3600s.
        # Request adds 100s.
        # Expected projected_total = 3600 + 100 = 3700.

        await service.check_transcription_limit(org_id, new_duration_seconds=100)

        # Verify UsageService.check_usage was called with correct projected_seconds
        mock_usage_service.check_usage.assert_called_once()
        args, kwargs = mock_usage_service.check_usage.call_args

        # UsageService.check_usage(org_id, projected_seconds=...)
        # Logic in entitlements: projected_total = int(pending_seconds + new_duration_seconds)
        # pending_seconds should be min(6000, 3600) = 3600
        # projected_total = 3600 + 100 = 3700

        assert kwargs["projected_seconds"] == 3700

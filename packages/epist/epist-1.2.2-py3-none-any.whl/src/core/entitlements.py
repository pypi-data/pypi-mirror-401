from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.audio import AudioResource
from models.auth import User

if TYPE_CHECKING:
    from models.auth import Organization


class EntitlementsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def check_access(self, org: "Organization", feature: str) -> bool:
        """
        Check if an organization has access to a specific feature based on its tier.
        """
        from models.entitlements import TIER_ENTITLEMENTS, Tier

        try:
            tier = Tier(org.tier)
            entitlements = TIER_ENTITLEMENTS.get(tier)
            if not entitlements:
                return False

            return feature in entitlements.get("features", [])
        except (ValueError, AttributeError):
            # Fallback if tier is invalid or org is None
            return False

    async def check_transcription_limit(self, org_id: UUID, new_duration_seconds: float = 0):
        from services.usage_service import UsageService

        usage_service = UsageService(self.db)

        # Race Condition Fix: Include pending/processing files
        # Files currently uploading/processing have duration=None or 0, but consume quota.
        # We assume a strict buffer (e.g. 10 mins) for each active file to prevent parallel abuse.
        pending_query = (
            select(func.count(AudioResource.id))
            .join(User, AudioResource.user_id == User.id)
            .where(User.organization_id == org_id)
            .where(AudioResource.status.in_(["pending", "processing"]))
        )
        pending_result = await self.db.exec(pending_query)
        pending_count = pending_result.one() or 0

        # Add 10 minutes (600s) per pending file
        # CAP: We cap the total pending penalty to 3600s (1 hour) to avoid blocking bulk ingestions immediately.
        pending_seconds = min(pending_count * 600, 3600)

        # Check Usage (Current + Pending + New Request)
        projected_total = int(pending_seconds + new_duration_seconds)

        # Delegate to UsageService which checks against Organization.monthly_audio_seconds
        # This keeps the logic centralized and efficient
        await usage_service.check_usage(org_id, projected_seconds=projected_total)

import logging
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.tier_limits import TIER_AUDIO_LIMITS, Tier
from models.auth import Organization

logger = logging.getLogger(__name__)


class UsageService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_usage(self, org_id: str, projected_seconds: int = 0) -> None:
        """
        Check if the organization has enough quota for the projected usage.
        Raises HTTPException if limit exceeded.
        """
        stmt = select(Organization).where(Organization.id == org_id)
        result = await self.db.exec(stmt)
        org = result.scalars().first()

        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Determine Limit (Robust access for tests + Centralized config)
        tier = getattr(org, "tier", Tier.FREE)
        limit = TIER_AUDIO_LIMITS.get(tier, TIER_AUDIO_LIMITS[Tier.FREE])

        # Current Usage
        current_usage = getattr(org, "monthly_audio_seconds", 0)

        if current_usage + projected_seconds > limit:
            logger.warning(
                f"Limit exceeded for org {org.id}. Usage: {current_usage}, Request: {projected_seconds}, Limit: {limit}"
            )
            raise HTTPException(
                status_code=403,
                detail=f"Usage limit exceeded for {tier} tier. Used: {current_usage / 3600:.1f}h / Limit: {limit / 3600:.1f}h. Please upgrade.",
            )

    async def increment_usage(self, org_id: str, seconds: int) -> None:
        """
        Increment the usage for an organization.
        """
        stmt = select(Organization).where(Organization.id == org_id)
        result = await self.db.exec(stmt)
        org = result.scalars().first()

        if org:
            current = getattr(org, "monthly_audio_seconds", 0)
            org.monthly_audio_seconds = current + seconds
            self.db.add(org)
            # We don't commit here usually if part of larger transaction,
            # but for usage tracking we might want to ensure it sticks.
            # Assuming caller handles commit or we do flush.
            # For safety in this service, let's flush/add to session.
            # The API endpoint usually commits.

    async def reset_usage(self, org_id: str) -> None:
        """
        Reset usage for billing cycle.
        """
        stmt = select(Organization).where(Organization.id == org_id)
        result = await self.db.exec(stmt)
        org = result.scalars().first()

        if org:
            org.monthly_audio_seconds = 0
            org.usage_reset_at = datetime.utcnow()
            self.db.add(org)
            await self.db.commit()
            logger.info(f"Usage reset for org {org.id}")

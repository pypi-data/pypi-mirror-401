from sqlalchemy.ext.asyncio import AsyncSession

from models.auth import Organization
from models.entitlements import TIER_ENTITLEMENTS, Tier


class EntitlementService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def get_tier(self, org: Organization) -> Tier:
        try:
            return Tier(org.tier)
        except ValueError:
            return Tier.FREE

    def check_access(self, org: Organization, feature: str) -> bool:
        tier = self.get_tier(org)
        entitlements = TIER_ENTITLEMENTS.get(tier, TIER_ENTITLEMENTS[Tier.FREE])
        return feature in entitlements["features"]

    def get_limits(self, org: Organization) -> dict:
        tier = self.get_tier(org)
        return TIER_ENTITLEMENTS.get(tier, TIER_ENTITLEMENTS[Tier.FREE])

    async def check_team_limit(self, org_id: str) -> bool:
        # To be implemented if we enforce strict checking before invite
        # Currently logic is handled in the organization endpoint.
        return True

    # Placeholder for usage tracking (Redis or SQL)
    async def get_usage(self, org_id: str) -> dict:
        # returns { "transcription_minutes": 12, "search_requests": 50 }
        # This requires tracking tables not yet created. For MVP, we return mocks or setup basic tracking later.
        return {"transcription_minutes": 0, "search_requests": 0}

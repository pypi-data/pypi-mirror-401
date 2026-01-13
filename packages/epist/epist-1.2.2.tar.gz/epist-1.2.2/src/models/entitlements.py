from enum import Enum
from typing import TypedDict


class Tier(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class Entitlement(TypedDict):
    transcription_minutes_limit: int
    search_requests_limit: int
    max_team_members: int
    features: list[str]


TIER_ENTITLEMENTS: dict[Tier, Entitlement] = {
    Tier.FREE: {
        "transcription_minutes_limit": 60,
        "search_requests_limit": 100,
        "max_team_members": 1,
        "features": ["basic_support", "standard_processing"],
    },
    Tier.PRO: {
        "transcription_minutes_limit": 600,
        "search_requests_limit": 10000,
        "max_team_members": 5,
        "features": ["priority_support", "advanced_chunking", "priority_queue", "api_access", "rss_ingestion"],
    },
    Tier.ENTERPRISE: {
        "transcription_minutes_limit": 999999,
        "search_requests_limit": 999999,
        "max_team_members": 999,
        "features": ["dedicated_support", "sso", "audit_logs", "slas", "rss_ingestion"],
    },
}

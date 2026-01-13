from enum import Enum


class Tier(str, Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"


# Limits in Seconds
TIER_AUDIO_LIMITS = {
    Tier.FREE: 5 * 3600,
    Tier.STARTER: 20 * 3600,
    Tier.PRO: 100 * 3600,
}

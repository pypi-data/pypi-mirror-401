from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user
from db.session import get_session
from models.auth import User
from services.stripe_service import StripeService

router = APIRouter()


@router.post("/checkout")
async def create_checkout_session(
    plan_id: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Create a Stripe Checkout Session to upgrade subscription.
    """
    stripe_service = StripeService(db)
    url = await stripe_service.create_checkout_session(str(current_user.organization_id), plan_id=plan_id)
    return {"url": url}


@router.post("/portal")
async def create_portal_session(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Create a Stripe Customer Portal session to manage subscription.
    """
    stripe_service = StripeService(db)
    url = await stripe_service.create_portal_session(str(current_user.organization_id))
    return {"url": url}


@router.get("/debug")
async def debug_stripe_config():
    """
    Temporary debug endpoint to verify Stripe configuration in Cloud Run.
    """
    import stripe

    from core.config import settings

    masked_key = settings.STRIPE_SECRET_KEY[:8] + "..." if settings.STRIPE_SECRET_KEY else "None"

    try:
        # Test Stripe Connection
        price = stripe.Price.retrieve(settings.STRIPE_PRICE_ID_PRO)
        stripe_status = "SUCCESS"
        price_info = f"{price.id} ({price.unit_amount} {price.currency})"
    except Exception as e:
        stripe_status = f"FAILED: {e!s}"
        price_info = "N/A"

    return {
        "environment": settings.ENVIRONMENT,
        "frontend_url": settings.FRONTEND_URL,
        "backend_cors_origins": settings.BACKEND_CORS_ORIGINS,
        "stripe_key_masked": masked_key,
        "stripe_price_id": settings.STRIPE_PRICE_ID_PRO,
        "stripe_connection": stripe_status,
        "price_info": price_info,
    }

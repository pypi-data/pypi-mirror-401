import hashlib
import secrets
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user
from core.limiter import limiter
from db.session import get_session
from models.auth import ApiKey, Organization, User


class OnboardingRequest(BaseModel):
    organization_name: str


router = APIRouter()


# TODO: Move to a shared utility or config
def generate_api_key() -> str:
    return f"sk_live_{secrets.token_urlsafe(32)}"


@router.post("/api-keys", response_model=dict, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_api_key(
    request: Request,
    name: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new API key for the authenticated user.
    """
    # Generate a secure random key
    raw_key = f"sk_live_{uuid.uuid4().hex}"
    # Use SHA256 to store the key hash, matching get_api_key logic
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    prefix = raw_key[:12]

    api_key = ApiKey(
        key_hash=key_hash,
        prefix=prefix,
        name=name,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
    )

    session.add(api_key)
    await session.commit()
    await session.refresh(api_key)

    print(
        f"DEBUG: create_api_key - Created key {api_key.id} for user {current_user.id} (Org: {current_user.organization_id})"
    )

    return {
        "id": api_key.id,
        "name": api_key.name,
        "key": raw_key,  # Only shown once
        "created_at": api_key.created_at,
    }


@router.post("/onboarding")
async def complete_onboarding(
    data: OnboardingRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Complete the onboarding process for the current user.
    """
    org_name = data.organization_name
    if not org_name:
        raise HTTPException(status_code=400, detail="Organization name is required")

    # Update organization name
    await session.refresh(current_user, ["organization"])
    if current_user.organization:
        current_user.organization.name = org_name
        session.add(current_user.organization)
    else:
        # Fallback in case organization is somehow missing
        org = Organization(name=org_name)
        session.add(org)
        await session.commit()
        await session.refresh(org)
        current_user.organization_id = org.id

    # Mark onboarding as complete
    current_user.onboarding_completed = True
    session.add(current_user)

    await session.commit()
    await session.refresh(current_user)

    return {"status": "success"}


@router.get("/me", response_model=dict)
async def get_me(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get current user details including organization info.
    """
    # Organization should be loaded because User lazy loads it?
    # Actually, let's explicit join if needed, or rely on lazy loading which works in async if session is open.
    # But better to load it explicitly or access it to trigger load.
    await session.refresh(current_user, ["organization"])

    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "firebase_uid": current_user.firebase_uid,
        "onboarding_completed": current_user.onboarding_completed,
        "organization": {
            "id": current_user.organization.id,
            "name": current_user.organization.name,
            "tier": current_user.organization.tier,
            "subscription_status": current_user.organization.subscription_status,
            # Add other fields if needed
        }
        if current_user.organization
        else None,
    }


@router.get("/api-keys", response_model=list[dict])
async def list_api_keys(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    List all active API keys for the authenticated user.
    """
    statement = select(ApiKey).where(ApiKey.user_id == current_user.id, ApiKey.is_active)
    results = await session.exec(statement)
    keys = results.all()

    print(f"DEBUG: list_api_keys - User {current_user.id} (Org: {current_user.organization_id}) has {len(keys)} keys.")
    for k in keys:
        print(f"DEBUG: Key ID: {k.id}, Active: {k.is_active}, Created: {k.created_at}, UserID: {k.user_id}")

    return [
        {"id": k.id, "name": k.name, "prefix": k.prefix, "created_at": k.created_at, "last_used_at": k.last_used_at}
        for k in keys
    ]


@router.delete("/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    key_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Revoke an API key.
    """
    statement = select(ApiKey).where(ApiKey.id == key_id, ApiKey.user_id == current_user.id)
    result = await session.exec(statement)
    api_key = result.first()

    if not api_key:
        raise HTTPException(status_code=404, detail="API Key not found")

    api_key.is_active = False
    session.add(api_key)
    await session.commit()


@router.put("/api-keys/{key_id}", response_model=dict)
async def rename_api_key(
    key_id: uuid.UUID,
    name: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Rename an API key.
    """
    statement = select(ApiKey).where(ApiKey.id == key_id, ApiKey.user_id == current_user.id)
    result = await session.exec(statement)
    api_key = result.first()

    if not api_key:
        raise HTTPException(status_code=404, detail="API Key not found")

    api_key.name = name
    session.add(api_key)
    await session.commit()
    await session.refresh(api_key)

    return {"id": api_key.id, "name": api_key.name, "prefix": api_key.prefix, "created_at": api_key.created_at}

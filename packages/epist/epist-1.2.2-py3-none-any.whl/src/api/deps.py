from __future__ import annotations

import hashlib
import logging
import uuid
from datetime import datetime
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader, HTTPBearer
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.auth import verify_firebase_token
from core.config import settings
from db.session import get_session
from models.auth import ApiKey, Organization, User

security = HTTPBearer()
api_key_header_scheme = APIKeyHeader(name="x-api-key", auto_error=False)

logger = logging.getLogger(__name__)


async def get_current_user(
    request: Request,
    authorization: str | None = Header(None),
    x_api_key: str | None = Security(api_key_header_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    """
    Validates Firebase ID token OR API Key and returns the current user.
    """
    # 1. Check for Bearer Token (Firebase)
    decoded_token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        try:
            decoded_token = verify_firebase_token(token)
        except Exception:
            # If token is invalid, we don't immediately fail.
            # This allows falling back to API key if present.
            print("DEBUG: get_current_user - Invalid Bearer token, falling back to API Key if available.")

    if decoded_token:
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name", "Unknown User")
        picture = decoded_token.get("picture")

        if not email:
            raise HTTPException(status_code=400, detail="Email required in token")

        # Check/Create User (JIT)
        user = (await session.exec(select(User).where(User.firebase_uid == uid))).first()

        if not user:
            user = (await session.exec(select(User).where(User.email == email))).first()
            try:
                if user:
                    user.firebase_uid = uid
                    user.avatar_url = picture
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
                else:
                    # Bootstrap Org
                    org = (
                        await session.exec(select(Organization).where(Organization.name == "Default Organization"))
                    ).first()
                    if not org:
                        org = Organization(name=f"{name}'s Organization")
                        session.add(org)
                        await session.commit()
                        await session.refresh(org)

                    user = User(
                        email=email, full_name=name, firebase_uid=uid, avatar_url=picture, organization_id=org.id
                    )
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
            except Exception as e:
                # Handle race condition for concurrent login/requests
                from sqlalchemy.exc import IntegrityError

                if not isinstance(e, IntegrityError):
                    raise e

                await session.rollback()
                logger.warning(f"IntegrityError (likely concurrent user creation) during JIT sync for {email}: {e}")
                # Try fetching one last time
                user = (await session.exec(select(User).where(User.email == email))).first()
                if not user:
                    raise e

        print(
            f"DEBUG: get_current_user (Firebase) - Resolved User: {user.id}, Email: {user.email}, FirebaseUID: {user.firebase_uid}"
        )
        request.state.user = user
        request.state.user_id = user.id
        request.state.auth_method = "session"
        return user

    # 2. Check for API Key
    if x_api_key:
        # Check Dev Key
        if x_api_key == settings.API_KEY:
            # Return a "Dev User" or the first admin user
            # For now, let's try to find a superuser or create a dummy dev user
            # Ideally, dev key should map to a specific system user.
            # Let's find the first user in DB to act as Dev
            user = (await session.exec(select(User))).first()
            if not user:
                # Bootstrap Dev Environment if completely empty
                logger.info("Dev Key used but no users found. Bootstrapping Dev Environment.")
                try:
                    # 1. Ensure Default Org
                    org = (
                        await session.exec(select(Organization).where(Organization.name == "Default Organization"))
                    ).first()
                    if not org:
                        org = Organization(name="Default Organization")
                        session.add(org)
                        await session.commit()
                        await session.refresh(org)

                    # 2. Create Dev User
                    user = User(
                        email="dev@epist.ai",
                        full_name="Dev User",
                        firebase_uid="dev-master-key",
                        avatar_url=None,
                        organization_id=org.id,
                        is_active=True,
                    )
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
                    logger.info(f"Bootstrapped Dev User: {user.email} ({user.id})")
                except Exception as e:
                    logger.error(f"Failed to bootstrap Dev User: {e}")
                    raise HTTPException(status_code=500, detail="Failed to bootstrap dev environment")

            if user:
                request.state.user = user
                request.state.user_id = user.id
                request.state.auth_method = "api_key"
                return user
            else:
                raise HTTPException(status_code=401, detail="No users found for Dev Key access")

        # Check DB Key
        key_hash = hashlib.sha256(x_api_key.encode()).hexdigest()
        api_key_obj = (await session.exec(select(ApiKey).where(ApiKey.key_hash == key_hash, ApiKey.is_active))).first()

        if api_key_obj:
            # Update usage
            api_key_obj.last_used_at = datetime.utcnow()
            session.add(api_key_obj)
            await session.commit()

            # Return associated user
            # We need to load the user since it's a relationship, but we have user_id
            user = (await session.exec(select(User).where(User.id == api_key_obj.user_id))).first()
            if user:
                request.state.user = user
                request.state.user_id = user.id
                request.state.auth_method = "api_key"
                return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_api_key(
    x_api_key: Annotated[str | None, Header()] = None,
    session: AsyncSession = Depends(get_session),
):
    """
    Validate X-API-Key header against DB or Dev Key.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )

    # 1. Check Dev Key
    if x_api_key == settings.API_KEY:
        return x_api_key

    # 2. Check DB
    key_hash = hashlib.sha256(x_api_key.encode()).hexdigest()
    api_key_obj = (await session.exec(select(ApiKey).where(ApiKey.key_hash == key_hash, ApiKey.is_active))).first()

    if api_key_obj:
        # Update last_used_at
        # Note: In high-throughput, move this to background task
        api_key_obj.last_used_at = datetime.utcnow()
        session.add(api_key_obj)
        await session.commit()
        return x_api_key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )


async def get_current_user_org_id(
    current_user: User = Depends(get_current_user),
) -> uuid.UUID:
    return current_user.organization_id


async def get_current_user_optional(
    request: Request,
    authorization: str | None = Header(None),
    x_api_key: str | None = Security(api_key_header_scheme),
    session: AsyncSession = Depends(get_session),
) -> User | None:
    """
    Optional version of get_current_user. Does not raise 401 if auth is missing.
    """
    try:
        if authorization or x_api_key:
            return await get_current_user(request, authorization, x_api_key, session)
        return None
    except HTTPException:
        return None


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verifies that the current user is a superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges",
        )
    return current_user

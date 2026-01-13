import uuid
from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api import deps
from db.session import get_session
from models.audio import AudioResource
from models.auth import Organization, User
from models.log import RequestLog

router = APIRouter()


@router.get("/stats", response_model=dict[str, Any])
async def get_admin_stats(
    session: AsyncSession = Depends(get_session),
    current_superuser: User = Depends(deps.get_current_superuser),
):
    """
    Get high-level system statistics.
    """
    user_count = (await session.exec(select(func.count(User.id)))).one()
    org_count = (await session.exec(select(func.count(Organization.id)))).one()
    audio_count = (await session.exec(select(func.count(AudioResource.id)))).one()

    # Active users in last 24h
    yesterday = datetime.utcnow() - timedelta(days=1)
    active_users_24h = (
        await session.exec(
            select(func.count(func.distinct(RequestLog.user_id))).where(RequestLog.created_at >= yesterday)
        )
    ).one()

    return {
        "users": user_count,
        "organizations": org_count,
        "audio_resources": audio_count,
        "active_users_24h": active_users_24h,
    }


@router.get("/usage", response_model=list[dict[str, Any]])
async def get_usage_metrics(
    days: int = Query(7, ge=1, le=30),
    session: AsyncSession = Depends(get_session),
    current_superuser: User = Depends(deps.get_current_superuser),
):
    """
    Get daily usage metrics for the last N days.
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    # Simple aggregation of requests per day
    # Note: For production-scale, this should use a proper analytics DB or pre-aggregated table
    query = (
        select(
            func.date_trunc("day", RequestLog.created_at).label("day"),
            func.count(RequestLog.id).label("count"),
            func.avg(RequestLog.latency_ms).label("avg_latency"),
        )
        .where(RequestLog.created_at >= start_date)
        .group_by("day")
        .order_by("day")
    )

    results = await session.exec(query)
    return [
        {
            "date": day.isoformat(),
            "requests": count,
            "avg_latency_ms": round(avg_latency, 2) if avg_latency else 0,
        }
        for day, count, avg_latency in results.all()
    ]


@router.get("/organizations", response_model=list[dict[str, Any]])
async def list_organizations(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
    current_superuser: User = Depends(deps.get_current_superuser),
):
    """
    List all organizations with their plans and user counts.
    """
    query = (
        select(Organization, func.count(User.id).label("user_count"))
        .outerjoin(User)
        .group_by(Organization.id)
        .order_by(Organization.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    results = await session.exec(query)
    return [
        {
            "id": org.id,
            "name": org.name,
            "tier": org.tier,
            "user_count": user_count,
            "subscription_status": org.subscription_status,
            "created_at": org.created_at.isoformat(),
        }
        for org, user_count in results.all()
    ]


@router.get("/users", response_model=list[dict[str, Any]])
async def list_users(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
    current_superuser: User = Depends(deps.get_current_superuser),
):
    """
    List all users with their superuser status and activity.
    """
    query = select(User).order_by(User.created_at.desc()).offset(offset).limit(limit)
    results = await session.exec(query)

    return [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat(),
            "organization_id": user.organization_id,
        }
        for user in results.all()
    ]


@router.get("/logs", response_model=list[dict[str, Any]])
async def get_recent_logs(
    limit: int = Query(50, ge=1, le=100),
    status_code: int | None = None,
    session: AsyncSession = Depends(get_session),
    current_superuser: User = Depends(deps.get_current_superuser),
):
    """
    Get recent request logs for debugging.
    """
    query = select(RequestLog).order_by(RequestLog.created_at.desc())
    if status_code:
        query = query.where(RequestLog.status_code == status_code)

    query = query.limit(limit)
    results = await session.exec(query)

    return [
        {
            "id": log.id,
            "method": log.method,
            "path": log.path,
            "status_code": log.status_code,
            "latency_ms": log.latency_ms,
            "created_at": log.created_at.isoformat(),
            "user_id": log.user_id,
        }
        for log in results.all()
    ]


@router.patch("/users/{user_id}", response_model=dict[str, Any])
async def update_user(
    user_id: uuid.UUID,
    is_superuser: bool | None = None,
    is_active: bool | None = None,
    session: AsyncSession = Depends(get_session),
    current_superuser: User = Depends(deps.get_current_superuser),
):
    """
    Update a user's status or role.
    """
    user = await session.get(User, user_id)
    if not user:
        return {"error": "User not found"}

    if is_superuser is not None:
        user.is_superuser = is_superuser
    if is_active is not None:
        user.is_active = is_active

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "is_superuser": user.is_superuser,
        "is_active": user.is_active,
    }


@router.patch("/organizations/{org_id}", response_model=dict[str, Any])
async def update_organization(
    org_id: uuid.UUID,
    tier: str | None = None,
    subscription_status: str | None = None,
    session: AsyncSession = Depends(get_session),
    current_superuser: User = Depends(deps.get_current_superuser),
):
    """
    Update an organization's tier or status.
    """
    org = await session.get(Organization, org_id)
    if not org:
        return {"error": "Organization not found"}

    if tier is not None:
        org.tier = tier
    if subscription_status is not None:
        org.subscription_status = subscription_status

    session.add(org)
    await session.commit()
    await session.refresh(org)

    return {
        "id": org.id,
        "name": org.name,
        "tier": org.tier,
        "subscription_status": org.subscription_status,
    }

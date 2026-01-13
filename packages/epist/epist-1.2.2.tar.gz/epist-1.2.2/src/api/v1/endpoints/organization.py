from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user, get_session
from models.auth import Organization, OrganizationInvitation, User
from services.entitlement_service import EntitlementService

router = APIRouter()


@router.get("/me")
async def get_my_organization(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get details of the current user's organization.
    """
    stmt = select(Organization).where(Organization.id == current_user.organization_id)
    result = await session.exec(stmt)
    org = result.first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return org


@router.get("/members")
async def list_members(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    List all members of the organization.
    """
    stmt = select(User).where(User.organization_id == current_user.organization_id)
    result = await session.exec(stmt)
    return result.all()


@router.get("/invitations")
async def get_invitations(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    List pending invitations for the organization.
    """
    stmt = select(OrganizationInvitation).where(
        OrganizationInvitation.organization_id == current_user.organization_id,
        OrganizationInvitation.status == "pending",
    )
    result = await session.exec(stmt)
    return result.all()


@router.post("/invite")
async def invite_member(
    payload: dict,  # {email: str, role: str}
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Invite a new member to the organization.
    """
    # 1. RBAC Check
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can invite members")

    email = payload.get("email")
    role = payload.get("role", "member")

    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    # 2. Entitlement Check (Max Members)
    entitlement_service = EntitlementService(session)
    org = await session.get(Organization, current_user.organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    limits = entitlement_service.get_limits(org)
    max_members = limits.get("max_team_members", 1)

    # Count current members
    # Note: Usage of count might be different in SQLModel/SQLAlchemy async
    # Simple way:
    users_stmt = select(User).where(User.organization_id == org.id)
    users_result = await session.exec(users_stmt)
    current_count = len(users_result.all())

    if current_count >= max_members:
        raise HTTPException(
            status_code=403, detail=f"Team limit reached ({max_members} members). Upgrade to Pro to add more members."
        )

    # 3. Create Invitation
    # Check if existing invite
    existing_stmt = select(OrganizationInvitation).where(
        OrganizationInvitation.email == email,
        OrganizationInvitation.organization_id == org.id,
        OrganizationInvitation.status == "pending",
    )
    if (await session.exec(existing_stmt)).first():
        raise HTTPException(status_code=400, detail="Invitation already pending for this email")

    invitation = OrganizationInvitation(email=email, role=role, organization_id=org.id, invited_by_id=current_user.id)
    session.add(invitation)
    await session.commit()
    await session.refresh(invitation)

    return invitation


@router.delete("/members/{user_id}")
async def remove_member(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Remove a member from the organization.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can remove members")

    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot remove yourself")

    user_to_remove = await session.get(User, user_id)
    if not user_to_remove:
        raise HTTPException(status_code=404, detail="User not found")

    if user_to_remove.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="User not in your organization")

    # Soft delete or deactivate?
    # For now, we set active=False or remove org?
    # Logic: Set is_active=False
    user_to_remove.is_active = False
    session.add(user_to_remove)
    await session.commit()

    return {"message": "User removed"}

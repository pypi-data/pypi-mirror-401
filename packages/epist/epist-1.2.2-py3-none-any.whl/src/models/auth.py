import uuid
from datetime import datetime, timedelta

from sqlmodel import Field, Relationship, SQLModel

from core.config import settings


class OrganizationInvitation(SQLModel, table=True):
    __tablename__ = "organization_invitations"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True)
    role: str = Field(default="member")
    status: str = Field(default="pending")  # pending, accepted, expired
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    invited_by_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(seconds=getattr(settings, "INVITE_EXPIRY", 86400 * 7))
    )  # 7 days default

    organization: "Organization" = Relationship(back_populates="invitations")
    invited_by: "User" = Relationship(back_populates="sent_invitations")


class Organization(SQLModel, table=True):
    __tablename__ = "organizations"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    tier: str = Field(default="free")
    stripe_customer_id: str | None = Field(default=None, index=True)
    stripe_subscription_id: str | None = Field(default=None)
    subscription_status: str | None = Field(default=None)
    current_period_end: datetime | None = Field(default=None)
    billing_cycle_anchor: datetime | None = Field(default=None)  # To align usage resets

    # Usage Tracking
    monthly_audio_seconds: int = Field(default=0)
    usage_reset_at: datetime = Field(default_factory=datetime.utcnow)

    last_webhook_id: str | None = Field(default=None)  # For idempotency
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    users: list["User"] = Relationship(back_populates="organization")
    api_keys: list["ApiKey"] = Relationship(back_populates="organization")
    invitations: list["OrganizationInvitation"] = Relationship(back_populates="organization")


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    full_name: str
    role: str = Field(default="admin")  # 'admin' or 'member'. Default admin for first user in org.
    firebase_uid: str | None = Field(default=None, unique=True, index=True)
    avatar_url: str | None = None
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    onboarding_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    organization: Organization = Relationship(back_populates="users")
    api_keys: list["ApiKey"] = Relationship(back_populates="user")
    sent_invitations: list["OrganizationInvitation"] = Relationship(back_populates="invited_by")


class ApiKey(SQLModel, table=True):
    __tablename__ = "api_keys"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    key_hash: str = Field(index=True)
    prefix: str
    name: str
    user_id: uuid.UUID = Field(foreign_key="users.id")
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    is_active: bool = Field(default=True)
    expires_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_used_at: datetime | None = None

    user: User = Relationship(back_populates="api_keys")
    organization: Organization = Relationship(back_populates="api_keys")

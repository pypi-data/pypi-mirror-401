import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "src"))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from models.auth import Organization


async def fix_tier():
    import subprocess

    print("Fetching DB Password...")
    try:
        # Fetch password using gcloud
        process = subprocess.run(
            ["gcloud", "secrets", "versions", "access", "latest", "--secret=epist-db-password-prod"],
            capture_output=True,
            text=True,
            check=True,
        )
        db_password = process.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch password: {e}")
        return

    # Connection String for Proxy (localhost:5433)
    # Using 'epist_user' and 'epist' db name as per config
    db_url = f"postgresql+asyncpg://epist_user:{db_password}@localhost:5433/epist"

    print("Connecting to DB via Proxy...")
    engine = create_async_engine(
        db_url,
        echo=True,
        future=True,
    )
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # User email: mr.seifollahi@gmail.com -> Find organization
        # But we need to join User and Org, or just find by Org ID if I had it.
        # I don't have the Org ID handy, but I have the price ID and subscription ID from the user report.
        # But wait, I can just search by the Stripe Customer ID if they have one?
        # User provided:
        # Customer: mr.seifollahi@gmail.com
        # Subscription: sub_1Sm6ow3yCRFf2ZvZcNK1ylmH
        # Price: price_1SkAau3yCRFf2ZvZUKCoBNk3

        # We can search for the organization where a user has that email OR if we have the stripe_customer_id stored.
        # But wait, stripe_customer_id is on the Organization.
        # I'll search by stripe_subscription_id if it was saved?
        # Or I'll filter by user email first to get the org.

        from models.auth import User

        stmt = select(User).where(User.email == "mr.seifollahi@gmail.com")
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            print("User not found!")
            return

        print(f"Found user: {user.email}, Org ID: {user.organization_id}")

        stmt = select(Organization).where(Organization.id == user.organization_id)
        result = await session.execute(stmt)
        org = result.scalars().first()

        if not org:
            print("Organization not found!")
            return

        print(f"Current Org Tier: {org.tier}, Status: {org.subscription_status}")

        # update
        org.tier = "starter"
        org.subscription_status = "active"
        org.stripe_subscription_id = "sub_1Sm6ow3yCRFf2ZvZcNK1ylmH"
        # We might also want to set stripe_customer_id if it's missing, but it should be there.
        # The user report shows "Customer: mr.seifollahi@gmail.com" which implies Stripe side.

        session.add(org)
        await session.commit()
        print("Updated Organization to STARTER tier.")


if __name__ == "__main__":
    asyncio.run(fix_tier())

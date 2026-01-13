import asyncio
import os
import sys
import traceback

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.core.config import settings


async def check_db():
    print("Checking database connection...", flush=True)
    db_url = str(settings.DATABASE_URL)
    print(f"Database URL: {db_url.split('@')[-1] if '@' in db_url else 'HIDDEN'}", flush=True)

    print("Starting DB check...", flush=True)
    try:
        # Enforce a strict timeout for the entire check
        async with asyncio.timeout(10):
            print("Creating async engine...", flush=True)
            engine = create_async_engine(str(settings.DATABASE_URL))

            print("Connecting to database...", flush=True)
            async with engine.connect() as conn:
                print("Executing query...", flush=True)
                result = await conn.execute(text("SELECT 1"))
                print(f"Connection successful! Result: {result.scalar()}", flush=True)

            await engine.dispose()
    except TimeoutError:
        print("Database check timed out after 10s!", flush=True)
        sys.exit(1)
    except Exception as e:
        print(f"Database check failed: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    print("Database check passed.", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(check_db())

import logging
import socket
from typing import Any

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user, get_session
from core.config import settings
from models.auth import User

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/db-schema")
async def check_schema(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    """
    Check the current database schema.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")

    results: dict[str, Any] = {}
    tables = ["organizations", "audio_resources", "users", "transcripts", "transcript_segments", "trace_events"]

    for table in tables:
        try:
            # Query column names for the table
            query = text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
            res = await session.execute(query)
            results[table] = [row[0] for row in res.all()]
        except Exception as e:
            results[table] = f"Error: {e}"

    return results


@router.get("/db-version")
async def check_db_version(
    current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    """
    Check the current alembic version in the database.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        query = text("SELECT version_num FROM alembic_version")
        res = await session.execute(query)
        row = res.first()
        return {"version": row[0] if row else "None"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/config-check")
async def check_config(current_user: User = Depends(get_current_user)):
    """
    Check key configuration settings (masked).
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")

    api_key = settings.API_KEY
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if api_key and len(api_key) > 8 else "***"

    return {
        "ENVIRONMENT": settings.ENVIRONMENT,
        "API_KEY_MASKED": masked_key,
        "API_KEY_LENGTH": len(api_key) if api_key else 0,
        "SENTRY_DSN_SET": bool(settings.SENTRY_DSN),
        "FIREBASE_PROJECT_ID": getattr(settings, "FIREBASE_PROJECT_ID", "Not Set"),
    }


@router.get("/network")
async def test_network(current_user: User = Depends(get_current_user)):
    """
    Diagnostic endpoint to test DNS resolution and outbound connectivity.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")

    results: dict[str, Any] = {}

    # 1. Test DNS
    target_host = "www2.cs.uic.edu"
    try:
        ip = socket.gethostbyname(target_host)
        results["dns"] = {"status": "ok", "host": target_host, "ip": ip}
    except Exception as e:
        results["dns"] = {"status": "error", "host": target_host, "message": str(e)}

    # 2. Test Outbound HTTP
    target_url = "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.head(target_url, follow_redirects=True)
            results["http"] = {
                "status": "ok" if response.status_code < 400 else "error",
                "url": target_url,
                "status_code": str(response.status_code),
            }
    except Exception as e:
        results["http"] = {"status": "error", "url": target_url, "message": str(e)}

    # 3. Inspect resolv.conf
    try:
        with open("/etc/resolv.conf") as f:
            results["resolv_conf"] = f.read()
    except Exception as e:
        results["resolv_conf"] = f"Error reading /etc/resolv.conf: {e}"

    # 4. Test Internal DNS
    target_internal = "metadata.google.internal"
    try:
        ip = socket.gethostbyname(target_internal)
        results["internal_dns"] = {"status": "ok", "host": target_internal, "ip": ip}
    except Exception as e:
        results["internal_dns"] = {
            "status": "error",
            "host": target_internal,
            "message": str(e),
        }

    return results

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user
from db.session import get_session
from models.auth import User
from models.log import RequestLog, RequestLogRead

router = APIRouter()


@router.get("", response_model=list[RequestLogRead])
async def get_logs(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(default=50, le=100),
    offset: int = 0,
    status_code: int | None = None,
    method: str | None = None,
    request_id: str | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    current_user: User = Depends(get_current_user),
):
    from datetime import UTC

    query = select(RequestLog).order_by(desc(RequestLog.created_at))

    # Filter by user
    query = query.where(RequestLog.user_id == current_user.id)

    if status_code:
        query = query.where(RequestLog.status_code == status_code)

    if method:
        query = query.where(RequestLog.method == method)

    if request_id:
        query = query.where(RequestLog.request_id == request_id)

    if start_time:
        if start_time.tzinfo:
            start_time = start_time.astimezone(UTC).replace(tzinfo=None)
        query = query.where(RequestLog.created_at >= start_time)

    if end_time:
        if end_time.tzinfo:
            end_time = end_time.astimezone(UTC).replace(tzinfo=None)
        query = query.where(RequestLog.created_at <= end_time)

    query = query.offset(offset).limit(limit)

    logs = await session.exec(query)
    return logs.all()

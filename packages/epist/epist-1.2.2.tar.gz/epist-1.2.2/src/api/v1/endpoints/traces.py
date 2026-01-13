from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user, get_session
from models.auth import User
from models.trace import TraceEvent

router = APIRouter()


@router.get("", response_model=list[TraceEvent])
async def list_traces(
    limit: int = Query(50, le=100),
    offset: int = 0,
    trace_id: str | None = None,
    component: str | None = None,
    root_only: bool = True,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    List trace events. By default, lists only root spans (unique traces).
    """
    query = select(TraceEvent).order_by(desc(TraceEvent.created_at)).offset(offset).limit(limit)

    if root_only:
        query = query.where(TraceEvent.parent_span_id == None)  # noqa: E711

    if trace_id:
        query = query.where(TraceEvent.trace_id == trace_id)

    if component:
        query = query.where(TraceEvent.component == component)

    # Filter by user
    query = query.where(TraceEvent.user_id == current_user.id)

    result = await session.exec(query)
    return result.all()


@router.get("/{trace_id}", response_model=list[TraceEvent])
async def get_trace_details(
    trace_id: str, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    """
    Get all events for a specific trace ID (waterfall).
    """
    query = select(TraceEvent).where(TraceEvent.trace_id == trace_id).order_by(TraceEvent.start_time)
    result = await session.exec(query)
    events = result.all()

    if not events:
        raise HTTPException(status_code=404, detail="Trace not found")

    # Check ownership (check first event)
    if events[0].user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this trace")

    return events

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import col, func, select

from src.database import SessionDep
from src.events.dependencies import record_event
from src.events.models import AccessEvent
from src.events.schemas import AccessEventPublic, AccessEventRead

events_router = APIRouter(prefix="/events", tags=["events"])


@events_router.get(
    "/",
    response_model=AccessEventPublic,
    status_code=status.HTTP_200_OK,
    description="Paginated, filterable list of plate detections, newest first.",
    summary="Get Access Events",
)
def list_events(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=50, le=100),
    code: str | None = None,
    label: str | None = None,
    allowed: bool | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> Any:
    """
    Get access event history with optional filters.

    The total count reflects the active filters, so it stays consistent with
    paginated/infinite-scrolled results.
    """
    filters: list[Any] = []
    if code:
        clean_code = code.upper().replace(" ", "")
        filters.append(col(AccessEvent.code).ilike(f"%{clean_code}%"))
    if label:
        filters.append(col(AccessEvent.label).ilike(f"%{label}%"))
    if allowed is not None:
        filters.append(col(AccessEvent.allowed) == allowed)
    if date_from is not None:
        filters.append(col(AccessEvent.created_at) >= date_from)
    if date_to is not None:
        filters.append(col(AccessEvent.created_at) <= date_to)

    count_statement = select(func.count(AccessEvent.id))
    data_statement = select(AccessEvent).order_by(col(AccessEvent.created_at).desc())
    for condition in filters:
        count_statement = count_statement.where(condition)
        data_statement = data_statement.where(condition)

    total = session.exec(count_statement).one()
    data = session.exec(data_statement.offset(offset).limit(limit)).all()

    return {"data": data, "total": total, "offset": offset, "limit": limit}


@events_router.post(
    "/",
    response_model=AccessEventRead,
    status_code=status.HTTP_201_CREATED,
    description="Records a detected plate and resolves it against the whitelist.",
    summary="Record Detection",
)
async def create_event(event: AccessEvent = Depends(record_event)) -> Any:
    return event

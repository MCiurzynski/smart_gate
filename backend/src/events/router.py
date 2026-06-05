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
    description="Paginated list of plate detections, newest first.",
    summary="Get Access Events",
)
def list_events(
    session: SessionDep, offset: int = 0, limit: int = Query(default=50, le=100)
) -> Any:
    """
    Get access event history
    """
    count_statement = select(func.count(AccessEvent.id))
    total = session.exec(count_statement).one()

    data_statement = (
        select(AccessEvent)
        .order_by(col(AccessEvent.created_at).desc())
        .offset(offset)
        .limit(limit)
    )
    data = session.exec(data_statement).all()

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

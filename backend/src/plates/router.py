from typing import Any

from fastapi import APIRouter, Query
from sqlmodel import func, select

from src.database import SessionDep
from src.plates.models import Plate, PlatePublic

plates_router = APIRouter(prefix="/plates", tags=["plates"])


@plates_router.get(
    "/",
    response_model=PlatePublic,
    description="Returns whitelist of all license plates",
)
def read_plate(
    session: SessionDep, offset: int = 0, limit: int = Query(default=100, le=100)
) -> Any:
    """
    Get license plate list
    """
    count_statement = select(func.count(Plate.id))
    total = session.exec(count_statement).one()

    data_statement = select(Plate).offset(offset).limit(limit)
    data = session.exec(data_statement).all()

    return {"data": data, "total": total, "offset": offset, "limit": limit}

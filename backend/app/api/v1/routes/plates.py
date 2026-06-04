from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from app.api.v1.deps import SessionDep
from app.models import Plate

router = APIRouter(prefix="/plates", tags=["plates"])


@router.get("/", response_model=list[Plate])
def read_plate(session: SessionDep) -> Any:
    """
    Get license plate list
    """
    return session.exec(select(Plate)).all()

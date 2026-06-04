from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from src.database import SessionDep
from src.models import Plate

router = APIRouter()


@router.get("/plates", response_model=list[Plate])
def read_plate(session: SessionDep) -> Any:
    """
    Get license plate list
    """
    return session.exec(select(Plate)).all()

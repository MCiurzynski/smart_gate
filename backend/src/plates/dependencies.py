from collections.abc import Mapping
from typing import Any

from fastapi import Depends, HTTPException
from sqlmodel import select

from src.database import SessionDep
from src.plates.models import Plate
from src.plates.schemas import PlateCreate, PlateUpdate


async def get_plate_by_code(session: SessionDep, plate_code: str) -> Plate | None:
    """
    Finds license plate by code
    """
    clean_code = plate_code.upper().replace(" ", "")
    return session.exec(select(Plate).where(Plate.code == clean_code)).first()


async def create_plate_by_code(session: SessionDep, plate_in: PlateCreate) -> Any:
    """
    Create a new license plate
    """
    plate = Plate.model_validate(plate_in)
    session.add(plate)
    session.commit()
    session.refresh(plate)
    return plate


async def update_plate_by_code(
    session: SessionDep,
    plate: Mapping = Depends(get_plate_by_code),
    *,
    plate_in: PlateUpdate,
) -> Any:
    """
    Update license plate
    """
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")

    update_data = plate_in.model_dump(exclude_unset=True)
    plate.sqlmodel_update(update_data)

    session.add(plate)
    session.commit()
    session.refresh(plate)
    return plate

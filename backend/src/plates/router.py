from collections.abc import Mapping
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import func, select

from src.database import SessionDep
from src.plates.dependencies import (
    create_plate_by_code,
    get_plate_by_code,
    update_plate_by_code,
)
from src.plates.models import Plate
from src.plates.schemas import PlatePublic

plates_router = APIRouter(prefix="/plates", tags=["plates"])


@plates_router.get(
    "/",
    response_model=PlatePublic,
    status_code=status.HTTP_200_OK,
    description="Returns a paginated list of all license plates in the whitelist.",
    summary="Get All Plates",
    responses={
        status.HTTP_200_OK: {
            "model": PlatePublic,
            "description": "Successfully retrieved the list of license plates.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User is not authenticated.",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "User does not have sufficient permissions.",
        },
    },
)
def list_plate(
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


@plates_router.post(
    "/",
    response_model=Plate,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new license plate entry",
    summary="Create Plate",
)
async def create_plate(plate: Mapping = Depends(create_plate_by_code)) -> Any:
    return plate


@plates_router.patch(
    "/{plate_code}",
    response_model=Plate,
    status_code=status.HTTP_200_OK,
    description="Updates an existing license plate by code",
    summary="Update Plate",
)
async def update_plate(plate: Mapping = Depends(update_plate_by_code)) -> Any:
    return plate


@plates_router.delete(
    "/{plate_code}",
    status_code=status.HTTP_200_OK,
    description="Deletes a license plate entry",
    summary="Delete Plate",
)
async def delete_plate(
    session: SessionDep, plate: Mapping = Depends(get_plate_by_code)
) -> Any:
    """
    Delete license plate
    """
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")

    session.delete(plate)
    session.commit()
    return {"message": "Plate deleted successfully"}


@plates_router.get(
    "/{plate_code}",
    status_code=status.HTTP_200_OK,
    description="Checks whether license plate is on the whitelist",
    summary="Check license plate",
)
async def check_plate(plate: Mapping = Depends(get_plate_by_code)):
    """
    Checks whether license plate is on the whitelist
    """
    if not plate:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized license plate"
        )

    return {"message": "Plate on whitelist", "data": plate}

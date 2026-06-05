from typing import Any

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import func, select

from src.database import SessionDep
from src.plates.models import Plate, PlateCreate, PlatePublic, PlateUpdate

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


@plates_router.post(
    "/",
    response_model=Plate,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new license plate entry",
    summary="Create Plate",
)
async def create_plate(session: SessionDep, plate_in: PlateCreate) -> Any:
    """
    Create a new license plate
    """
    plate = Plate.model_validate(plate_in)
    session.add(plate)
    session.commit()
    session.refresh(plate)
    return plate


@plates_router.patch(
    "/{plate_code}",
    response_model=Plate,
    status_code=status.HTTP_200_OK,
    description="Updates an existing license plate by code",
    summary="Update Plate",
)
async def update_plate(
    session: SessionDep, plate_code: str, plate_in: PlateUpdate
) -> Any:
    """
    Update license plate
    """
    db_plate = session.get(Plate, plate_code)
    if not db_plate:
        raise HTTPException(status_code=404, detail="Plate not found")

    update_data = plate_in.model_dump(exclude_unset=True)
    db_plate.sqlmodel_update(update_data)
    session.add(db_plate)
    session.commit()
    session.refresh(db_plate)
    return db_plate


@plates_router.delete(
    "/{plate_code}",
    status_code=status.HTTP_200_OK,
    description="Deletes a license plate entry",
    summary="Delete Plate",
)
async def delete_plate(session: SessionDep, plate_code: str) -> Any:
    """
    Delete license plate
    """
    db_plate = session.get(Plate, plate_code)
    if not db_plate:
        raise HTTPException(status_code=404, detail="Plate not found")

    session.delete(db_plate)
    session.commit()
    return {"message": "Plate deleted successfully"}

import uuid

from sqlmodel import Field, SQLModel

from src.plates.schemas import PlateBase


class Plate(PlateBase, SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

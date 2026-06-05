import uuid

from sqlmodel import Field, SQLModel


class PlateBase(SQLModel):
    label: str | None = None
    code: str = Field(index=True, unique=True)


class PlateCreate(PlateBase):
    pass


class PlateUpdate(PlateBase):
    pass


class Plate(PlateBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class PlatePublic(SQLModel):
    data: list[Plate]
    total: int
    offset: int
    limit: int

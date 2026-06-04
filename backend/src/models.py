from sqlmodel import Field, SQLModel


class PlateBase(SQLModel):
    label: str | None = None


class PlateCreate(PlateBase):
    code: str


class PlateUpdate(PlateBase):
    pass


class Plate(PlateBase, table=True):
    code: str = Field(primary_key=True)

import uuid
from datetime import datetime

from sqlmodel import SQLModel


class AccessEventCreate(SQLModel):
    code: str


class AccessEventRead(SQLModel):
    id: uuid.UUID
    code: str
    allowed: bool
    label: str | None
    created_at: datetime


class AccessEventPublic(SQLModel):
    data: list[AccessEventRead]
    total: int
    offset: int
    limit: int

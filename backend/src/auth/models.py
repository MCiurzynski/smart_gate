import uuid
from datetime import datetime

from sqlmodel import DateTime, Field, SQLModel

from src.auth.utils import get_datetime_utc


class UserBase(SQLModel):
    name: str = Field(unique=True, min_length=4, max_length=24)


class UserCreate(SQLModel):
    password: str = Field(min_length=8, max_length=30)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    create_at: datetime | None = Field(
        default_factory=get_datetime_utc, sa_type=DateTime(timezone=True)
    )

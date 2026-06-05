import uuid
from datetime import datetime

from sqlmodel import DateTime, Field, SQLModel

from src.auth.utils import get_datetime_utc


class AccessEvent(SQLModel, table=True):
    __tablename__ = "access_events"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    code: str = Field(index=True, max_length=16)
    allowed: bool = Field(default=False)
    label: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
        index=True,
    )

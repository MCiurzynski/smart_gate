import re

from pydantic import field_validator
from sqlmodel import Field, SQLModel

PATTERNS = [
    # Two-letter county code
    r"^[A-Z]{2}[0-9]{5}$",
    r"^[A-Z]{2}[0-9]{4}[A-Z]$",
    r"^[A-Z]{2}[0-9]{3}[A-Z]{2}$",
    r"^[A-Z]{2}[1-9][A-Z][0-9]{3}$",
    r"^[A-Z]{2}[1-9][A-Z]{2}[0-9]{2}$",
    # Three-letter county code
    r"^[A-Z]{3}[A-Z][0-9]{3}$",
    r"^[A-Z]{3}[0-9]{2}[A-Z]{2}$",
    r"^[A-Z]{3}[1-9][A-Z][0-9]{2}$",
    r"^[A-Z]{3}[0-9]{2}[A-Z][1-9]$",
    r"^[A-Z]{3}[1-9][A-Z]{2}[1-9]$",
    r"^[A-Z]{3}[A-Z]{2}[0-9]{2}$",
    r"^[A-Z]{3}[0-9]{5}$",
    r"^[A-Z]{3}[0-9]{4}[A-Z]$",
    r"^[A-Z]{3}[0-9]{3}[A-Z]{2}$",
    r"^[A-Z]{3}[A-Z][0-9]{2}[A-Z]$",
    r"^[A-Z]{3}[A-Z][1-9][A-Z]{2}$",
    # Reduced-size
    r"^[A-Z][0-9]{3}$",
    r"^[A-Z][0-9]{2}[A-Z]$",
    r"^[A-Z][1-9][A-Z][1-9]$",
    r"^[A-Z]{2}[0-9]{2}$",
    r"^[A-Z][1-9][A-Z]{2}$",
    r"^[A-Z]{3}[1-9]$",
    r"^[A-Z]{2}[1-9][A-Z]$",
]


class PlateBase(SQLModel):
    label: str | None = None
    code: str = Field(index=True, unique=True, min_length=3, max_length=10)

    @field_validator("code")
    @classmethod
    def validate_polish_plate(cls, v: str) -> str:
        clean_v = v.upper().replace(" ", "")

        if not any(re.fullmatch(p, clean_v) for p in PATTERNS):
            raise ValueError(
                f"Invalid Polish license plate format: '{v}. "
                "Does not match any official registration plate standard."
            )
        return clean_v


class PlateCreate(PlateBase):
    pass


class PlateUpdate(PlateBase):
    pass


class PlatePublic(SQLModel):
    data: list[PlateBase]
    total: int
    offset: int
    limit: int

from datetime import UTC, datetime

from argon2 import PasswordHasher

ph = PasswordHasher()


def get_password_hash(password: str) -> str:
    """Uses Argon2 to hash password"""
    return ph.hash(password)


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)

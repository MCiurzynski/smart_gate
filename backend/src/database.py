from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine, select

from src.auth.dependencies import create_user
from src.auth.models import User, UserCreate
from src.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    user = session.exec(
        select(User).where(User.name == settings.SUPERUSER_NAME)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.SUPERUSER_NAME,
            password=settings.SUPERUSER_PASSWORD,
        )
        user = create_user(session=session, user_create=user_in)


SessionDep = Annotated[Session, Depends(get_db)]

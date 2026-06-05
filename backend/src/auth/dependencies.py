from sqlmodel import Session

from src.auth.models import User, UserCreate
from src.auth.utils import get_password_hash


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User(
        name=user_create.name, hashed_password=get_password_hash(user_create.password)
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

from typing import Optional

from sqlalchemy import select, true
from werkzeug.security import generate_password_hash

from shared.database import SessionLocal, engine, logger
from shared.models import User


def get_user(user_id: str) -> Optional[User]:
    with SessionLocal() as session:
        return session.get(User, user_id)


def is_admin_exists() -> bool:
    stmt = select(User).where(User.is_admin.is_(true()))
    with SessionLocal() as session:
        return session.scalar(stmt) is not None


def create_tables() -> None:
    from shared.models import Base

    Base.metadata.create_all(bind=engine)


def get_user_by_name(user_name: str) -> Optional[User]:
    with SessionLocal() as session:
        return session.scalar(select(User).where(User.name == user_name))


def add_admin(
    user_name: str,
    password: str,
) -> Optional[User]:
    with SessionLocal() as session:
        try:
            user = User(
                name=user_name,
                password_hash=generate_password_hash(password),
                is_admin=True,
            )
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            logger.error(e)
    return None

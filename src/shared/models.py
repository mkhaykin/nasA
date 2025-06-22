import datetime

from flask_login import UserMixin
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash


class Base(DeclarativeBase):
    pass


class User(Base, UserMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=False,
        server_default="f",
    )

    is_admin = Column(Boolean, default=True)

    __table_args__ = (UniqueConstraint("name", name="uc_name"),)

    def __repr__(self) -> str:
        return self.name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def change_password(self, password_old: str, password_new: str) -> None:
        if self.check_password(password_old):
            self.set_password(password_new)

    def get_id(self) -> str:
        return str(self.user_id)


class Ticket(Base):
    __tablename__ = "tickets"
    ticket_id = Column(Integer, primary_key=True)
    ticket_hash = Column(String(128), unique=True, nullable=False)
    is_reserved = Column(Boolean, default=False)
    reserved_at = Column(DateTime)
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime)
    file_uploaded = Column(String(256))
    created_at = Column(DateTime, default=datetime.datetime.now())

    RESERVATION_TIMEOUT = 5

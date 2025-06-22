from datetime import datetime, timedelta
from typing import Optional, Sequence

import sqlalchemy as sa
from sqlalchemy import and_, false, true

from shared.database import SessionLocal, logger
from shared.models import Ticket
from shared.utils import generate_secure_ticket, hash_ticket


def generate_tickets(count: int) -> Sequence[str]:
    with SessionLocal() as session:
        try:
            session.execute(sa.delete(Ticket))

            tickets = [generate_secure_ticket() for _ in range(count)]
            for t in tickets:
                session.add(Ticket(ticket_hash=hash_ticket(t)))

            session.commit()
            return tickets
        except Exception as e:
            session.rollback()
            logger.error(e)

    return []


def get_tickets() -> Sequence[Ticket]:
    stmt = sa.select(Ticket)
    with SessionLocal() as session:
        try:
            result = session.execute(stmt).scalars().all()
        except Exception as e:
            logger.error(e)

    return result


def validate_ticket(ticket_value: str) -> Optional[Ticket]:
    """Проверяет тикет"""
    hashed = hash_ticket(ticket_value)
    stmt = sa.select(Ticket).where(Ticket.ticket_hash == hashed)
    with SessionLocal() as session:
        try:
            ticket = session.execute(stmt).scalar_one_or_none()
            return ticket
        except Exception as e:
            logger.error(e)

    return None


def reserve_ticket(ticket_id: int) -> bool:
    """Проверяет тикет и резервирует его"""
    stmt = (
        sa.update(Ticket)
        .where(Ticket.ticket_id == ticket_id)
        .where(Ticket.is_used.is_(false()))
        .where(Ticket.is_reserved.is_(false()))
        .values(
            is_reserved=True,
            reserved_at=datetime.now(),
        )
    )
    with SessionLocal() as session:
        try:
            result = session.execute(stmt)
            session.commit()
            if result.rowcount == 1:
                return True
            elif result.rowcount > 1:
                raise Exception("Ошибка блокировки")
        except Exception as e:
            session.rollback()
            logger.error(e)

    return False


def use_ticket(ticket_id: int) -> bool:
    """Проверяет тикет и резервирует его"""
    stmt = (
        sa.update(Ticket)
        .where(Ticket.ticket_id == ticket_id)
        .where(Ticket.is_used.is_(false()))
        .where(Ticket.is_reserved.is_(true()))
        .values(
            is_used=True,
            used_at=datetime.now(),
        )
    )
    with SessionLocal() as session:
        try:
            result = session.execute(stmt)
            session.commit()
            if result.rowcount == 1:
                return True
            elif result.rowcount > 1:
                raise Exception("Ошибка использования")
        except Exception as e:
            session.rollback()
            logger.error(e)

    return False


def release_expired() -> None:
    """Освобождение просроченных резерваций"""
    timeout = datetime.now() - timedelta(minutes=Ticket.RESERVATION_TIMEOUT)

    with SessionLocal() as session:
        try:
            session.execute(
                sa.update(Ticket)
                .where(
                    and_(
                        Ticket.is_reserved.is_(true()),
                        Ticket.reserved_at < timeout,
                        Ticket.is_used.is_(false()),
                    ),
                )
                .values(
                    is_reserved=False,
                ),
            )
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(e)

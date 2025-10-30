from fastapi import HTTPException
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ticket
from app.schemas import (
    TicketCreate,
    TicketOut,
    PaginatedTickets,
    TicketUpdate
)
from app.utils import Status


async def create_ticket(payload: TicketCreate, db: AsyncSession) -> TicketOut:
    ticket = Ticket(**payload.model_dump())
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return TicketOut.model_validate(ticket)


async def get_tickets_count(
        db: AsyncSession,
        *,
        search: str | None = None,
        status: Status | None = None,
        assigned_id: int | None = None
) -> int:
    q = select(func.count(Ticket.id))
    if search:
        q = q.where(Ticket.title.ilike(f"%{search}%"))
    if status:
        q = q.where(Ticket.status == status)
    if assigned_id is not None:
        q = q.where(Ticket.assigned_to_id == assigned_id)
    result = await db.execute(q)
    return result.scalar_one()


async def list_tickets(
        page: int,
        size: int,
        search: str,
        status: Status,
        assigned_id: int,
        db: AsyncSession
) -> PaginatedTickets:
    skip = (page - 1) * size

    q = select(Ticket).order_by(Ticket.created_at.desc())

    if search:
        q = q.where(Ticket.title.ilike(f"%{search}%"))
    if status:
        q = q.where(Ticket.status == Status(status))
    if assigned_id is not None:
        q = q.where(Ticket.assigned_to_id == assigned_id)

    total = await get_tickets_count(
        db,
        search=search,
        status=Status(status) if status else None,
        assigned_id=assigned_id
    )

    q = q.offset(skip).limit(size)
    res = await db.execute(q)
    tickets = res.scalars().unique().all()
    tickets = [TicketOut.model_validate(ticket) for ticket in tickets]

    return PaginatedTickets(
        total=total,
        page=page,
        size=size,
        tickets=tickets
    )


async def update_ticket(payload: TicketUpdate, db: AsyncSession) -> TicketOut:
    values = {}

    if payload.assigned_id is not None:
        values["assigned_id"] = payload.assigned_id
    if payload.status is not None:
        values["status"] = payload.status

    if not values:
        raise HTTPException(status_code=400, detail="No fields to update")

    q = (
        update(Ticket)
        .where(Ticket.id == payload.ticket_id)
        .values(**values)
        .returning(Ticket)
    )

    result = await db.execute(q)
    await db.commit()

    ticket = result.scalar_one()
    return TicketOut.model_validate(ticket)


async def delete_ticket(ticket_id: int, db: AsyncSession) -> None:
    q = delete(Ticket).where(Ticket.id == ticket_id)
    await db.execute(q)
    await db.commit()

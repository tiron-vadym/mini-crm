from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.crud.tickets import (
    create_ticket,
    update_ticket,
    list_tickets,
    delete_ticket
)
from app.models import User
from app.schemas import (
    TicketCreate,
    TicketOut,
    PaginatedTickets,
    TicketUpdate
)
from app.dependencies import get_db, get_current_user, require_admin

router = APIRouter(tags=["tickets"])


@router.post("/tickets", response_model=TicketOut, status_code=HTTP_201_CREATED)
async def create_public_ticket(
        payload: TicketCreate,
        db: AsyncSession = Depends(get_db)
):
    ticket = await create_ticket(payload, db)
    return ticket


@router.patch("/tickets", response_model=TicketOut, status_code=HTTP_200_OK)
async def assign_ticket(
        payload: TicketUpdate,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if user.role != "admin" and payload.assign_id is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to assign tickets"
        )

    ticket = await update_ticket(payload, db)
    return ticket


@router.get("/tickets", response_model=PaginatedTickets, status_code=HTTP_200_OK)
async def my_tickets(
        page: int = 1,
        size: int = 20,
        search: str | None = None,
        status: str | None = None,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    assigned_id = None if user.role == "admin" else user.id
    return await list_tickets(page, size, search, status, assigned_id, db)


@router.delete("/tickets", status_code=status.HTTP_204_NO_CONTENT)
async def remove_ticket(
        ticket_id: int,
        user: User = Depends(require_admin),
        db: AsyncSession = Depends(get_db)
):
    await delete_ticket(ticket_id, db)

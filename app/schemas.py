from pydantic import BaseModel
from datetime import datetime

from app.utils import Role, BaseModelORM, Status


class UserCreate(BaseModel):
    username: str
    password: str
    role: Role


class UserOut(BaseModelORM):
    id: int
    username: str
    role: Role


class TokenSchema(BaseModelORM):
    access_token: str


class LoginSchema(BaseModelORM):
    username: str
    password: str


class ClientCreate(BaseModelORM):
    name: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None


class ClientOut(ClientCreate):
    id: int


class TicketCreate(BaseModel):
    title: str
    description: str | None = None
    client_id: int


class TicketUpdate(BaseModel):
    ticket_id: int
    assigned_id: int | None = None
    status: Status


class TicketList(BaseModel):
    page: int = 1
    size: int = 20
    search: str | None = None
    status: str | None = None
    assigned_id: int | None = None


class TicketOut(BaseModelORM):
    id: int
    title: str
    description: str | None
    status: str
    created_at: datetime
    client_id: int
    assigned_id: int | None


class PaginatedTickets(BaseModel):
    total: int
    page: int
    size: int
    tickets: list[TicketOut]

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import Role, Status


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(Enum(Role), nullable=False)

    tickets = relationship("Ticket", back_populates="assigned_to")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    phone = Column(String(32))
    email = Column(String(64))
    address = Column(String(128))

    tickets = relationship("Ticket", back_populates="client")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False, index=True)
    description = Column(Text)
    status = Column(Enum(Status), default=Status.new, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    assigned_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    client = relationship("Client", back_populates="tickets")
    assigned_to = relationship("User", back_populates="tickets")

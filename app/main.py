from fastapi import FastAPI
from app.routers import auth, tickets, client

app = FastAPI(title="Mini-CRM Repair Requests")

app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(client.router)


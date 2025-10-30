# Mini-CRM "Repair Requests"

Tech: FastAPI, SQLAlchemy async, PostgreSQL, Alembic, Docker

## Quick start (pull from Docker Hub)
Update `.env` with correct values.

```bash
use alembic revision --autogenerate -m "init tables"
docker compose up -d
```

# High-level business flow
1) A customer submits a repair request via a public form (open API).
2) A request is created with an initial status (e.g., new).
3) An admin reviews new requests and assigns them to a worker.
4) A worker sees their assigned requests.
5) The worker progresses the request (e.g., "in progress") and completes it ("done").

# Functional possibilities
- Pagination on list endpoint.
- Auth: simple JWT; admin and worker must log in.
- User management: admin can Create/Read/Update/Delete workers.
- Public API to create a repair request.
- Search by request title (admin/worker tasks list).
- Status filtering (admin/worker tasks list).
- Permissions: admin has full access; worker can only work with their own requests.
- Proper validation and HTTP success/error codes.

# Entities
- User (role: admin|worker, password hash)
- Client (basic contact info)
- Ticket

# Endpoints:
- POST /auth/token
- POST /auth/users
- CRUD /tickets
- POST /clients
- GET /clients/{client_name}


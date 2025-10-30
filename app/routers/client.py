from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.crud.client import get_client_by_name, create_client
from app.dependencies import get_db
from app.schemas import ClientOut, ClientCreate

router = APIRouter(tags=["client"])


@router.post(
    "/clients",
    response_model=ClientOut,
    status_code=HTTP_201_CREATED
)
async def add_client(
        payload: ClientCreate,
        db: AsyncSession = Depends(get_db)
):
    client = await create_client(payload.model_dump(), db)
    return client


@router.get(
    "/clients/{client_name}",
    response_model=ClientOut | None,
    status_code=HTTP_200_OK
)
async def get_client(
        client_name: str,
        db: AsyncSession = Depends(get_db)
):
    client = await get_client_by_name(client_name, db)
    return client

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Client
from app.schemas import ClientOut


async def create_client(data: dict, db: AsyncSession) -> ClientOut:
    client = Client(**data)
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return ClientOut.model_validate(client)


async def get_client_by_name(name: str, db: AsyncSession) -> ClientOut | None:
    q = await db.execute(select(Client).where(Client.name == name))
    user = q.scalars().one_or_none()
    return ClientOut.model_validate(user)

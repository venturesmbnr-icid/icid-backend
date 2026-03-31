from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
from typing import List, Optional


async def create_client(db: AsyncSession, payload: ClientCreate) -> Client:
    obj = Client(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_client(db: AsyncSession, client_id: str) -> Optional[Client]:
    result = await db.execute(select(Client).where(Client.client_id == client_id))
    return result.scalar_one_or_none()


async def list_clients(db: AsyncSession) -> List[Client]:
    result = await db.execute(select(Client))
    return result.scalars().all()


async def update_client(
    db: AsyncSession, client_id: str, payload: ClientUpdate
) -> Optional[Client]:
    obj = await get_client(db, client_id)
    if not obj:
        return None

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(obj, field, value)

    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_client(db: AsyncSession, client_id: str) -> bool:
    obj = await get_client(db, client_id)
    if not obj:
        return False

    await db.delete(obj)
    await db.commit()
    return True

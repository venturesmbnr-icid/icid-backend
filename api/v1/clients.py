from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.crud.client import (
    create_client, get_client, list_clients, update_client, delete_client
)

router = APIRouter(prefix="/v1/clients", tags=["Clients"])


@router.post("/", response_model=ClientRead)
async def create(db: AsyncSession = Depends(get_session), payload: ClientCreate = None):
    return await create_client(db, payload)


@router.get("/", response_model=list[ClientRead])
async def list_all(db: AsyncSession = Depends(get_session)):
    return await list_clients(db)


@router.get("/{client_id}", response_model=ClientRead)
async def read(client_id: str, db: AsyncSession = Depends(get_session)):
    obj = await get_client(db, client_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    return obj


@router.put("/{client_id}", response_model=ClientRead)
async def update(client_id: str, payload: ClientUpdate, db: AsyncSession = Depends(get_session)):
    obj = await update_client(db, client_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    return obj


@router.delete("/{client_id}")
async def delete(client_id: str, db: AsyncSession = Depends(get_session)):
    ok = await delete_client(db, client_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"status": "deleted"}

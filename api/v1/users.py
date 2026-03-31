from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from uuid import UUID

# from api.db.session import get_session
# from api.schemas.user import UserCreate, UserRead, UserUpdate
# from api.schemas.user import UserRead
from api.schemas.user import UserListResponse


# from api.crud.user import (
#     create_user, get_user, list_users, update_user, delete_user
# )
from api.queries.users import get_all_users


router = APIRouter(prefix="/v1/users", tags=["Users"])


# @router.post("/", response_model=UserRead)
# async def create(db: AsyncSession = Depends(get_session), payload: UserCreate = None):
#     obj = await create_user(db, payload)
#     return obj



@router.get("/", response_model=UserListResponse)
async def list_all():
    rows = get_all_users()

    list_of_users = [
        {
            "user_id": row[0],
            "email": row[1],
            "first_name": row[2],
            "last_name": row[3],
            "phone_number": row[4],
            "employer": row[5],
        }
        for row in rows
    ]

    return {
        "status": "success",
        "message": "List of all users",
        "data": list_of_users,
    }

# @router.get("/", response_model=list[UserRead])
# async def list_all(db: AsyncSession = Depends(get_session)):
#     return await list_users(db)




# @router.get("/{uuid}", response_model=UserRead)
# async def read(uuid: UUID, db: AsyncSession = Depends(get_session)):
#     obj = await get_user(db, uuid)
#     if not obj:
#         raise HTTPException(status_code=404, detail="User not found")
#     return obj


# @router.put("/{uuid}", response_model=UserRead)
# async def update(uuid: UUID, payload: UserUpdate, db: AsyncSession = Depends(get_session)):
#     obj = await update_user(db, uuid, payload)
#     if not obj:
#         raise HTTPException(status_code=404, detail="User not found")
#     return obj


# @router.delete("/{uuid}")
# async def delete(uuid: UUID, db: AsyncSession = Depends(get_session)):
#     ok = await delete_user(db, uuid)
#     if not ok:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"status": "deleted"}

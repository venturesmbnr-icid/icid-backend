from fastapi import APIRouter, HTTPException
from api.schemas.user import UserListItem, UserListResponse
from api.queries.users import get_all_users

router = APIRouter(prefix="/v1/users", tags=["Users"])


@router.get("/", response_model=UserListResponse)
def list_all_users():
    rows = get_all_users()

    if rows is None:
        raise HTTPException(status_code=500, detail="Failed to fetch users")

    data = [
        UserListItem(
            user_id=str(row[0]),
            email=row[1],
            first_name=row[2],
            last_name=row[3],
            phone_number=row[4],
            employer=row[5],
        )
        for row in rows
    ]

    return UserListResponse(
        status="success",
        message="List of all users",
        data=data,
    )

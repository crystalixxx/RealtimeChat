from fastapi import APIRouter, Depends, HTTPException

from app.database.crud.user import (
    get_all_users,
    get_user_by_id,
    block_user,
    unblock_user,
    create_user,
    delete_user,
    update_user,
)
from app.database.schemas.user import UserCreate, UserUpdate
from app.database.session import get_db_connection
from app.misc.auth import get_current_user, get_current_superuser
from starlette import status

user_router = APIRouter()


@user_router.get("/")
async def read_users(
    db=Depends(get_db_connection), current_user=Depends(get_current_user)
):
    return get_all_users(db)


@user_router.get("/{user_id}")
async def user_by_id(
    user_id: int, db=Depends(get_db_connection), current_user=Depends(get_current_user)
):
    current_user = get_user_by_id(db, user_id)

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return current_user


@user_router.post("/{user_id}")
async def user_create(
    user: UserCreate,
    db=Depends(get_db_connection),
    current_user=Depends(get_current_superuser),
):
    user = create_user(db, user)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    return user


@user_router.delete("/{user_id}")
async def user_delete(
    user_id: int,
    db=Depends(get_db_connection),
    current_user=Depends(get_current_superuser),
):
    return delete_user(db, user_id)


@user_router.patch("/{user_id}")
async def user_update(
    user_id: int,
    user: UserUpdate,
    db=Depends(get_db_connection),
    current_user=Depends(get_current_superuser),
):
    return update_user(db, user, current_user)


@user_router.post("/block/{user_id}")
async def user_block(
    user_id: int,
    db=Depends(get_db_connection),
    current_user=Depends(get_current_superuser),
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    current_user = block_user(db, user_id)

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return current_user


@user_router.post("/unblock/{user_id}")
async def user_unblock(
    user_id: int,
    db=Depends(get_db_connection),
    current_user=Depends(get_current_superuser),
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    current_user = unblock_user(db, user_id)

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return current_user

from fastapi import APIRouter, Depends

from app.database.session import get_db_connection
from app.misc.auth import get_current_user

chats_router = APIRouter()


@chats_router.get("/")
async def list_of_chats(
    db=Depends(get_db_connection), current_user=Depends(get_current_user)
):
    return current_user.chats

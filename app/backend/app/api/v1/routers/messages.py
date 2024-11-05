from fastapi import APIRouter, Depends, HTTPException

from app.misc.auth import get_current_user
from app.database.session import get_db_connection
from app.database.schemas.message import MessageCreate, Message
from app.database.crud.user import get_user_by_id
from app.database.crud.messages import send_message, delete_message, get_message_by_id
from app.database.crud.chats import user_is_member_of_chat
from starlette.status import HTTP_409_CONFLICT

messages_router = APIRouter()


@messages_router.post("/{user_id}/{chat_id}", response_model=Message)
async def message_send(
    user_id: int,
    chat_id: int,
    message: MessageCreate,
    db=Depends(get_db_connection),
    current_user=Depends(user_is_member_of_chat),
):
    user = get_user_by_id(db, current_user.member_id)

    if user.is_blocked:
        return

    return send_message(db, user_id, chat_id, message.content)


@messages_router.delete("/{message_id}")
async def message_delete(
    message_id: int,
    db=Depends(get_db_connection),
    current_user=Depends(get_current_user),
):
    if current_user.is_blocked:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="User has been blocked"
        )

    message = await get_message_by_id(db, message_id)

    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    if message.sender_id == current_user.id or current_user.is_superadmin:
        return delete_message(db, message_id)

    raise HTTPException(status_code=403, detail="Not enough permissions")

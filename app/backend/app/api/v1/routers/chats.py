from asyncio import create_task
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from app.database.crud.chats import create_chat
from app.database.crud.messages import get_messages_from_chat
from app.database.session import get_db_connection
from app.misc.auth import get_current_user
from app.database.schemas.chat import ChatCreate
from app.misc.connections.redis_connection_manager import chat_manager
from starlette.status import HTTP_409_CONFLICT

chats_router = APIRouter()


@chats_router.get("/")
async def list_of_chats(
    db=Depends(get_db_connection), current_user=Depends(get_current_user)
):
    return {"chats": current_user.chats}


@chats_router.post("/{user_id}")
async def chat_create(
    user_id: int,
    chat_scheme: ChatCreate,
    db=Depends(get_db_connection),
    current_user=Depends(get_current_user),
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="Can't create chat with yourself"
        )

    return create_chat(db, chat_scheme.name, current_user.id, user_id)


@chats_router.websocket("/ws/{chat_id}/{user_id}")
async def chat_endpoint(
    websocket: WebSocket,
    chat_id: int,
    user_id: int,
    db=Depends(get_db_connection),
):
    print("here")

    await websocket.accept()
    await chat_manager.connect(chat_id, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            await chat_manager.send_message(chat_id, data, user_id, db)

    except WebSocketDisconnect:
        chat_manager.disconnect(chat_id, user_id)


@chats_router.get("/{chat_id}")
async def get_chat_messages(
    chat_id: int, db=Depends(get_db_connection), current_user=Depends(get_current_user)
):
    return get_messages_from_chat(db, chat_id)

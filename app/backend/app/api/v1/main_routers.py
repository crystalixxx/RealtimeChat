from fastapi import APIRouter

from .routers.auth import auth_router
from .routers.chats import chats_router
from .routers.user import user_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/api", tags=["auth"])
api_router.include_router(chats_router, prefix="/api/chats", tags=["chats"])
api_router.include_router(user_router, prefix="/api/users", tags=["users"])

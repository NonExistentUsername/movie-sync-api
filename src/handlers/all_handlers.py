from fastapi import APIRouter

from handlers.auth import auth_router
from handlers.commands import commands_router
from handlers.rooms import rooms_router
from handlers.users import users_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(rooms_router, prefix="/rooms", tags=["rooms"])
api_router.include_router(commands_router, prefix="/commands", tags=["commands"])

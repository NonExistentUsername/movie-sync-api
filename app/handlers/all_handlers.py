from fastapi import APIRouter
from handlers.auth import auth_router
from handlers.users import users_router
from handlers.app import app_router
from handlers.commands import commands_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=["users"])
api_router.include_router(users_router, prefix='/users', tags=["users"])
api_router.include_router(commands_router, prefix='/commands', tags=["commands"])
api_router.include_router(app_router, prefix='/app', tags=["app"])

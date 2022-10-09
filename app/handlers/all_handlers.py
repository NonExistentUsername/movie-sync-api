from fastapi import APIRouter, Depends
from handlers.auth import auth_router
from handlers.users import users_router
from handlers.app import app_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth')
api_router.include_router(users_router, prefix='/users')
api_router.include_router(app_router, prefix='/app')

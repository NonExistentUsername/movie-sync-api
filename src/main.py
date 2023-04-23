from fastapi import FastAPI
from fastapi_pagination import add_pagination

import core.global_variables
from db.base_class import Base
from db.session import engine
from handlers.all_handlers import api_router
from models.associations import user_room_member_association_table
from models.room import Room
from models.user import User


def get_application():
    tags_metadata = [
        {
            "name": "auth",
            "description": "Authorization.",
        },
        {
            "name": "users",
            "description": "Operations with users.",
        },
        {
            "name": "rooms",
            "description": "Operations with rooms.",
        },
        {
            "name": "commands",
            "description": "Operations with commands.",
        },
        {
            "name": "app",
            "description": "Get last update for application.",
        },
    ]
    application = FastAPI(
        title="MirumApp",
        openapi_tags=tags_metadata,
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    )
    application.include_router(api_router)
    add_pagination(application)
    return application


app = get_application()


@app.on_event("startup")
def init():
    core.global_variables.init()

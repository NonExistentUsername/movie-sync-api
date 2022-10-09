import os
from fastapi import FastAPI
from handlers.all_handlers import api_router
from db.session import engine
from db.base_class import Base
from fastapi_pagination import add_pagination
# import core.global_variables


Base.metadata.create_all(bind=engine)


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
        openapi_tags=tags_metadata
    )
    application.include_router(api_router)
    add_pagination(application)
    return application


app = get_application()


# @app.on_event("startup")
# def init():
#     core.global_variables.init()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", app_dir="app", port=8000, host="127.0.0.1", reload=True, workers=1)

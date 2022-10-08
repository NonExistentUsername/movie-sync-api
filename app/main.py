import os
from fastapi import FastAPI
from handlers import router
from db.session import engine
from db.base_class import Base
from fastapi_pagination import add_pagination
# import core.global_variables


Base.metadata.create_all(bind=engine)


def get_application():
    application = FastAPI()
    application.include_router(router)
    add_pagination(application)
    return application


app = get_application()


# @app.on_event("startup")
# def init():
#     core.global_variables.init()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", app_dir="app", port=8000, host="127.0.0.1", reload=True, workers=1)

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

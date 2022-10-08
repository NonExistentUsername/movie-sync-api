import os

from fastapi import FastAPI
from handlers.all_handlers import api_router

from db.session import engine
from db.base_class import Base
from fastapi_pagination import add_pagination
import core.global_variables


Base.metadata.create_all(bind=engine)


def get_application():
    application = FastAPI()
    application.include_router(api_router, prefix='/api')
    add_pagination(application)
    return application


app = get_application()


@app.on_event("startup")
def init():
    core.global_variables.init()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=int(os.getenv('PORT')), host="0.0.0.0", reload=True, workers=1)


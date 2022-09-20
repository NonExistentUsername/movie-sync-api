from fastapi import FastAPI
from handlers import router

from db.session import engine
from db.base_class import Base
from fastapi_pagination import add_pagination


Base.metadata.create_all(bind=engine)


def get_application():
    application = FastAPI()
    application.include_router(router)
    add_pagination(application)
    return application


app = get_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)

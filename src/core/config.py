import os

DEBUG = os.getenv("DEBUG") == "True"

BASE_DIR = str(os.getenv("BASE_DIR"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(str(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
JWT_SECRET = str(os.getenv("JWT_SECRET"))


def get_jwt_algorithm() -> str:
    return "HS256"


def get_postgres_uri() -> str:
    POSTGRES_DB = str(os.getenv("POSTGRES_DB"))
    POSTGRES_USER = str(os.getenv("POSTGRES_USER"))
    POSTGRES_PASSWORD = str(os.getenv("POSTGRES_PASSWORD"))

    POSTGRES_URI_TEMPLATE = "postgresql+asyncpg://{username}:{password}@db:5432/{database}"

    return POSTGRES_URI_TEMPLATE.format(
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB,
    )

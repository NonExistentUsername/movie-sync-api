from starlette.config import Config

DEBUG = False

config = None

if DEBUG:
    config = Config(".env")

    MYSQL_USER = config("MYSQL_USER", cast=str, default="")
    MYSQL_PASSWORD = config("MYSQL_PASSWORD", cast=str, default="")
    MYSQL_SERVER = config("MYSQL_SERVER", cast=str, default="")
    MYSQL_PORT = config("MYSQL_PORT", cast=str, default="")
    MYSQL_DB = config("MYSQL_DB", cast=str, default="")

    DATABASE_URL = "sqlite:///./sql_app.db"

    BASE_DIR = config("BASE_DIR", cast=str, default="")
    ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=1)
    JWT_SECRET = config("JWT_SECRET", cast=str, default="")
    JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="")
else:
    import os

    MYSQL_USER = str(os.getenv("MYSQL_USER"))
    MYSQL_PASSWORD = str(os.getenv("MYSQL_PASSWORD"))
    MYSQL_SERVER = str(os.getenv("MYSQL_SERVER"))
    MYSQL_PORT = str(os.getenv("MYSQL_PORT"))
    MYSQL_DB = str(os.getenv("MYSQL_DB"))

    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
    
    BASE_DIR = str(os.getenv("BASE_DIR"))
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    JWT_SECRET = str(os.getenv("JWT_SECRET"))
    JWT_ALGORITHM = str(os.getenv("JWT_ALGORITHM"))

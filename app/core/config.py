from starlette.config import Config

DEBUG = True

config = None

if DEBUG:
    config = Config(".env")
else:
    config = Config("/etc/secrets/.env")

MYSQL_USER = config("MYSQL_USER", cast=str, default="")
MYSQL_PASSWORD = config("MYSQL_PASSWORD", cast=str, default="")
MYSQL_SERVER = config("MYSQL_SERVER", cast=str, default="")
MYSQL_PORT = config("MYSQL_PORT", cast=str, default="")
MYSQL_DB = config("MYSQL_DB", cast=str, default="")

if DEBUG:
    DATABASE_URL = "sqlite:///./sql_app.db"
else:
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"

BASE_DIR = config("BASE_DIR", cast=str, default="")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=1)
JWT_SECRET = config("JWT_SECRET", cast=str, default="")
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="")

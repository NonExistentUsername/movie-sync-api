from starlette.config import Config
import os

DEBUG = bool(os.getenv("DEBUG"))
if DEBUG:
    1 / 0

if DEBUG:
    config = Config(".env")

    DATABASE_URL = "sqlite:///./sql_app.db"

    BASE_DIR = config("BASE_DIR", cast=str, default="")
    ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=1)
    JWT_SECRET = config("JWT_SECRET", cast=str, default="")
    JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="")
else:
    import os

    DATABASE_URL = str(os.getenv('DATABASE_URL'))
    # Replace 'postgres' to 'postgresql'
    DATABASE_URL = "postgresql" + DATABASE_URL[8:]
    print(f"used {DATABASE_URL}")
    
    BASE_DIR = str(os.getenv("BASE_DIR"))
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    JWT_SECRET = str(os.getenv("JWT_SECRET"))
    JWT_ALGORITHM = str(os.getenv("JWT_ALGORITHM"))

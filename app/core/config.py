from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=str, default="")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=1)
JWT_SECRET = config("JWT_SECRET", cast=str, default="")
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="")

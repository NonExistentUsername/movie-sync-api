import os

DEBUG = os.getenv("DEBUG") == "True"

BASE_DIR = str(os.getenv("BASE_DIR"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
JWT_SECRET = str(os.getenv("JWT_SECRET"))
JWT_ALGORITHM = str(os.getenv("JWT_ALGORITHM"))
DATABASE_URL = str(os.getenv("DATABASE_URL"))

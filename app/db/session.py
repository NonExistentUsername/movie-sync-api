from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import core.config

SQLALCHEMY_DATABASE_URI = core.config.DATABASE_URL

connect_args = {}

if core.config.DEBUG:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args=connect_args,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import core.config

SQLALCHEMY_DATABASE_URI = core.config.DATABASE_URL

connect_args = {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args=connect_args,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import core.config

POSTGRES_URI_TEMPLATE = "postgresql+asyncpg://{username}:{password}@db:5432/{database}"

SQLALCHEMY_DATABASE_URI = POSTGRES_URI_TEMPLATE.format(
    username=core.config.POSTGRES_USER,
    password=core.config.POSTGRES_PASSWORD,
    database=core.config.POSTGRES_DB,
)

connect_args = {}

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=True,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False, class_=AsyncSession)

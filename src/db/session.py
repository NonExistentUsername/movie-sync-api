from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import core.config

SQLALCHEMY_DATABASE_URI = core.config.get_postgres_uri()


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={},
    pool_pre_ping=True,
    echo=True,
)


SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False, class_=AsyncSession
)

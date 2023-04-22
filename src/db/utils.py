from db.base_class import Base
from db.session import engine
from models.associations import *
from models.room import *


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import dotenv_values

env = dotenv_values(".env")

async_engine = create_async_engine(env.get("DB_URL"), echo=False)
Base = declarative_base()
DBSession = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def init_models(): 
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
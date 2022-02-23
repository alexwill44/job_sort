from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import dotenv_values

env = dotenv_values(".env")

engine = create_engine(env.get("DB_SYNC_URL"))
async_engine = create_async_engine(env.get("DB_URL"), echo=True,)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, class_=AsyncSession, bind=async_engine)
BaseModel = declarative_base()
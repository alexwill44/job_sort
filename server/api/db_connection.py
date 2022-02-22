from sqlalchemy.ext.asyncio import create_async_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import dotenv_values

env = dotenv_values(".env")

async_engine = create_async_engine(env.get("DB_URL"), echo=True,)
SessionLocal = sessionmaker(async_engine)
Base = declarative_base()
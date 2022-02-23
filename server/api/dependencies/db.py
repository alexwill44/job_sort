from typing import AsyncGenerator
from api.db_connection import DBSession

async def get_db() -> AsyncGenerator: 
    async with DBSession() as db:
        yield db
    
from sqlalchemy.ext.asyncio import AsyncSession
from api.db_connection import DBSession

async def get_db() -> AsyncSession:
    async with DBSession() as session:
        yield session

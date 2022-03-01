from api.models import Job
from distutils.log import error
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

class JobCrud:
    
    CACHE = {}
    
    @classmethod
    async def get_by_id(
        cls,
        db: AsyncSession,
        id: int
    ) : 
        global CACHE
        try: 
            async with db as session:
                result = await session.execute(select(Job).where(Job.id == id))
                CACHE = {i.id: i.title for i in result.scalars()}
                return CACHE
        except: 
            print(error)

    @classmethod
    async def get_all_jobs(
        cls,
        db: AsyncSession,
    ) : 
        global CACHE
        try: 
            async with db as session:
                result = await session.execute(select(Job))
                CACHE = {i.id: i.title for i in result.scalars()}
                return CACHE
        except: 
            print(error)

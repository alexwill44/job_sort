import asyncio
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies.db import get_db
from api.models import Job
from api.db_connection import DBSession

async def seed(db):
    print("-- Planting Data -- ")
    for i in range(5):
        #create test dummy data for job listings
        job = Job(
            date_found = f"{date.today()}",
            company = f"{i}xyz.corp",
            title = f"{i} Software Dev",
            location = f"{i} City, CA",
            remote = "",
            link = f"www.{i}{i}{i}{i}{i}{i}.com",
        )    
        try:
            async with db() as session:
                async with session.begin():
                    session.add(job)
            print(job.title)
        except Exception as err:
            print(err)

if __name__ == "__main__":
    asyncio.run(seed(DBSession))
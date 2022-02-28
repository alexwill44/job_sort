from datetime import datetime
from distutils.log import error
from typing import List
from sqlalchemy import select 
import asyncio
from api.schemas.jobs import JobResponse
from fastapi import APIRouter, HTTPException, status, Depends
from api import schemas
from api.crud import JobCrud
from api.dependencies.db import get_db
from api.models import Job
from sqlalchemy.ext.asyncio import AsyncSession 


router = APIRouter(prefix="/app", tags=["jobs"])

@router.get("/alljobs")
async def get_jobs(db: AsyncSession = Depends(get_db)
) -> List[Job]:
    start = datetime.now()
    jobs = await JobCrud.get_all_jobs(db)
    finish = datetime.now()
    return jobs, finish - start
   
@router.get("/ajob")
async def get_job_by_id(id: int, db: AsyncSession = Depends(get_db)
) -> Job:
    start = datetime.now()
    job = await JobCrud.get_by_id(db, id)
    finish = datetime.now()
    return job, finish - start

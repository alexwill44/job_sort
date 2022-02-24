from typing import List
from api.schemas.jobs import JobResponse
from fastapi import APIRouter, HTTPException, status, Depends
from api import schemas
from api.crud import JobCrud
from api.dependencies.db import get_db
from api.models import Job
from sqlalchemy.ext.asyncio import AsyncSession 


router = APIRouter(prefix="/app", tags=["jobs"])

@router.get("/alljobs", response_model=JobResponse)
async def get_all_jobs( db: AsyncSession = Depends(get_db)
) -> List[Job]:
    jobs = await JobCrud.get_all_jobs(db)
    return {"jobs":jobs.scalars().all()}

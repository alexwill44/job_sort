from datetime import datetime
from typing import List

from pydantic import BaseModel

class Job(BaseModel):
    id : int
    date_found : str
    company : str
    title : str
    location : str
    remote : str
    link : str
    source : str
    submitted_by : str
    notes  : str
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode : True

class JobCreate(BaseModel): 
    date_found : str
    company : str
    title : str
    location : str
    remote : str
    link : str
    source : str
    submitted_by : str
    notes  : str

class JobResponse(BaseModel): 
    jobs: List[Job]
    
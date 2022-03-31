from datetime import date, datetime
from ssl import create_default_context

from pydantic import BaseModel

class ImportFile(BaseModel):
    id : int
    total_rows : int
    created_at : datetime
    updated_at : datetime

    class Config: 
        orm_mode=True

class ImportFileCreate(BaseModel):
    total_rows : int

class CreateImportFileResponse(BaseModel):
    message : str
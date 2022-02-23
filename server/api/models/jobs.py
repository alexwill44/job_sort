from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, String

from api.db_connection import Base

class Job(Base):
    """Jobs Table"""

    __tablename__ = "jobs"

    id = Column(BigInteger, primary_key=True, autoincrement=True, Unique=True)
    date_found = Column(DateTime, index=True, nullable=False)
    company = Column(String, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    remote = Column(String, index=True, nullable=False, default="Not Indicated")
    linke = Column(String, index=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"{self.company} | {self.title}"
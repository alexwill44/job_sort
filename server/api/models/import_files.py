from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, Integer

from api.db_connection import Base

class ImportFile(Base):
    """ Import File Table """

    __tablename__ = "import_files"

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    total_rows = Column(Integer, index=True, nullable=False)

    jobs = relationship("Job", back_populates="import_file")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"{self.id} | {self.total_rows}"
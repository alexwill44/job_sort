import sys
from typing import List
from sqlalchemy import MetaData
from api.db_connection import Base, engine
from api.models import Job
from sqlalchemy.sql.schema import Table


if __name__ == "__main__":
    args = sys.argv

    if len(args) > 1 and args[1] == "drop_tables":
        drop: List[Table] = [
            Job.__table__,
        ]
        print("-- the end in nigh --")
        for table in drop:
            print(f" say bye to: {table.name}")
        Base.metadata.drop_all(bind=engine, tables=drop)

    print("-- Setting the Tables ; ) --")
    metadata: MetaData = Base.metadata
    metadata.create_all(bind=engine)
    # tables are created in the order they are imported from models/__init__.py
    for table in metadata.tables:
        print(f' : | {table} ')
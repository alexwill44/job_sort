from api.models import ImportFile
from api.schemas import import_file
from sqlalchemy.ext.asyncio import AsyncSession

class ImportFileCrud:
   
    @classmethod
    async def create_import_file(
        cls, 
        data: import_file.ImportFileCreate, 
        db: AsyncSession,
    ) -> ImportFile:
        """ created an import file """
        import_file = ImportFile(**dict(data))
        db.add(import_file)
        await db.commit()
        return import_file
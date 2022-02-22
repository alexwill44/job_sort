from dotenv import dotenv_values
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

env = dotenv_values(".env")

app = FastAPI(
    title="Sort Job Listing - Python (FastAPI)",
    description="Sort Job Listing CSV Files",
    version="0.0.1",
)

@app.exception_handler(StarletteHTTPException)
async def http_exception(_,exc):
    return JSONResponse({"err": exc.detail}, status_code=exc.status_code)

@app.get("/")
async def root():
    return {"message": f'{env.get("TEST")}'}


if __name__ == "__main__":
    import uvicorn 
    from sqlalchemy.ext.asyncio import create_async_engine
    from api.db_connection import Base 

    async_engine = create_async_engine(env.get("DB_URL"), echo=True,)
    Base.metadata.create_all(async_engine)

    uvicorn.run( 
        "main:app", host="0.0.0.0.", reload=True, port=3501,
    )

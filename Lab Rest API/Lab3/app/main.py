from fastapi import FastAPI
from app.api.book_router import router
from app.database import engine, Base
import app.models.book_model # Важливо для створення таблиць

app = FastAPI(title="Library Cursor API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router)
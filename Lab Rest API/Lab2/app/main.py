from fastapi import FastAPI
from app.api.book_router import router
from app.database import engine, Base

app = FastAPI(title="Library Pro API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router)

@app.get("/")
async def root():
    return {"status": "API is running", "docs": "/docs"}
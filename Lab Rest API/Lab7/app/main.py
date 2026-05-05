from fastapi import FastAPI
from app.api.book_router import router as book_router

app = FastAPI(title="Rate Limiter API")

app.include_router(book_router)
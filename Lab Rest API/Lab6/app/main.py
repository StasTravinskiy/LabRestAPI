from fastapi import FastAPI
import uvicorn
from app.api.auth_router import router as auth_router
from app.api.book_router import router as book_router

app = FastAPI(title="Secure Library API", version="1.0")

app.include_router(auth_router)
app.include_router(book_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
from fastapi import FastAPI
import uvicorn
from app.api.book_router import router

app = FastAPI(title="Library API with MongoDB")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to Mongo Library API!", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
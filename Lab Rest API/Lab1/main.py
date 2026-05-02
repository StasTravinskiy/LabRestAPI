import uvicorn
from fastapi import FastAPI
from api.book_router import router

app = FastAPI(
    title="Library Management API",
    description="Асинхронне API для керування каталогом книг",
    version="1.0.0"
)

# Підключаємо роутер
app.include_router(router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Вітаємо у Library API!",
        "instructions": "Перейдіть на /docs для тестування",
        "docs_url": "http://127.0.0.1:8000/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_and_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Тест створення
        payload = {
            "title": "Kobzar",
            "author": "Shevchenko",
            "description": "Poems",
            "year": 1840,
            "status": "наявна в бібліотеці"
        }
        response = await ac.post("/books/", json=payload)
        assert response.status_code == 201
        book_id = response.json()["id"]

        # Тест отримання всіх
        response = await ac.get("/books/")
        assert response.status_code == 200
        assert len(response.json()) > 0

        # Тест видалення
        response = await ac.delete(f"/books/{book_id}")
        assert response.status_code == 204

        # Тест ідемпотентності видалення (повторне видалення)
        response = await ac.delete(f"/books/{book_id}")
        assert response.status_code == 204
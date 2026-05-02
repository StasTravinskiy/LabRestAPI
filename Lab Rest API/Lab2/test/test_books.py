import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_workflow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Створення
        new_book = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "year": 2008,
            "status": "наявна в бібліотеці"
        }
        res_post = await ac.post("/books/", json=new_book)
        assert res_post.status_code == 201
        book_id = res_post.json()["id"]

        # 2. Отримання з пагінацією
        res_get = await ac.get("/books/?limit=1&offset=0")
        assert res_get.status_code == 200
        assert len(res_get.json()) == 1

        # 3. Видалення
        res_del = await ac.delete(f"/books/{book_id}")
        assert res_del.status_code == 204
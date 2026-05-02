@pytest.mark.asyncio
async def test_cursor_pagination():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for i in range(3):
            await ac.post("/books/", json={
                "title": f"Book {i}", "author": "Test", "year": 2020 + i, "status": "наявна в бібліотеці"
            })

        res1 = await ac.get("/books/?limit=2")
        data1 = res1.json()
        assert len(data1["items"]) == 2
        assert data1["next_cursor"] is not None

        res2 = await ac.get(f"/books/?limit=2&cursor={data1['next_cursor']}")
        data2 = res2.json()
        assert len(data2["items"]) >= 1
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional

class BookRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.books

    def _map_book(self, book: dict) -> dict:
        if book:
            book["id"] = str(book.pop("_id"))
        return book

    async def get_all(self, limit: int, offset: int) -> List[dict]:
        cursor = self.collection.find().skip(offset).limit(limit)
        books = await cursor.to_list(length=limit)
        return [self._map_book(book) for book in books]

    async def get_by_id(self, book_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(book_id):
            return None
        book = await self.collection.find_one({"_id": ObjectId(book_id)})
        return self._map_book(book)

    async def create(self, book_data: dict) -> dict:
        result = await self.collection.insert_one(book_data)
        created_book = await self.collection.find_one({"_id": result.inserted_id})
        return self._map_book(created_book)

    async def delete(self, book_id: str) -> bool:
        if not ObjectId.is_valid(book_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0
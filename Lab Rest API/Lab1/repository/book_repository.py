from typing import List, Dict, Optional
from uuid import UUID
from models.book_storage import books_db

class BookRepository:
    async def get_all(self) -> List[Dict]:
        return books_db

    async def get_by_id(self, book_id: UUID) -> Optional[Dict]:
        return next((book for book in books_db if book["id"] == book_id), None)

    async def add(self, book_data: Dict) -> Dict:
        books_db.append(book_data)
        return book_data

    async def delete(self, book_id: UUID) -> bool:
        global books_db
        initial_len = len(books_db)
        books_db[:] = [b for b in books_db if b["id"] != book_id]
        return len(books_db) < initial_len
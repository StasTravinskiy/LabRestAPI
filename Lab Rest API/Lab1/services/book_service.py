from uuid import uuid4, UUID
from typing import List, Optional
from repository.book_repository import BookRepository
from schemas.book_schema import BookCreate, BookStatus


class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def list_books(self, status: Optional[BookStatus] = None,
                         author: Optional[str] = None,
                         sort_by: Optional[str] = None) -> List[dict]:
        books = await self.repo.get_all()

        # Фільтрація
        if status:
            books = [b for b in books if b["status"] == status]
        if author:
            books = [b for b in books if author.lower() in b["author"].lower()]

        # Сортування
        if sort_by in ["title", "year"]:
            books = sorted(books, key=lambda x: x[sort_by])

        return books

    async def get_book(self, book_id: UUID):
        return await self.repo.get_by_id(book_id)

    async def create_book(self, book_in: BookCreate):
        book_data = book_in.model_dump()
        book_data["id"] = uuid4()
        return await self.repo.add(book_data)

    async def delete_book(self, book_id: UUID):
        # Ідемпотентне видалення: повертаємо True незалежно від того,
        # чи була книга, щоб API міг повернути 204 No Content
        await self.repo.delete(book_id)
        return True
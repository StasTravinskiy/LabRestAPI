from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.book_repository import BookRepository
from app.schemas.book_schema import BookCreate
from uuid import UUID

class BookService:
    def __init__(self, db: AsyncSession):
        self.repo = BookRepository(db)

    async def fetch_books(self, limit: int, offset: int, status: str, author: str, sort_by: str):
        return await self.repo.get_all(limit, offset, status, author, sort_by)

    async def fetch_book(self, book_id: UUID):
        return await self.repo.get_by_id(book_id)

    async def add_book(self, book_in: BookCreate):
        return await self.repo.create(book_in.model_dump())

    async def remove_book(self, book_id: UUID):
        await self.repo.delete(book_id)
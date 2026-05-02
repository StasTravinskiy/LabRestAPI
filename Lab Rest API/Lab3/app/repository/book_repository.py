from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, asc
from app.models.book_model import BookModel
from uuid import UUID
from typing import Optional


class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_cursor(self, limit: int, cursor: Optional[UUID] = None, status: str = None, author: str = None):
        query = select(BookModel).order_by(asc(BookModel.id))

        if status:
            query = query.where(BookModel.status == status)
        if author:
            query = query.where(BookModel.author.ilike(f"%{author}%"))
        if cursor:
            query = query.where(BookModel.id > cursor)

        query = query.limit(limit + 1)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, data: dict):
        new_book = BookModel(**data)
        self.db.add(new_book)
        await self.db.commit()
        await self.db.refresh(new_book)
        return new_book

    async def delete(self, book_id: UUID):
        await self.db.execute(delete(BookModel).where(BookModel.id == book_id))
        await self.db.commit()
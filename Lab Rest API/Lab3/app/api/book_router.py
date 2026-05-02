from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.book_schema import BookRead, BookCreate, BookCursorResponse, BookStatus
from app.repository.book_repository import BookRepository
from uuid import UUID
from typing import Optional

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=BookCursorResponse)
async def get_books(
        limit: int = Query(10, ge=1),
        cursor: Optional[UUID] = None,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None,
        db: AsyncSession = Depends(get_db)
):
    repo = BookRepository(db)
    books = await repo.get_all_cursor(limit, cursor, status, author)

    next_cursor = None
    if len(books) > limit:
        next_cursor = books[limit - 1].id
        books = books[:limit]

    return {"items": books, "next_cursor": next_cursor}


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, db: AsyncSession = Depends(get_db)):
    repo = BookRepository(db)
    return await repo.create(book_in.model_dump())


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BookRepository(db)
    await repo.delete(book_id)
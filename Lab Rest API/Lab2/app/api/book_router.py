from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.book_schema import BookRead, BookCreate, BookStatus
from app.services.book_service import BookService
from uuid import UUID
from typing import List, Optional

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookRead])
async def get_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = Query(None, pattern="^(title|year)$"),
    db: AsyncSession = Depends(get_db)
):
    service = BookService(db)
    return await service.fetch_books(limit, offset, status, author, sort_by)

@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    book = await service.fetch_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    return await service.add_book(book_in)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    await service.remove_book(book_id)
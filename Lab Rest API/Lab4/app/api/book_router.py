from fastapi import APIRouter, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.book_schema import BookRead, BookCreate
from app.repository.book_repository import BookRepository
from typing import List

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookRead])
async def get_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncIOMotorDatabase = Depends(get_db)  # Прокидаємо БД
):
    repo = BookRepository(db)
    return await repo.get_all(limit, offset)

@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    repo = BookRepository(db)
    book = await repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    repo = BookRepository(db)
    return await repo.create(book_in.model_dump())

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    repo = BookRepository(db)
    deleted = await repo.delete(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
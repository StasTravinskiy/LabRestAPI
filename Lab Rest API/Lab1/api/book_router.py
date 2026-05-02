from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from schemas.book_schema import BookRead, BookCreate, BookStatus
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()

@router.get("/", response_model=List[BookRead])
async def get_books(
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = Query(None, regex="^(title|year)$")
):
    return await service.list_books(status, author, sort_by)

@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: UUID):
    book = await service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreate):
    return await service.create_book(book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    await service.delete_book(book_id)
    return None # DELETE ідемпотентний, завжди 204
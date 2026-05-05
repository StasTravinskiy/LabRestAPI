from fastapi import APIRouter, Depends
from typing import List
import uuid
from app.schemas.book_schema import BookCreate, BookRead
from app.auth.dependencies import get_current_user
from app.db import books_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookRead])
async def get_books(current_user: dict = Depends(get_current_user)):
    return books_db

@router.post("/", response_model=BookRead)
async def add_book(book_in: BookCreate, current_user: dict = Depends(get_current_user)):
    new_book = book_in.model_dump()
    new_book["id"] = uuid.uuid4()
    books_db.append(new_book)
    return new_book
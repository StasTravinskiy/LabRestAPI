from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class BookRead(BookCreate):
    id: UUID
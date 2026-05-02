from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from typing import Optional, List

class BookStatus(str, Enum):
    AVAILABLE = "наявна в бібліотеці"
    ISSUED = "видана комусь"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: Optional[str] = None
    year: int = Field(..., gt=0)
    status: BookStatus = BookStatus.AVAILABLE

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: UUID
    class Config:
        from_attributes = True

class BookCursorResponse(BaseModel):
    items: List[BookRead]
    next_cursor: Optional[UUID] = None
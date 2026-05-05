from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

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
    id: str  

    class Config:
        from_attributes = True
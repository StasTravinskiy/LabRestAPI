import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(index=True)
    author: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="наявна в бібліотеці")
    year: Mapped[int] = mapped_column()
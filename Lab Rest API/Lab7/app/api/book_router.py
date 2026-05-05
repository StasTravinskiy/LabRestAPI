from fastapi import APIRouter, Request, Depends
from app.core.rate_limiter import rate_limit

router = APIRouter(prefix="/books", tags=["Books"])

async def get_optional_user(request: Request) -> str | None:
    token = request.headers.get("Authorization")
    if token == "Bearer secret_token":
        return "user_123"
    return None

@router.get("/")
async def get_books(request: Request, user_id: str | None = Depends(get_optional_user)):
    await rate_limit(request, user_id)
    return {"message": "Success", "data": ["Book 1", "Book 2"]}
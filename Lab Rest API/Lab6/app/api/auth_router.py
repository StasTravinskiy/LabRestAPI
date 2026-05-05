from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from app.schemas.user_schema import UserCreate, UserResponse, Token, TokenRefreshRequest
from app.auth.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.db import users_db, REFRESH_SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    if user_data.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = get_password_hash(user_data.password)
    users_db[user_data.username] = {"username": user_data.username, "password": hashed_pw}
    return {"username": user_data.username}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
async def refresh_token(request: TokenRefreshRequest):
    """Ендпоінт для отримання нового access_token за допомогою refresh_token"""
    credentials_exception = HTTPException(status_code=401, detail="Invalid refresh token")
    try:
        payload = jwt.decode(request.refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in users_db:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    new_access_token = create_access_token(data={"sub": username})
    new_refresh_token = create_refresh_token(data={"sub": username})

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
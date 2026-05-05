from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str
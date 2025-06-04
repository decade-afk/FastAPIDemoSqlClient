from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)

class User(UserBase):
    id: int
    name: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    name: Annotated[str, Field(..., min_length=3, max_length=50, example="John Doe")]
    password: Annotated[str, Field(..., min_length=8, max_length=50, example="strongpassword")]

class User(UserBase):
    id: int
    name: str
    
    class Config:
        from_attributes = True  # 替代旧版 orm_mode=True
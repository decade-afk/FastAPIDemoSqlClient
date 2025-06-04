# from pydantic import BaseModel
# from datetime import datetime

# class UserBase(BaseModel):
#     username: str
#     email: str

# class UserCreate(UserBase):
#     pass

# class User(UserBase):
#     id: int
#     created_at: datetime

#     class Config:
#         orm_mode = True

# class ProductBase(BaseModel):
#     name: str
#     price: float
#     description: str | None = None

# class ProductCreate(ProductBase):
#     pass

# class Product(ProductBase):
#     id: int

#     class Config:
#         orm_mode = True
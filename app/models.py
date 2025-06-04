# from sqlalchemy import Column, Integer, String, Float, Text, TIMESTAMP
# from .database import Base
# from datetime import datetime

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), index=True)
#     email = Column(String(100), unique=True, index=True)
#     created_at = Column(TIMESTAMP, default=datetime.utcnow)

# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), index=True)
#     price = Column(Float)
#     description = Column(Text)
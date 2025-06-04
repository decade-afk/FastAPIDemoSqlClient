# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from . import models, schemas
# from .database import SessionLocal, engine
# from fastapi.responses import JSONResponse
# from .database import get_db

# # 创建所有表结构（生产环境建议使用 Alembic）
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # 健康检查端点
# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}

# # 获取所有用户
# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = db.query(models.User).offset(skip).limit(limit).all()
#     return users

# # 获取单个用户
# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# # 获取所有产品
# @app.get("/products/", response_model=list[schemas.Product])
# def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     products = db.query(models.Product).offset(skip).limit(limit).all()
#     return products


from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://test:testpassword@db/testdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

Base.metadata.create_all(bind=engine)

@app.get("/items/")
async def read_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

@app.post("/items/")
async def create_item(name: str):
    db = SessionLocal()
    db_item = Item(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return {"name": db_item.name, "id": db_item.id}  
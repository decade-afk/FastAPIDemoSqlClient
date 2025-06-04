from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from .dependencies import get_current_user
from datetime import datetime
import os

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI with MySQL (Python 3.12)",
    description="Dockerized FastAPI application with MySQL database",
    version="1.0.0"
)

# 启动时间
startup_time = datetime.now()

api_router = APIRouter()

@api_router.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "python_version": os.sys.version,
        "startup_time": startup_time.isoformat()
    }

@api_router.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(crud.get_db)):
    return crud.create_user(db, user)

@api_router.get("/users/", response_model=list[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(crud.get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@api_router.get("/users/me", response_model=schemas.User, tags=["Users"])
def read_current_user(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@api_router.post("/token", tags=["Authentication"])
def login_for_access_token(form_data: schemas.TokenRequest):
    return crud.authenticate_user(form_data.username, form_data.password)

# 项目相关端点
item_router = APIRouter()

@item_router.post("/", response_model=schemas.Item, tags=["Items"])
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(crud.get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_item(db, item, current_user.id)

@item_router.get("/", response_model=list[schemas.Item], tags=["Items"])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(crud.get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_items(db, current_user.id, skip=skip, limit=limit)

@item_router.get("/{item_id}", response_model=schemas.Item, tags=["Items"])
def read_item(
    item_id: int,
    db: Session = Depends(crud.get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this item")
    return item

@item_router.put("/{item_id}", response_model=schemas.Item, tags=["Items"])
def update_item(
    item_id: int,
    item: schemas.ItemUpdate,
    db: Session = Depends(crud.get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")
    return crud.update_item(db, item_id, item)

@item_router.delete("/{item_id}", tags=["Items"])
def delete_item(
    item_id: int,
    db: Session = Depends(crud.get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")
    crud.delete_item(db, item_id)
    return {"status": "Item deleted"}

# 包含所有路由
app.include_router(api_router, prefix="")
app.include_router(item_router, prefix="/items")
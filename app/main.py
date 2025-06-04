from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, SessionLocal
from .dependencies import get_db, get_current_active_user, get_admin_user
from datetime import datetime
import os

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI with MySQL Testing",
    description="API with full Pytest test suite",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 启动时间
startup_time = datetime.now()

@app.on_event("startup")
async def startup_event():
    print("Application started successfully")

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "python_version": os.sys.version,
        "startup_time": startup_time.isoformat()
    }

@app.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/me", response_model=schemas.User, tags=["Users"])
def read_current_user(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

@app.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(form_data: schemas.TokenRequest, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建伪令牌 - 在实际项目中应生成真实的JWT
    access_token = user.email  # 使用邮箱作为令牌进行简化
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/admin/items/", response_model=schemas.Item, tags=["Admin"])
def create_admin_item(
    item: schemas.ItemCreate, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_admin_user)
):
    return crud.create_item(db, item, admin.id)
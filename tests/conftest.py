import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
import os

# 使用测试数据库
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://test_user:test_password@localhost:3306/test_db")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 每次测试前创建所有表
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# 替换应用的数据库依赖
app.dependency_overrides[get_db] = override_get_db

# 创建测试客户端
@pytest.fixture
def client():
    client = TestClient(app)
    yield client
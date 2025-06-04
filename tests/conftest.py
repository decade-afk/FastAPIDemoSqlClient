import sys
from pathlib import Path

# 将项目根目录添加到 sys.path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base
from app.dependencies import get_db as original_get_db, get_current_active_user, get_admin_user
from app.crud import create_user
from app.schemas import UserCreate, ItemCreate

# 测试数据库连接
TEST_DATABASE_URL = "mysql+pymysql://testuser:testpass@localhost:3307/fastapi_test"

# 创建测试引擎和会话
engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建测试数据库表
@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# 覆盖依赖项 - 为每个测试创建一个独立的事务
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

# 覆盖应用依赖
@pytest.fixture(scope="function")
def test_app(db_session):
    # 覆盖数据库依赖
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # 由外部的db_session fixture处理关闭
    
    app.dependency_overrides[original_get_db] = override_get_db
    
    # 覆盖认证依赖
    def override_get_current_active_user():
        # 创建测试用户
        test_user_data = UserCreate(
            name="Test User", 
            email="test@example.com", 
            password="password"
        )
        test_user = create_user(db_session, test_user_data)
        return test_user
    
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    
    # 覆盖管理员依赖
    def override_get_admin_user():
        # 创建管理员用户
        admin_data = UserCreate(
            name="Admin User", 
            email="admin@example.com", 
            password="adminpassword"
        )
        admin_user = create_user(db_session, admin_data)
        admin_user.is_admin = True
        db_session.commit()
        return admin_user
    
    app.dependency_overrides[get_admin_user] = override_get_admin_user
    
    return app

# 测试客户端
@pytest.fixture(scope="function")
def client(test_app):
    with TestClient(test_app) as test_client:
        yield test_client

# 创建测试数据
@pytest.fixture(scope="function")
def create_test_data(db_session):
    # 创建普通用户
    user_data = UserCreate(
        name="Regular User", 
        email="regular@example.com", 
        password="regularpass"
    )
    regular_user = create_user(db_session, user_data)
    
    # 创建项目
    items = []
    for i in range(5):
        item_data = ItemCreate(
            title=f"Test Item {i}",
            description=f"Description for test item {i}"
        )
        item = create_item(db_session, item_data, regular_user.id)
        items.append(item)
    
    return {"regular_user": regular_user, "items": items}
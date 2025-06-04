import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from app.dependencies import get_current_user
from app.crud import create_user, get_user_by_email
from app.schemas import UserCreate

# 覆盖依赖项 - 创建测试数据库会话
@pytest.fixture(scope="session")
def test_engine():
    return create_engine(
        "mysql+pymysql://testuser:testpass@127.0.0.1:3307/fastapi_test",
        pool_size=5,
        max_overflow=10,
        pool_recycle=300
    )

# 在每个测试函数前创建一个新的事务，测试后回滚
@pytest.fixture(scope="function")
def test_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=connection
    )
    session = SessionLocal()
    
    # 创建所有表
    Base.metadata.create_all(bind=connection)
    
    yield session
    
    # 清理
    session.close()
    transaction.rollback()
    connection.close()

# 覆盖依赖注入
@pytest.fixture(scope="function")
def override_db(test_session):
    def _override_get_db():
        try:
            yield test_session
        finally:
            test_session.rollback()
    
    app.dependency_overrides[get_db] = _override_get_db
    return test_session

# 创建测试客户端
@pytest.fixture(scope="function")
def client(override_db):
    with TestClient(app) as test_client:
        yield test_client

# 创建认证用户
@pytest.fixture(scope="function")
def authenticated_client(client):
    # 创建测试用户
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    user = response.json()
    
    # 登录获取token
    login_data = {
        "username": "test@example.com",
        "password": "securepassword"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # 设置认证头
    headers = {"Authorization": f"Bearer {token}"}
    
    # 模拟认证用户
    def _get_current_user_override():
        return user
    
    app.dependency_overrides[get_current_user] = _get_current_user_override
    
    # 返回带认证头的客户端
    client.headers.update(headers)
    return client

# 创建测试数据
@pytest.fixture(scope="function")
def create_test_data(test_session):
    from app.crud import create_item
    from app.schemas import ItemCreate
    
    # 创建用户
    user_data = UserCreate(name="Data Owner", email="owner@example.com", password="testpass")
    user = create_user(test_session, user_data)
    
    # 创建项目
    items = []
    for i in range(1, 6):
        item_data = ItemCreate(
            title=f"Item {i}",
            description=f"Description for item {i}",
            owner_id=user.id
        )
        items.append(create_item(test_session, item_data))
    
    return {"user": user, "items": items}
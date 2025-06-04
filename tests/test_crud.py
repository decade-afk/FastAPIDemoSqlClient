import pytest
from app.crud import create_user, get_user_by_email, authenticate_user, create_item
from app.schemas import UserCreate, ItemCreate

def test_create_user(db_session):
    user_data = UserCreate(
        name="Test User", 
        email="test_crud@example.com", 
        password="testpassword"
    )
    user = create_user(db_session, user_data)
    assert user.id is not None
    assert user.email == user_data.email
    assert user.name == user_data.name

def test_authenticate_user(db_session):
    # 创建用户
    user_data = UserCreate(
        name="Auth User", 
        email="auth@example.com", 
        password="authpassword"
    )
    create_user(db_session, user_data)
    
    # 测试正确密码
    user = authenticate_user(db_session, "auth@example.com", "authpassword")
    assert user is not None
    assert user.email == "auth@example.com"
    
    # 测试错误密码
    user = authenticate_user(db_session, "auth@example.com", "wrongpassword")
    assert user is None
    
    # 测试不存在的用户
    user = authenticate_user(db_session, "nonexistent@example.com", "password")
    assert user is None

def test_create_item(db_session):
    # 先创建用户
    user_data = UserCreate(
        name="Item Creator", 
        email="creator@example.com", 
        password="createpass"
    )
    user = create_user(db_session, user_data)
    
    # 创建项目
    item_data = ItemCreate(
        title="New Test Item",
        description="Description for new item"
    )
    item = create_item(db_session, item_data, user.id)
    
    assert item.id is not None
    assert item.title == item_data.title
    assert item.owner_id == user.id
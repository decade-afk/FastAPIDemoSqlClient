import pytest
from tests.test_utils import (
    create_random_user,
    create_random_item,
    create_test_token,
    get_auth_headers,
    assert_api_response
)

def test_user_registration(client, db_session):
    """测试用户注册流程"""
    # 创建测试用户
    user_data = {
        "name": "New Test User",
        "email": "new.user@example.com",
        "password": "SecurePassword123!"
    }
    
    # 发送注册请求
    response = client.post("/users/", json=user_data)
    data = assert_api_response(response, 200, ["id", "name", "email", "is_active"])
    
    # 验证响应数据
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["is_active"] is True
    assert data["is_admin"] is False
    
    # 验证数据库中是否存在该用户
    from app.crud import get_user_by_email
    user_in_db = get_user_by_email(db_session, user_data["email"])
    assert user_in_db is not None
    assert user_in_db.email == user_data["email"]

def test_item_creation(client, db_session):
    """测试创建项目流程"""
    # 创建测试用户
    user = create_random_user(db_session)
    token = create_test_token(user.email)
    headers = get_auth_headers(token)
    
    # 创建项目数据
    item_data = {
        "title": "Test Item",
        "description": "This is a test item created through API"
    }
    
    # 发送创建项目请求
    response = client.post("/items/", json=item_data, headers=headers)
    data = assert_api_response(response, 200, ["id", "title", "owner_id", "created_at"])
    
    # 验证响应数据
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert data["owner_id"] == user.id
    
    # 验证数据库中是否存在该项目
    from app.crud import get_item
    item_in_db = get_item(db_session, data["id"])
    assert item_in_db is not None
    assert item_in_db.title == item_data["title"]

@pytest.mark.parametrize("endpoint", [
    ("/items/"),
    ("/users/me")
])
def test_authentication_required(endpoint, client):
    """测试需要认证的端点"""
    # 不提供令牌访问
    response = client.get(endpoint)
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers
    assert "detail" in response.json()
    
    # 提供无效令牌访问
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = client.get(endpoint, headers=invalid_headers)
    assert response.status_code == 401

def test_admin_access(client, db_session):
    """测试管理员权限验证"""
    # 创建普通用户
    regular_user = create_random_user(db_session)
    regular_token = create_test_token(regular_user.email)
    regular_headers = get_auth_headers(regular_token)
    
    # 普通用户访问管理员端点
    response = client.post("/admin/items/", json={"title": "Test"}, headers=regular_headers)
    assert response.status_code == 403
    
    # 创建管理员用户
    admin_user = create_random_user(db_session, is_admin=True)
    admin_token = create_test_token(admin_user.email)
    admin_headers = get_auth_headers(admin_token)
    
    # 管理员访问管理员端点
    response = client.post("/admin/items/", json={"title": "Admin Item"}, headers=admin_headers)
    assert response.status_code == 200
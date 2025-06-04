import pytest
from app.schemas import UserCreate, ItemCreate

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "python_version" in data
    assert "startup_time" in data

def test_create_user(client):
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secret"
    }
    response = client.post("/users/", json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "john@example.com"
    assert data["name"] == "John Doe"
    assert "id" in data
    assert "created_at" in data
    
    # 尝试创建重复用户
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_create_item(authenticated_client):
    item_data = {
        "title": "New Item",
        "description": "Item description"
    }
    response = authenticated_client.post("/items/", json=item_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Item"
    assert data["description"] == "Item description"
    assert "id" in data
    assert "owner_id" in data
    assert "created_at" in data

def test_get_items(authenticated_client, create_test_data):
    response = authenticated_client.get("/items/")
    
    assert response.status_code == 200
    data = response.json()
    
    # 验证数据创建是否成功
    assert len(data) == 5
    assert data[0]["title"] == "Item 1"
    assert data[4]["title"] == "Item 5"
    
    # 验证分页
    response = authenticated_client.get("/items/?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Item 3"
    assert data[1]["title"] == "Item 4"

def test_update_item(authenticated_client, create_test_data):
    item = create_test_data["items"][0]
    
    update_data = {
        "title": "Updated Title",
        "description": "Updated description"
    }
    
    response = authenticated_client.put(f"/items/{item.id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"
    
    # 验证数据库中的实际更新
    response = authenticated_client.get(f"/items/{item.id}")
    assert response.json()["title"] == "Updated Title"

def test_delete_item(authenticated_client, create_test_data):
    item = create_test_data["items"][0]
    
    # 删除项目
    response = authenticated_client.delete(f"/items/{item.id}")
    assert response.status_code == 200
    assert response.json() == {"status": "Item deleted"}
    
    # 验证项目已被删除
    response = authenticated_client.get(f"/items/{item.id}")
    assert response.status_code == 404
    
    # 尝试删除不存在项目
    response = authenticated_client.delete("/items/9999")
    assert response.status_code == 404

def test_unauthenticated_access(client):
    # 未认证用户尝试访问受保护端点
    response = client.get("/items/")
    assert response.status_code == 401
    
    # 尝试创建项目
    response = client.post("/items/", json={"title": "Test", "description": "Test"})
    assert response.status_code == 401

def test_invalid_token(authenticated_client):
    # 使用无效token
    authenticated_client.headers["Authorization"] = "Bearer invalidtoken"
    
    response = authenticated_client.get("/items/")
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]
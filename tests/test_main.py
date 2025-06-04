def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0  # 确保有测试数据

def test_read_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "alice"

def test_read_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_product(client):
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"
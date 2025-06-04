# def test_read_users(client):
#     response = client.get("/users/")
#     assert response.status_code == 200
#     assert len(response.json()) > 0  # 确保有测试数据

# def test_read_user(client):
#     response = client.get("/users/1")
#     assert response.status_code == 200
#     assert response.json()["username"] == "alice"

# def test_read_products(client):
#     response = client.get("/products/")
#     assert response.status_code == 200
#     assert len(response.json()) > 0

# def test_read_product(client):
#     response = client.get("/products/1")
#     assert response.status_code == 200
#     assert response.json()["name"] == "Laptop"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, Base, SessionLocal

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://test:testpassword@localhost:3306/testdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[SessionLocal] = override_get_db

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"name": "Test Item"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) > 0  
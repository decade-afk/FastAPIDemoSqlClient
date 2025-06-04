import os
import mysql.connector
import pytest
from httpx import AsyncClient
from app.main import app

# 测试环境变量
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "testuser"),
    "password": os.getenv("MYSQL_PASSWORD", "testpass"),
    "database": os.getenv("MYSQL_DATABASE", "testdb"),
    "port": os.getenv("MYSQL_PORT", 3306)
}

@pytest.mark.asyncio
async def test_read_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 先插入测试数据
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name) VALUES ('Test Item')")
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # 测试API
        response = await client.get(f"/items/{item_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Test Item"
        
        # 清理测试数据
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM items WHERE id = {item_id}")
        conn.commit()
        conn.close()

@pytest.mark.asyncio
async def test_item_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/items/9999")
        assert response.status_code == 404
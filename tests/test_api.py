import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
root_path = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(root_path))

import os
import mysql.connector
from fastapi.testclient import TestClient
from app.main import app

# 测试环境变量
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "testuser"),
    "password": os.getenv("MYSQL_PASSWORD", "testpass"),
    "database": os.getenv("MYSQL_DATABASE", "testdb"),
    "port": int(os.getenv("MYSQL_PORT", "3306"))  # 确保端口是整数
}

# 创建测试客户端
client = TestClient(app)

def test_read_item():
    # 先插入测试数据
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 创建测试表（如果不存在）
    cursor.execute("CREATE TABLE IF NOT EXISTS items (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NOT NULL)")
    
    # 插入测试数据
    cursor.execute("INSERT INTO items (name) VALUES ('Test Item')")
    item_id = cursor.lastrowid
    conn.commit()
    
    try:
        # 测试API
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Test Item"
    finally:
        # 清理测试数据
        cursor.execute(f"DELETE FROM items WHERE id = {item_id}")
        conn.commit()
        conn.close()

def test_item_not_found():
    response = client.get("/items/9999")
    assert response.status_code == 404
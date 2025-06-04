import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
root_path = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(root_path))
import os
import mysql.connector
import pytest
from fastapi.testclient import TestClient
from app.main import app

# 测试环境变量
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "testuser"),
    "password": os.getenv("MYSQL_PASSWORD", "testpass"),
    "database": os.getenv("MYSQL_DATABASE", "testdb"),
    "port": int(os.getenv("MYSQL_PORT", "3306"))
}

# 创建测试客户端
client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_test_data():
    """在所有测试前后清理测试数据"""
    # 测试前清空items表并插入基础数据
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS items")
    cursor.execute("""
        CREATE TABLE items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        )
    """)
    cursor.execute("INSERT INTO items (name) VALUES ('Test Item 1'), ('Test Item 2')")
    conn.commit()
    conn.close()
    
    yield  # 执行测试
    
    # 测试后清空items表
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE items")
    conn.commit()
    conn.close()

def test_read_item():
    # 获取第一个项目的ID
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM items LIMIT 1")
    item_id = cursor.fetchone()[0]
    conn.close()
    
    # 测试API
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] is not None

def test_item_not_found():
    # 使用非常大的ID确保不存在
    response = client.get("/items/9999999")
    assert response.status_code == 404
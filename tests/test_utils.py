import random
import string
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app import crud
from app.schemas import UserCreate, ItemCreate

def random_string(length: int = 10) -> str:
    """生成随机字符串"""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def random_email(domain: str = "example.com") -> str:
    """生成随机邮箱地址"""
    return f"{random_string(8)}.{random_string(4)}@{domain}"

def random_password() -> str:
    """生成随机密码"""
    return f"Passw0rd!{random_string(4)}"

def create_random_user(db: Session, is_admin: bool = False) -> crud.User:
    """创建随机测试用户"""
    user_data = UserCreate(
        name=f"Test User {random_string(5)}",
        email=random_email(),
        password=random_password()
    )
    user = crud.create_user(db, user_data)
    if is_admin:
        user.is_admin = True
        db.commit()
        db.refresh(user)
    return user

def create_random_item(db: Session, owner_id: int) -> crud.Item:
    """创建随机测试项目"""
    item_data = ItemCreate(
        title=f"Test Item {uuid.uuid4().hex[:6]}",
        description=f"Description for test item {datetime.now().strftime('%H:%M:%S')}"
    )
    return crud.create_item(db, item_data, owner_id)

def create_test_token(user_email: str) -> str:
    """创建测试令牌（模拟认证）"""
    # 在测试环境中，我们使用邮箱作为令牌进行简化
    return user_email

def get_auth_headers(token: str) -> dict:
    """获取认证头信息"""
    return {"Authorization": f"Bearer {token}"}

def assert_api_response(response, expected_status: int, expected_keys: list):
    """验证API响应基本格式"""
    assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
    data = response.json()
    for key in expected_keys:
        assert key in data, f"Missing key: {key} in response"
    return data
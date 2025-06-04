import random
import string

def random_string(length=10):
    """生成随机字符串"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def random_email():
    """生成随机邮箱地址"""
    return f"{random_string(8)}@{random_string(5)}.com"

def create_random_user(session):
    """创建随机测试用户"""
    from app.crud import create_user
    from app.schemas import UserCreate
    
    user_data = UserCreate(
        name=f"Test User {random_string(5)}",
        email=random_email(),
        password="password"
    )
    return create_user(session, user_data)

def create_random_item(session, user_id):
    """创建随机测试项目"""
    from app.crud import create_item
    from app.schemas import ItemCreate
    
    item_data = ItemCreate(
        title=f"Item {random_string(6)}",
        description=f"Description for item {random_string(12)}",
        owner_id=user_id
    )
    return create_item(session, item_data)
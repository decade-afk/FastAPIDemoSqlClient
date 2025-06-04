# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os

# # 从环境变量获取数据库连接信息
# DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://test_user:test_password@localhost:3306/test_db")

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# # 数据库依赖函数
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


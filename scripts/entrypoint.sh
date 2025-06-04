#!/bin/bash
set -e

# chmod +x scripts/entrypoint.sh

# 启动MySQL服务
service mysql start

# 执行数据库初始化
mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';"
mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};"
mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';"
mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "FLUSH PRIVILEGES;"

# 初始化数据库表
mysql -u root -p${MYSQL_ROOT_PASSWORD} ${MYSQL_DATABASE} < /app/scripts/init.sql

# 启动FastAPI服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
# 保持容器运行，等待后台进程
wait
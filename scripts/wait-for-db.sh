#!/bin/bash
# 等待MySQL数据库准备就绪的脚本
# 参数:
#   $1: 数据库主机名
#   $2: 用户名
#   $3: 密码
#   $4: 数据库名（可选）
#   $@: 要执行的命令

set -e

HOST="$1"
USER="$2"
PASS="$3"
DBNAME="$4"
shift 4
COMMAND="$@"

if [ -z "$HOST" ] || [ -z "$USER" ] || [ -z "$PASS" ]; then
  echo "Usage: wait-for-db.sh <host> <user> <pass> [dbname] <command>"
  exit 1
fi

echo "Waiting for MySQL at $HOST to accept connections..."

# 最多尝试30次，每次等待2秒
MAX_RETRIES=30
WAIT_SECONDS=2
attempt=1

until mysqladmin ping -h "$HOST" -u "$USER" -p"$PASS" --silent; do
  if [ $attempt -ge $MAX_RETRIES ]; then
    echo "Error: MySQL not available after $MAX_RETRIES attempts" >&2
    exit 1
  fi
  
  echo "MySQL unavailable ($attempt/$MAX_RETRIES) - retrying in $WAIT_SECONDS seconds..."
  sleep $WAIT_SECONDS
  attempt=$((attempt+1))
done

# 如果指定了数据库名，检查数据库是否存在
if [ -n "$DBNAME" ]; then
  until echo "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '$DBNAME'" | \
        mysql -h "$HOST" -u "$USER" -p"$PASS" -s -N | grep -q "$DBNAME"; do
    if [ $attempt -ge $MAX_RETRIES ]; then
      echo "Error: Database $DBNAME not created after $MAX_RETRIES attempts" >&2
      exit 1
    fi
    
    echo "Database $DBNAME not created yet ($attempt/$MAX_RETRIES) - retrying in $WAIT_SECONDS seconds..."
    sleep $WAIT_SECONDS
    attempt=$((attempt+1))
  done
  echo "Database $DBNAME is ready!"
fi

echo "MySQL is up - executing command: $COMMAND"
exec $COMMAND
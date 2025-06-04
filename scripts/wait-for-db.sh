#!/bin/bash
# 等待MySQL数据库准备就绪 - Python 3.12优化版
set -euo pipefail

host="$1"
shift
cmd="$@"

attempt=1
max_attempts=30

until mysqladmin ping -h "$host" -u "user" -p"password" --silent; do
  if [ $attempt -ge $max_attempts ]; then
    echo "Error: MySQL not available after $max_attempts attempts" >&2
    exit 1
  fi
  
  echo "MySQL unavailable ($attempt/$max_attempts) - retrying in 2 seconds..."
  sleep 2
  attempt=$((attempt+1))
done

echo "MySQL is up - executing: $cmd"
exec $cmd
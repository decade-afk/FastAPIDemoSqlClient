FROM python:3.12-slim

LABEL maintainer="Your Name"

# 安装MySQL客户端和系统依赖
RUN apt-get update && \
    apt-get install -y default-mysql-client curl && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . /app

# 确保脚本可执行
RUN chmod +x scripts/wait-for-db.sh

# 暴露应用端口
EXPOSE 80

# 设置测试环境变量
ENV PYTHONPATH=/app

# 启动命令（开发模式）
CMD ["./scripts/wait-for-db.sh", "db", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

# 测试命令（在docker-compose.test.yml中使用）
CMD ["pytest", "-v", "tests/"]
FROM python:3.12

# 安装MySQL客户端
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制Python依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app ./app
COPY scripts ./scripts

# 为entrypoint.sh添加可执行权限
RUN chmod +x /app/scripts/entrypoint.sh

# 环境变量
ENV MYSQL_ROOT_PASSWORD=rootpass
ENV MYSQL_USER=testuser
ENV MYSQL_PASSWORD=testpass
ENV MYSQL_DATABASE=testdb

# 暴露端口
EXPOSE 8000 3306

# 设置入口点
CMD ["/app/scripts/entrypoint.sh"]
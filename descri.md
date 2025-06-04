### **使用说明**

1. **本地开发**：
   ```bash
   # 启动服务
   docker-compose up -d

   # 查看日志
   docker-compose logs -f

   # 访问 API
   http://localhost:8000/docs  # Swagger UI
   ```

2. **运行测试**：
   ```bash
   # 安装依赖
   pip install -r requirements.txt

   # 运行测试
   pytest tests/ -v
   ```

3. **CI/CD 流程**：
   - 每次推送代码到 `main` 或 `feature/*` 分支时，GitHub Actions 会自动触发
   - 工作流会：
     1. 构建 Docker 镜像
     2. 启动 MySQL 容器并执行最新 SQL 脚本
     3. 启动 FastAPI 容器
     4. 运行测试
     5. 清理资源

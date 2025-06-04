USE test_db;

-- 清空现有数据（确保每次测试都是干净的）
TRUNCATE TABLE users;
TRUNCATE TABLE products;

-- 插入测试用户
INSERT INTO users (username, email) VALUES
('alice', 'alice@example.com'),
('bob', 'bob@example.com'),
('charlie', 'charlie@example.com');

-- 插入测试产品
INSERT INTO products (name, price, description) VALUES
('Laptop', 999.99, 'High-performance laptop'),
('Mouse', 29.99, 'Wireless optical mouse'),
('Keyboard', 59.99, 'Mechanical keyboard');
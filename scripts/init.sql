-- 创建数据库
CREATE DATABASE IF NOT EXISTS `fastapi`;
USE `fastapi`;

-- 创建用户表
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL UNIQUE,
  `hashed_password` VARCHAR(100) NOT NULL,
  `is_active` BOOLEAN NOT NULL DEFAULT 1,
  `is_admin` BOOLEAN NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 创建项目表
CREATE TABLE IF NOT EXISTS `items` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `owner_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 插入初始数据（可选）
INSERT INTO `users` (`name`, `email`, `hashed_password`, `is_admin`)
VALUES
  ('Admin User', 'admin@example.com', 'hashed_password_here', 1),
  ('John Doe', 'john.doe@example.com', 'hashed_password_here', 0);

-- 为测试用户创建一些项目
INSERT INTO `items` (`title`, `description`, `owner_id`)
SELECT 'Initial Project', 'Project created during database initialization', id
FROM `users` WHERE `email` = 'admin@example.com';
-- 创建MySQL数据库脚本
-- 连接到MySQL服务器后执行此脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS sports_booking 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE sports_booking;

-- 显示数据库信息
SELECT DATABASE() as 'Current Database';

-- 显示表信息
SHOW TABLES;
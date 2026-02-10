#!/usr/bin/env python3
"""
初始化MySQL数据库脚本
"""

import pymysql
import sys

def create_database():
    """创建数据库"""
    try:
        # 连接到MySQL服务器（不指定数据库）
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            charset='utf8mb4'
        )
        
        cursor = conn.cursor()
        
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS sports_booking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ 数据库 sports_booking 创建成功")
        
        # 切换到数据库
        cursor.execute("USE sports_booking")
        print("✅ 切换到数据库 sports_booking")
        
        # 显示当前数据库
        cursor.execute("SELECT DATABASE() as current_db")
        result = cursor.fetchone()
        print(f"当前数据库: {result[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        return False

def test_connection():
    """测试数据库连接"""
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='sports_booking',
            charset='utf8mb4'
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION() as mysql_version")
        version = cursor.fetchone()
        print(f"✅ MySQL版本: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始初始化MySQL数据库...")
    
    # 创建数据库
    if create_database():
        print("✅ 数据库创建完成")
        
        # 测试连接
        if test_connection():
            print("✅ 数据库连接测试成功")
            print("🎉 MySQL数据库初始化完成！")
        else:
            print("❌ 数据库连接测试失败")
            sys.exit(1)
    else:
        print("❌ 数据库创建失败")
        sys.exit(1)
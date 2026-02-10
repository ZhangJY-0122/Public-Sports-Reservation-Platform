#!/usr/bin/env python3
import sqlite3

try:
    conn = sqlite3.connect('sports_booking.db')
    cursor = conn.cursor()
    
    # 获取所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("数据库中的表:")
    if tables:
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("  数据库中没有表")
    
    conn.close()
    print("数据库检查完成")
    
except Exception as e:
    print(f"错误: {e}")
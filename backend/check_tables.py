#!/usr/bin/env python3
import sqlite3

def check_database_tables():
    try:
        conn = sqlite3.connect('sports_booking.db')
        cursor = conn.cursor()
        
        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("=== 数据库中的表 ===")
        if tables:
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("  数据库中没有表")
        
        # 检查表结构
        for table in tables:
            table_name = table[0]
            print(f"\n=== {table_name} 表结构 ===")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - {'DEFAULT' if col[4] else ''} {col[4] if col[4] else ''}")
        
        conn.close()
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    check_database_tables()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库检查脚本
"""

import sqlite3
import os

def check_database():
    db_path = 'sports_booking.db'
    
    if not os.path.exists(db_path):
        print(f"数据库文件 {db_path} 不存在")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"数据库中的表: {[table[0] for table in tables]}")
    print()
    
    # 检查每个表的结构
    for table in tables:
        table_name = table[0]
        print(f"=== {table_name} 表结构 ===")
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        structure = cursor.fetchone()
        if structure:
            print(structure[0])
        
        # 检查表中的数据
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"数据行数: {count}")
        
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            print(f"数据预览:")
            for i, row in enumerate(rows[:5]):  # 只显示前5行
                print(f"  行{i+1}: {row}")
        print()
    
    conn.close()

if __name__ == "__main__":
    check_database()
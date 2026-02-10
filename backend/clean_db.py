#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理数据库冲突
"""

import sqlite3
import os

def clean_database():
    """清理数据库冲突"""
    try:
        # 查找数据库文件
        db_files = ['app.db', 'database.db']
        db_file = None
        
        for file in db_files:
            if os.path.exists(file):
                db_file = file
                break
        
        if not db_file:
            print('❌ 找不到数据库文件')
            return False
        
        print(f'🔍 找到数据库文件: {db_file}')
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # 查看所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print('📋 当前数据库中的表:')
        for table in tables:
            print(f'  - {table[0]}')
        
        # 删除冲突的表
        conflict_tables = ['booking_shares', 'booking_shares_old']
        for table_name in conflict_tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f'🗑️ 已删除表: {table_name}')
        
        conn.commit()
        conn.close()
        
        print('✅ 数据库清理完成')
        return True
        
    except Exception as e:
        print(f'❌ 清理失败: {e}')
        return False

if __name__ == '__main__':
    clean_database()
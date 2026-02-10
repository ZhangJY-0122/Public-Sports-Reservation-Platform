#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查MySQL数据库中coach_bookings表结构和数据
"""

import pymysql
import sys
import os
from config import Config

def get_db_config():
    """获取数据库配置"""
    try:
        config = Config()
        uri = config.SQLALCHEMY_DATABASE_URI
        
        print(f"数据库URI: {uri}")
        
        # 解析URI格式: mysql://user:password@host:port/database
        if '://' not in uri:
            print("❌ 数据库URI格式错误")
            return None
            
        protocol, rest = uri.split('://', 1)
        
        if '@' in rest:
            auth_info, host_info = rest.split('@', 1)
            user_pass = auth_info.split(':', 1)
            user = user_pass[0]
            password = user_pass[1] if len(user_pass) > 1 else ''
            
            if '/' in host_info:
                host_port_db = host_info.split('/', 1)
                host_port = host_port_db[0]
                database = host_port_db[1]
                
                if ':' in host_port:
                    host_port_parts = host_port.split(':', 1)
                    host = host_port_parts[0]
                    port = int(host_port_parts[1])
                else:
                    host = host_port
                    port = 3306
            else:
                print("❌ 数据库URI中缺少数据库名")
                return None
        else:
            print("❌ 数据库URI格式错误")
            return None
            
        return {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4'
        }
        
    except Exception as e:
        print(f"❌ 解析数据库配置失败: {e}")
        return None

def check_database():
    """检查数据库"""
    db_config = get_db_config()
    if not db_config:
        return
        
    print("\n=== 数据库连接配置 ===")
    print(f"Host: {db_config['host']}")
    print(f"Port: {db_config['port']}")
    print(f"User: {db_config['user']}")
    print(f"Database: {db_config['database']}")
    print(f"Password: {'*' * len(db_config['password'])}")
    
    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        print("\n✅ 数据库连接成功")
        
        # 检查coach_bookings表结构
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'coach_bookings'
            ORDER BY ORDINAL_POSITION
        """, (db_config['database'],))
        
        columns = cursor.fetchall()
        
        print("\n=== coach_bookings表结构 ===")
        if not columns:
            print("❌ coach_bookings表不存在")
            return
            
        has_venue_id = False
        for col in columns:
            col_name, data_type, is_nullable, default, key = col
            print(f"列名: {col_name:20} | 类型: {data_type:15} | 可空: {is_nullable:3} | 默认值: {default}")
            if col_name == 'venue_id':
                has_venue_id = True
                
        print(f"\n=== venue_id列检查 ===")
        print(f"venue_id列是否存在: {'✅ 是' if has_venue_id else '❌ 否'}")
        
        # 检查当前数据
        cursor.execute("SELECT COUNT(*) FROM coach_bookings")
        count = cursor.fetchone()[0]
        
        print(f"\n=== 当前coach_bookings表数据 ===")
        print(f"总记录数: {count}")
        
        if count > 0:
            # 显示表结构和数据示例
            cursor.execute("DESCRIBE coach_bookings")
            describe_columns = [desc[0] for desc in cursor.fetchall()]
            print(f"表字段: {', '.join(describe_columns)}")
            
            cursor.execute("SELECT * FROM coach_bookings LIMIT 3")
            rows = cursor.fetchall()
            print("\n前3条记录:")
            for i, row in enumerate(rows, 1):
                print(f"记录{i}: {row}")
                
            # 检查venue_id字段的数据情况
            cursor.execute("SELECT venue_id FROM coach_bookings LIMIT 5")
            venue_data = cursor.fetchall()
            print(f"\nvenue_id字段数据示例: {venue_data}")
            
        cursor.close()
        connection.close()
        
    except pymysql.Error as e:
        print(f"\n❌ 数据库操作失败: {e}")
        print("请检查:")
        print("1. MySQL服务是否运行")
        print("2. 数据库连接配置是否正确")
        print("3. 用户权限是否足够")
        print("4. 数据库名是否存在")

if __name__ == "__main__":
    check_database()
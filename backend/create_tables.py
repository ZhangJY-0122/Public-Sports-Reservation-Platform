#!/usr/bin/env python3
"""
使用SQLAlchemy创建MySQL数据库表结构
"""

import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db

def create_all_tables():
    """创建所有数据库表"""
    try:
        # 创建Flask应用
        app = create_app('development')
        
        with app.app_context():
            print("🔄 开始创建数据库表...")
            
            # 创建所有表
            db.create_all()
            
            print("✅ 数据库表创建成功")
            
            # 检查表是否创建成功
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📋 当前数据库中的表 ({len(tables)}个):")
            for table in sorted(tables):
                print(f"  - {table}")
            
            return True
            
    except Exception as e:
        print(f"❌ 创建数据库表失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 开始初始化MySQL数据库表结构...")
    
    if create_all_tables():
        print("🎉 数据库表结构初始化完成！")
    else:
        print("❌ 数据库表结构初始化失败")
        sys.exit(1)
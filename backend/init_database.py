#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建数据库表结构
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append('.')

from app import create_app
from models import db

def init_database():
    """初始化数据库"""
    print("🔧 开始初始化数据库...")
    
    # 创建Flask应用
    app = create_app('development')
    
    with app.app_context():
        try:
            # 创建所有表
            print("📋 创建数据库表...")
            db.create_all()
            print("✅ 数据库表创建成功！")
            
            # 检查表是否创建成功
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 数据库中的表: {tables}")
            
        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
            raise

if __name__ == '__main__':
    init_database()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查费用分摊模型表结构
"""

from models import db, BookingShare, User
from app import create_app
import os

def check_booking_share_table():
    """检查费用分摊表结构"""
    app = create_app()
    with app.app_context():
        try:
            # 检查数据库连接
            print('🔍 检查数据库连接...')
            
            # 查看所有表
            print('📋 数据库中的表:')
            for table in db.engine.table_names():
                print(f'  - {table}')
            
            # 检查booking_shares表是否存在
            tables = db.engine.table_names()
            if 'booking_shares' in tables:
                print('✅ booking_shares表已存在')
                
                # 检查表结构
                from sqlalchemy import text
                result = db.session.execute(text('PRAGMA table_info(booking_shares)'))
                print('📊 booking_shares表结构:')
                for row in result:
                    print(f'  {row.name}: {row.type} - {"NOT NULL" if row.notnull else "NULL"}')
            else:
                print('❌ booking_shares表不存在')
                
                # 尝试创建表
                print('🔧 尝试创建booking_shares表...')
                BookingShare.__table__.create(db.engine, checkfirst=True)
                print('✅ 表创建成功')
            
            # 测试模型实例化
            print('🧪 测试模型实例化...')
            share = BookingShare(
                event_name='测试活动', 
                user_id=1, 
                share_amount=100.50
            )
            
            # 测试to_dict方法
            print('📋 测试to_dict方法...')
            dict_data = share.to_dict()
            print(f'✅ 模型实例化和序列化成功: {dict_data}')
            
            return True
            
        except Exception as e:
            print(f'❌ 测试失败: {e}')
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    check_booking_share_table()
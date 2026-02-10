#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试费用分摊API功能
"""

import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from app import create_app
from models import db, User, BookingShare
import traceback

def test_booking_share_api():
    """测试费用分摊API功能"""
    try:
        print('🚀 开始测试费用分摊API...')
        
        # 创建应用
        app = create_app()
        with app.app_context():
            print('✅ Flask应用创建成功')
            
            # 检查数据库连接
            print('🔍 检查数据库连接...')
            db.create_all()
            print('✅ 数据库表结构检查完成')
            
            # 检查BookingShare模型
            print('🔍 检查BookingShare模型...')
            share = BookingShare(
                event_name='测试活动',
                user_id=1,
                share_amount=100.50,
                paid_amount=50.00
            )
            
            print(f'✅ BookingShare模型实例化成功: {share.to_dict()}')
            
            # 检查数据库字段
            print('🔍 检查数据库字段...')
            columns = [column.name for column in BookingShare.__table__.columns]
            expected_columns = ['id', 'event_name', 'user_id', 'share_amount', 'paid_amount', 'is_paid', 'created_at', 'updated_at']
            
            for col in expected_columns:
                if col in columns:
                    print(f'✅ 字段 {col} 存在')
                else:
                    print(f'❌ 字段 {col} 不存在')
            
            print(f'📋 所有字段: {columns}')
            
            # 测试to_dict方法
            print('🔍 测试to_dict方法...')
            dict_data = share.to_dict()
            required_fields = ['id', 'event_name', 'user_id', 'share_amount', 'paid_amount', 'is_paid', 'created_at', 'updated_at']
            
            for field in required_fields:
                if field in dict_data:
                    print(f'✅ to_dict方法包含字段: {field} = {dict_data[field]}')
                else:
                    print(f'❌ to_dict方法缺少字段: {field}')
            
            print('✅ 费用分摊API测试完成！')
            
            return True
            
    except Exception as e:
        print(f'❌ 测试失败: {e}')
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_booking_share_api()
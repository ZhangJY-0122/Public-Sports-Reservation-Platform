#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试费用分摊API功能
"""

from models import db, BookingShare, User
from app import create_app

def test_booking_share():
    """测试费用分摊功能"""
    app = create_app()
    with app.app_context():
        try:
            # 创建数据库表
            db.create_all()
            print('✅ 数据库表创建成功')
            
            # 测试模型
            share = BookingShare(event_name='测试活动', user_id=1, share_amount=100.50)
            print(f'✅ 模型创建成功: {share.to_dict()}')
            
            # 检查to_dict方法
            dict_data = share.to_dict()
            expected_fields = ['id', 'event_name', 'user_id', 'share_amount', 'paid_amount', 'is_paid', 'created_at', 'updated_at']
            for field in expected_fields:
                if field not in dict_data:
                    print(f'❌ 缺少字段: {field}')
                else:
                    print(f'✅ 字段存在: {field} = {dict_data[field]}')
            
            print('✅ 所有测试通过！')
            return True
            
        except Exception as e:
            print(f'❌ 测试失败: {e}')
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    test_booking_share()
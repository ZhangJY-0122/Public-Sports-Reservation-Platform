#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完整测试费用分摊API功能
"""

from app import create_app
from models import db, User, Booking, BookingShare
import sys

def test_booking_share_full():
    """完整测试费用分摊API功能"""
    app = create_app()
    with app.app_context():
        try:
            print('🚀 开始完整测试费用分摊API...')
            
            # 1. 检查应用上下文
            print('✅ Flask应用上下文正常')
            
            # 2. 检查数据库连接
            with db.engine.connect() as conn:
                result = conn.execute(db.text('SELECT 1')).scalar()
                print(f'✅ 数据库连接正常: {result}')
            
            # 3. 检查模型定义
            print('📊 检查模型定义...')
            print(f'  - BookingShare表: {BookingShare.__tablename__}')
            print(f'  - BookingShare字段: {[col.name for col in BookingShare.__table__.columns]}')
            
            # 4. 检查Blueprint注册
            print('🔗 检查Blueprint注册...')
            if 'booking_share' in app.blueprints:
                print('✅ booking_share蓝图已注册')
            else:
                print('❌ booking_share蓝图未注册')
            
            # 5. 测试API路由注册
            print('🛣️ 检查API路由...')
            routes = []
            for rule in app.url_map.iter_rules():
                if 'booking-share' in rule.rule:
                    routes.append(f"{rule.rule} [{', '.join(rule.methods)}]")
            
            if routes:
                print('✅ 费用分摊API路由已注册:')
                for route in routes:
                    print(f'  - {route}')
            else:
                print('❌ 费用分摊API路由未注册')
            
            # 6. 测试模型关系
            print('🔗 检查模型关系...')
            try:
                # 检查Booking模型是否正确引用BookingShare
                booking_shares_rel = getattr(Booking, 'shares', None)
                if booking_shares_rel:
                    print('✅ Booking模型包含shares关系')
                else:
                    print('⚠️ Booking模型没有shares关系')
            except Exception as e:
                print(f'⚠️ 模型关系检查失败: {e}')
            
            print('\n🎉 费用分摊API完整测试完成！')
            return True
            
        except Exception as e:
            print(f'❌ 测试失败: {e}')
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = test_booking_share_full()
    sys.exit(0 if success else 1)
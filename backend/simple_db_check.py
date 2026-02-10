#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单检查数据库状态
"""

try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from config import DevelopmentConfig
    
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db = SQLAlchemy(app)
    
    print("=== Flask应用和数据库配置初始化成功 ===")
    
    with app.app_context():
        # 检查coach_bookings表是否存在
        from models import CoachBooking
        
        print("\n=== coach_bookings模型信息 ===")
        print(f"表名: {CoachBooking.__tablename__}")
        
        # 检查列信息
        columns = [column.name for column in CoachBooking.__table__.columns]
        print(f"所有列: {', '.join(columns)}")
        
        # 检查venue_id列是否存在
        has_venue_id = 'venue_id' in columns
        print(f"venue_id列是否存在: {'✅ 是' if has_venue_id else '❌ 否'}")
        
        # 检查数据
        count = CoachBooking.query.count()
        print(f"\n=== 数据统计 ===")
        print(f"coach_bookings表总记录数: {count}")
        
        if count > 0:
            # 显示前几条记录
            bookings = CoachBooking.query.limit(3).all()
            print("\n前3条记录:")
            for i, booking in enumerate(bookings, 1):
                print(f"记录{i}: {booking.to_dict()}")
                
            # 检查venue_id字段的数据情况
            venue_ids = [booking.venue_id for booking in CoachBooking.query.limit(5).all()]
            print(f"\nvenue_id字段数据示例: {venue_ids}")
            
            # 统计非空venue_id的数量
            non_null_count = CoachBooking.query.filter(CoachBooking.venue_id.isnot(None)).count()
            print(f"venue_id非空记录数: {non_null_count}")
            
        print("\n=== 检查完成 ===")
        
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保已安装所需依赖")
except Exception as e:
    print(f"❌ 数据库检查失败: {e}")
    import traceback
    traceback.print_exc()
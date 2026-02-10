#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查数据库并启动Flask服务
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数"""
    try:
        # 导入相关模块
        from flask import Flask, jsonify
        from config import DevelopmentConfig
        from models import db, CoachBooking, Venue
        
        print("=== 数据库状态检查 ===")
        
        # 创建Flask应用
        app = Flask(__name__)
        app.config.from_object(DevelopmentConfig)
        db.init_app(app)
        
        with app.app_context():
            # 检查表结构
            columns = [column.name for column in CoachBooking.__table__.columns]
            has_venue_id = 'venue_id' in columns
            
            print(f"✅ 数据库连接成功")
            print(f"coach_bookings表字段: {', '.join(columns)}")
            print(f"venue_id列是否存在: {'✅ 是' if has_venue_id else '❌ 否'}")
            
            # 检查数据
            total_bookings = CoachBooking.query.count()
            bookings_with_venue = CoachBooking.query.filter(CoachBooking.venue_id.isnot(None)).count() if has_venue_id else 0
            
            print(f"总预约记录数: {total_bookings}")
            print(f"包含venue_id的记录数: {bookings_with_venue}")
            print(f"venue_id覆盖率: {(bookings_with_venue/total_bookings*100):.1f}%" if total_bookings > 0 else "0%")
            
            # 检查场馆数据
            total_venues = Venue.query.count()
            print(f"场馆总数: {total_venues}")
            
            # 显示一些示例数据
            if total_bookings > 0:
                print("\n=== 最近3条预约记录 ===")
                recent_bookings = CoachBooking.query.order_by(CoachBooking.created_at.desc()).limit(3).all()
                for i, booking in enumerate(recent_bookings, 1):
                    booking_dict = booking.to_dict()
                    print(f"记录{i}:")
                    print(f"  ID: {booking_dict.get('id')}")
                    print(f"  预约编号: {booking_dict.get('booking_no')}")
                    print(f"  状态: {booking_dict.get('status')}")
                    if has_venue_id:
                        print(f"  venue_id: {booking_dict.get('venue_id')}")
                    print(f"  创建时间: {booking_dict.get('created_at')}")
                    print()
            
            # 总结
            print("=== 检查结果总结 ===")
            if has_venue_id:
                if bookings_with_venue == 0:
                    print("⚠️ venue_id字段已添加，但所有现有记录的venue_id都是NULL")
                    print("💡 这是正常现象，因为这些记录是在添加venue_id字段之前创建的")
                else:
                    print("✅ venue_id字段正常工作，已有部分记录包含venue_id数据")
            else:
                print("❌ venue_id字段不存在，需要执行数据库迁移")
            
            print("\n=== 启动Flask服务 ===")
            print("正在启动Flask服务...")
            print("访问地址: http://127.0.0.1:5000")
            print("数据库状态API: http://127.0.0.1:5000/api/debug/database_status")
            
            # 启动Flask服务
            app.run(
                host='127.0.0.1',
                port=5000,
                debug=False,
                use_reloader=False
            )
            
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保已安装所需依赖")
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复coach_bookings表中的venue_id数据
为现有的NULL记录分配合适的场馆
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数"""
    try:
        from flask import Flask
        from config import DevelopmentConfig
        from models import db, CoachBooking, Venue
        
        # 创建Flask应用
        app = Flask(__name__)
        app.config.from_object(DevelopmentConfig)
        db.init_app(app)
        
        with app.app_context():
            print("=== 开始修复venue_id数据 ===")
            
            # 获取所有场馆信息
            venues = Venue.query.all()
            print(f"可用场馆数量: {len(venues)}")
            
            if not venues:
                print("❌ 没有可用的场馆数据，无法分配venue_id")
                return
            
            for venue in venues:
                print(f"  场馆 {venue.id}: {venue.name}")
            
            # 查询所有venue_id为NULL的记录
            null_bookings = CoachBooking.query.filter(CoachBooking.venue_id.is_(None)).all()
            print(f"\n需要修复的预约记录数量: {len(null_bookings)}")
            
            if not null_bookings:
                print("✅ 所有预约记录都已包含venue_id数据")
                return
            
            # 修复策略：简单轮询分配
            success_count = 0
            for i, booking in enumerate(null_bookings):
                # 使用轮询方式分配场馆
                venue = venues[i % len(venues)]
                booking.venue_id = venue.id
                
                print(f"修复记录 {booking.id} (预约编号: {booking.booking_no}) -> 分配场馆: {venue.name} (ID: {venue.id})")
                success_count += 1
            
            # 提交更改
            db.session.commit()
            print(f"\n✅ 成功修复 {success_count} 条记录的venue_id")
            
            # 验证修复结果
            total_bookings = CoachBooking.query.count()
            bookings_with_venue = CoachBooking.query.filter(CoachBooking.venue_id.isnot(None)).count()
            print(f"验证结果:")
            print(f"  总预约记录: {total_bookings}")
            print(f"  包含venue_id的记录: {bookings_with_venue}")
            print(f"  venue_id覆盖率: {(bookings_with_venue/total_bookings*100):.1f}%")
            
            print("\n=== 修复完成 ===")
            print("现在外键字段已经有数据了！")
            
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库状态检查API
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from models import CoachBooking, Venue

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

@app.route('/api/debug/db_status')
def db_status():
    """数据库状态检查接口"""
    try:
        # 检查coach_bookings表结构
        columns = [column.name for column in CoachBooking.__table__.columns]
        has_venue_id = 'venue_id' in columns
        
        # 检查数据统计
        total_bookings = CoachBooking.query.count()
        bookings_with_venue = CoachBooking.query.filter(CoachBooking.venue_id.isnot(None)).count()
        bookings_without_venue = CoachBooking.query.filter(CoachBooking.venue_id.is_(None)).count()
        
        # 最近的预约记录
        recent_bookings = CoachBooking.query.order_by(CoachBooking.created_at.desc()).limit(5).all()
        
        # 获取示例记录
        sample_booking = None
        if total_bookings > 0:
            sample_booking = CoachBooking.query.first()
        
        # 统计各种状态的数据
        status_stats = {}
        for status in ['upcoming', 'confirmed', 'completed', 'cancelled']:
            count = CoachBooking.query.filter_by(status=status).count()
            status_stats[status] = count
        
        # 场馆数据统计
        total_venues = Venue.query.count()
        venues_with_price = Venue.query.filter(Venue.price_per_hour.isnot(None)).count()
        
        return jsonify({
            'code': 0,
            'message': '数据库状态检查成功',
            'data': {
                # 表结构信息
                'table_structure': {
                    'has_venue_id_column': has_venue_id,
                    'all_columns': columns,
                    'coach_bookings_columns_count': len(columns)
                },
                
                # 数据统计
                'data_statistics': {
                    'total_bookings': total_bookings,
                    'bookings_with_venue_id': bookings_with_venue,
                    'bookings_without_venue_id': bookings_without_venue,
                    'venue_id_coverage_rate': f"{(bookings_with_venue/total_bookings*100):.1f}%" if total_bookings > 0 else "0%"
                },
                
                # 状态统计
                'status_statistics': status_stats,
                
                # 场馆统计
                'venue_statistics': {
                    'total_venues': total_venues,
                    'venues_with_price': venues_with_price
                },
                
                # 示例数据
                'sample_data': {
                    'first_booking': sample_booking.to_dict() if sample_booking else None,
                    'recent_bookings_count': len(recent_bookings),
                    'recent_bookings': [booking.to_dict() for booking in recent_bookings]
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': f'数据库检查失败: {str(e)}',
            'data': None
        }), 500

@app.route('/api/debug/check_venue_data')
def check_venue_data():
    """检查venue_id相关数据"""
    try:
        # 检查venue_id字段的数据情况
        bookings_with_venue = CoachBooking.query.filter(CoachBooking.venue_id.isnot(None)).all()
        bookings_without_venue = CoachBooking.query.filter(CoachBooking.venue_id.is_(None)).all()
        
        # 检查有效的venue_id
        venue_ids = []
        if bookings_with_venue:
            venue_ids = [booking.venue_id for booking in bookings_with_venue]
            unique_venue_ids = list(set(venue_ids))
            
            # 检查这些venue_id是否在venues表中存在
            existing_venues = Venue.query.filter(Venue.id.in_(unique_venue_ids)).all()
            existing_venue_ids = [venue.id for venue in existing_venues]
            missing_venue_ids = [vid for vid in unique_venue_ids if vid not in existing_venue_ids]
        
        return jsonify({
            'code': 0,
            'message': 'venue_id数据检查成功',
            'data': {
                'total_bookings': CoachBooking.query.count(),
                'bookings_with_venue_id_count': len(bookings_with_venue),
                'bookings_without_venue_id_count': len(bookings_without_venue),
                'unique_venue_ids': unique_venue_ids if bookings_with_venue else [],
                'existing_venue_ids': existing_venue_ids if bookings_with_venue else [],
                'missing_venue_ids': missing_venue_ids if bookings_with_venue else [],
                'sample_bookings_with_venue': [
                    {
                        'id': booking.id,
                        'venue_id': booking.venue_id,
                        'booking_no': booking.booking_no,
                        'coach_id': booking.coach_id,
                        'user_id': booking.user_id
                    } for booking in bookings_with_venue[:5]
                ],
                'sample_bookings_without_venue': [
                    {
                        'id': booking.id,
                        'venue_id': booking.venue_id,
                        'booking_no': booking.booking_no,
                        'coach_id': booking.coach_id,
                        'user_id': booking.user_id
                    } for booking in bookings_without_venue[:5]
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': f'venue_id数据检查失败: {str(e)}',
            'data': None
        }), 500

if __name__ == '__main__':
    print("=== 数据库调试API启动 ===")
    print("访问 http://127.0.0.1:5001/api/debug/db_status 查看数据库状态")
    print("访问 http://127.0.0.1:5001/api/debug/check_venue_data 查看venue_id数据")
    app.run(debug=False, host='127.0.0.1', port=5001)
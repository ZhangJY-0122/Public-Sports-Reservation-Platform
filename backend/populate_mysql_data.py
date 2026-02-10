#!/usr/bin/env python3
"""
填充MySQL数据库初始数据
"""

import os
import sys
from datetime import datetime, timedelta
import random

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import User, VenueCategory, Venue, Activity, Coach, UserRole

def create_sample_data():
    """创建示例数据"""
    try:
        print("🔄 开始填充数据...")
        
        # 1. 创建用户（如果不存在）
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                real_name='系统管理员',
                phone='13800000000',
                role=UserRole.ADMIN
            )
            admin_user.set_password('123456')
            db.session.add(admin_user)
            print("✅ 创建管理员用户: admin/123456")
        
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            test_user = User(
                username='testuser',
                email='test@example.com',
                real_name='测试用户',
                phone='13900000000',
                role=UserRole.USER
            )
            test_user.set_password('123456')
            db.session.add(test_user)
            print("✅ 创建测试用户: testuser/123456")
        
        # 2. 创建场馆分类
        categories = [
            {'name': '篮球', 'description': '室内外篮球场地'},
            {'name': '足球', 'description': '足球场地'},
            {'name': '羽毛球', 'description': '羽毛球场地'},
            {'name': '网球', 'description': '网球场'},
            {'name': '游泳', 'description': '游泳池'},
            {'name': '健身', 'description': '健身房'},
            {'name': '乒乓球', 'description': '乒乓球桌'},
            {'name': '排球', 'description': '排球场地'}
        ]
        
        for cat_data in categories:
            existing = VenueCategory.query.filter_by(name=cat_data['name']).first()
            if not existing:
                category = VenueCategory(**cat_data)
                db.session.add(category)
        
        print(f"✅ 创建 {len([c for c in categories if not VenueCategory.query.filter_by(name=c['name']).first()])} 个场馆分类")
        
        # 3. 创建场馆
        venues_data = [
            {'name': '中央体育馆', 'description': '综合性体育场馆', 'category': '篮球', 'location': '市中心', 'price_per_hour': 100, 'type': '室内'},
            {'name': '绿色足球场', 'description': '标准足球场地', 'category': '足球', 'location': '郊区', 'price_per_hour': 80, 'type': '室外'},
            {'name': '飞翔羽毛球馆', 'description': '专业羽毛球场地', 'category': '羽毛球', 'location': '商业区', 'price_per_hour': 60, 'type': '室内'},
            {'name': '阳光网球场', 'description': '室外网球场', 'category': '网球', 'location': '公园内', 'price_per_hour': 70, 'type': '室外'},
            {'name': '蓝色游泳馆', 'description': '标准游泳池', 'category': '游泳', 'location': '体育中心', 'price_per_hour': 120, 'type': '室内'}
        ]
        
        for venue_data in venues_data:
            existing = Venue.query.filter_by(name=venue_data['name']).first()
            if not existing:
                category = VenueCategory.query.filter_by(name=venue_data['category']).first()
                if category:
                    venue = Venue(
                        name=venue_data['name'],
                        description=venue_data['description'],
                        type=venue_data['type'],
                        category_id=category.id,
                        location=venue_data['location'],
                        price_per_hour=venue_data['price_per_hour'],
                        contact_phone='13800138000'
                    )
                    db.session.add(venue)
        
        print(f"✅ 创建 {len([v for v in venues_data if not Venue.query.filter_by(name=v['name']).first()])} 个场馆")
        
        # 4. 创建活动
        activities_data = [
            {'title': '周末篮球赛', 'description': '友谊篮球比赛', 'activity_type': 'basketball', 'location': '中央体育馆'},
            {'title': '羽毛球训练营', 'description': '专业羽毛球训练', 'activity_type': 'badminton', 'location': '飞翔羽毛球馆'},
            {'title': '游泳健身班', 'description': '游泳技能培训', 'activity_type': 'swimming', 'location': '蓝色游泳馆'}
        ]
        
        for activity_data in activities_data:
            existing = Activity.query.filter_by(title=activity_data['title']).first()
            if not existing:
                from datetime import date, time
                activity = Activity(
                    title=activity_data['title'],
                    description=activity_data['description'],
                    activity_type=activity_data['activity_type'],
                    start_date=date.today() + timedelta(days=7),
                    end_date=date.today() + timedelta(days=7),
                    start_time=time(9, 0),
                    end_time=time(11, 0),
                    location=activity_data['location'],
                    max_participants=20,
                    organizer_id=admin_user.id
                )
                db.session.add(activity)
        
        print(f"✅ 创建 {len([a for a in activities_data if not Activity.query.filter_by(title=a['title']).first()])} 个活动")
        
        # 5. 创建教练
        coaches_data = [
            {'name': '张教练', 'specialization': '篮球', 'experience_years': 5, 'phone': '13800000001'},
            {'name': '李教练', 'specialization': '羽毛球', 'experience_years': 3, 'phone': '13800000002'},
            {'name': '王教练', 'specialization': '游泳', 'experience_years': 8, 'phone': '13800000003'}
        ]
        
        for coach_data in coaches_data:
            existing = Coach.query.filter_by(name=coach_data['name']).first()
            if not existing:
                coach = Coach(
                    name=coach_data['name'],
                    specialization=coach_data['specialization'],
                    experience_years=coach_data['experience_years'],
                    phone=coach_data['phone'],
                    introduction='专业体育教练，擅长教学。',
                    hourly_rate=200.0
                )
                db.session.add(coach)
        
        print(f"✅ 创建 {len([c for c in coaches_data if not Coach.query.filter_by(name=c['name']).first()])} 个教练")
        
        # 提交所有更改
        db.session.commit()
        
        # 6. 统计信息
        user_count = User.query.count()
        category_count = VenueCategory.query.count()
        venue_count = Venue.query.count()
        activity_count = Activity.query.count()
        coach_count = Coach.query.count()
        
        print("🎉 数据填充完成！")
        print(f"📊 统计信息:")
        print(f"  - 用户: {user_count} 个")
        print(f"  - 场馆分类: {category_count} 个")
        print(f"  - 场馆: {venue_count} 个")
        print(f"  - 活动: {activity_count} 个")
        print(f"  - 教练: {coach_count} 个")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据填充失败: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return False

if __name__ == "__main__":
    print("🚀 开始填充MySQL数据库初始数据...")
    
    # 创建Flask应用并获取应用上下文
    app = create_app()
    with app.app_context():
        if create_sample_data():
            print("🎉 数据填充完成！")
        else:
            print("❌ 数据填充失败")
            sys.exit(1)
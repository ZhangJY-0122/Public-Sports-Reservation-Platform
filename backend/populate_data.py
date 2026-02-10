#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据填充脚本
为数据库添加测试数据：场馆、用户、预约记录等
"""

import sys
import random
from datetime import datetime, timedelta

# 添加当前目录到Python路径
sys.path.append('.')

from app import create_app
from models import db, User, Venue, VenueCategory, Booking, BookingStatus

def populate_venues():
    """添加场馆数据"""
    print("\n🏟️ 添加场馆数据...")
    
    # 场馆分类数据
    categories_data = [
        "篮球场馆",
        "羽毛球馆", 
        "游泳馆",
        "健身中心",
        "网球场",
        "足球场",
        "乒乓球馆",
        "排球馆"
    ]
    
    # 场馆数据 - 每个分类对应多个场馆
    venues_data = [
        # 篮球场馆
        ("金牌篮球馆", "篮球场馆", "体育中心A座", "8片标准篮球场地", 120.0, 40),
        ("银牌篮球馆", "篮球场馆", "体育中心B座", "6片标准篮球场地", 100.0, 32),
        ("铜牌篮球馆", "篮球场馆", "体育中心C座", "4片标准篮球场地", 80.0, 24),
        
        # 羽毛球馆
        ("金牌羽毛球馆", "羽毛球馆", "体育中心A座", "24片专业羽毛球场地，木地板", 80.0, 48),
        ("银牌羽毛球馆", "羽毛球馆", "体育中心B座", "16片专业羽毛球场地，木地板", 70.0, 32),
        ("铜牌羽毛球馆", "羽毛球馆", "体育中心C座", "12片专业羽毛球场地，木地板", 60.0, 24),
        
        # 游泳馆
        ("金牌游泳馆", "游泳馆", "水上中心A馆", "8道50米标准泳池", 60.0, 50),
        ("银牌游泳馆", "游泳馆", "水上中心B馆", "6道50米标准泳池", 50.0, 40),
        ("铜牌游泳馆", "游泳馆", "水上中心C馆", "4道25米短池", 40.0, 25),
        
        # 健身中心
        ("全能健身中心", "健身中心", "健身大厦1层", "器械齐全，环境优雅", 50.0, 60),
        ("力量健身中心", "健身中心", "健身大厦2层", "专业力量训练器械", 60.0, 40),
        ("有氧健身中心", "健身中心", "健身大厦3层", "有氧器械和团体课程", 45.0, 50),
        
        # 网球场
        ("金牌网球场", "网球场", "网球中心A馆", "4片标准网球场，硬地", 90.0, 16),
        ("银牌网球场", "网球场", "网球中心B馆", "3片标准网球场，硬地", 80.0, 12),
        ("铜牌网球场", "网球场", "网球中心C馆", "2片标准网球场，硬地", 70.0, 8),
        
        # 足球场
        ("金牌足球场", "足球场", "足球公园A场", "11人制标准足球场", 200.0, 22),
        ("银牌足球场", "足球场", "足球公园B场", "7人制足球场", 100.0, 14),
        ("铜牌足球场", "足球场", "足球公园C场", "5人制足球场", 60.0, 10),
        
        # 乒乓球馆
        ("金牌乒乓球馆", "乒乓球馆", "球类中心A馆", "20台专业乒乓球台", 40.0, 40),
        ("银牌乒乓球馆", "乒乓球馆", "球类中心B馆", "15台专业乒乓球台", 35.0, 30),
        ("铜牌乒乓球馆", "乒乓球馆", "球类中心C馆", "10台专业乒乓球台", 30.0, 20),
        
        # 排球馆
        ("金牌排球馆", "排球馆", "排球中心A馆", "4片标准排球场", 70.0, 24),
        ("银牌排球馆", "排球馆", "排球中心B馆", "3片标准排球场", 60.0, 18),
        ("铜牌排球馆", "排球馆", "排球中心C馆", "2片标准排球场", 50.0, 12)
    ]
    
    # 获取或创建场馆分类
    existing_categories = db.session.query(VenueCategory).all()
    if len(existing_categories) < 8:
        print("  📝 创建场馆分类...")
        # 清空现有分类
        db.session.query(VenueCategory).delete()
        db.session.commit()
        
        # 创建分类
        for category_name in categories_data:
            category = VenueCategory(name=category_name)
            db.session.add(category)
            print(f"  ✅ 添加分类: {category_name}")
        
        db.session.commit()
    
    # 重新查询分类
    existing_categories = db.session.query(VenueCategory).all()
    
    # 构建分类ID映射
    category_id_map = {}
    for cat in existing_categories:
        category_id_map[cat.name] = cat.id
    
    print(f"  📊 现有分类: {list(category_id_map.keys())}")
    
    # 批量添加场馆
    for venue_name, category_name, location, description, price, capacity in venues_data:
        try:
            # 检查场馆是否已存在
            existing_venue = db.session.query(Venue).filter(Venue.name == venue_name).first()
            if existing_venue:
                print(f"  ⚠️ 场馆已存在: {venue_name}")
                continue
                
            category_id = category_id_map.get(category_name)
            if not category_id:
                print(f"  ❌ 找不到分类 '{category_name}' 的ID")
                continue
                
            venue = Venue(
                name=venue_name,
                type=category_name,  # 添加必填字段
                category_id=category_id,
                location=location,
                description=description,
                business_hours='06:00-22:00',  # 添加必填字段
                contact_phone='13800138000',  # 添加必填字段
                price_per_hour=price,
                capacity=capacity
            )
            
            db.session.add(venue)
            print(f"  ✅ 添加场馆: {venue.name}")
        except Exception as e:
            print(f"  ❌ 添加场馆失败 {venue_name}: {e}")
    
    db.session.commit()
    print("🏟️ 场馆数据添加完成！")

def populate_users():
    """添加更多用户数据"""
    print("\n👤 添加用户数据...")
    
    # 检查是否已有用户数据
    existing_users = db.session.query(User).count()
    if existing_users > 1:  # 已经有用户数据
        print(f"  ⚠️ 已存在 {existing_users} 个用户，跳过用户数据添加")
        return
    
    # 清空现有用户数据（除了管理员）
    db.session.query(User).filter(User.role != 'admin').delete()
    db.session.commit()
    
    # 测试用户数据
    test_users = [
        ("zhangsan", "zhangsan@email.com", "zhangsan123", "张三", "13800138001"),
        ("lisi", "lisi@email.com", "lisi123", "李四", "13800138002"),
        ("wangwu", "wangwu@email.com", "wangwu123", "王五", "13800138003"),
        ("zhaoliu", "zhaoliu@email.com", "zhaoliu123", "赵六", "13800138004"),
        ("sunqi", "sunqi@email.com", "sunqi123", "孙七", "13800138005"),
        ("zhouba", "zhouba@email.com", "zhouba123", "周八", "13800138006"),
        ("wujiu", "wujiu@email.com", "wujiu123", "吴九", "13800138007"),
        ("zhengshi", "zhengshi@email.com", "zhengshi123", "郑十", "13800138008"),
        ("testuser1", "test1@email.com", "test123", "测试用户一", "13800138009"),
        ("testuser2", "test2@email.com", "test123", "测试用户二", "13800138010"),
        ("xiaoming", "xiaoming@email.com", "xiaoming123", "小明", "13800138011"),
        ("xiaohong", "xiaohong@email.com", "xiaohong123", "小红", "13800138012"),
        ("xiaoli", "xiaoli@email.com", "xiaoli123", "小李", "13800138013"),
        ("xiaozhang", "xiaozhang@email.com", "xiaozhang123", "小张", "13800138014"),
        ("xiaowang", "xiaowang@email.com", "xiaowang123", "小王", "13800138015")
    ]
    
    # 批量创建测试用户
    for user_data in test_users:
        try:
            username, email, password, real_name, phone = user_data
            user = User(
                username=username,
                email=email,
                password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8jJLx1E1i2",  # 统一测试密码哈希
                real_name=real_name,
                phone=phone,
                role='user'  # 使用字符串类型而不是布尔值
            )
            db.session.add(user)
            print(f"  ✅ 添加用户: {user.username} ({user.real_name})")
        except Exception as e:
            print(f"  ❌ 添加用户失败 {user_data[0]}: {e}")
    
    db.session.commit()
    print("👤 用户数据添加完成！")

def populate_bookings():
    """添加预约记录数据"""
    print("\n📅 添加预约记录数据...")
    
    # 清空现有预约数据
    db.session.query(Booking).delete()
    db.session.commit()
    
    # 获取所有用户和场馆
    users = db.session.query(User).filter(User.role != 'admin').all()
    venues = db.session.query(Venue).all()
    
    if not users or not venues:
        print("  ⚠️ 缺少用户或场馆数据，跳过预约记录创建")
        return
    
    # 时间段配置
    time_slots = [
        ("08:00", "10:00"),
        ("10:00", "12:00"),
        ("14:00", "16:00"),
        ("16:00", "18:00"),
        ("19:00", "21:00")
    ]
    
    booking_count = 0
    base_date = datetime.now()
    
    # 生成过去7天到未来30天的预约
    for day_offset in range(-7, 30):  # 过去7天到未来30天
        booking_date = (base_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')
        
        # 每天随机生成0-3个预约
        daily_bookings = random.randint(0, 3)
        
        for _ in range(daily_bookings):
            # 随机选择用户、场馆和时间段
            user = random.choice(users)
            venue = random.choice(venues)
            start_time, end_time = random.choice(time_slots)
            
            # 根据日期设置状态
            if day_offset < 0:  # 过去的预约
                status = random.choice([BookingStatus.COMPLETED, BookingStatus.CANCELLED])  # 已完成或已取消
            elif day_offset == 0:  # 今天的预约
                status = random.choice([BookingStatus.UPCOMING, BookingStatus.COMPLETED])
            else:  # 未来的预约
                status = BookingStatus.UPCOMING
            
            booking = create_booking(user.id, venue.id, booking_date, start_time, end_time, status)
            if booking:
                booking_count += 1
                if booking_count % 10 == 0:  # 每10个预约打印一次进度
                    print(f"  📊 已创建 {booking_count} 个预约记录...")
    
    print(f"📅 预约记录添加完成！共创建 {booking_count} 个预约")

def create_booking(user_id, venue_id, booking_date_str, start_time_str, end_time_str, status=BookingStatus.UPCOMING):
    """创建预约记录"""
    try:
        # 解析日期和时间
        booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()
        
        # 检查时间冲突
        existing_booking = db.session.query(Booking).filter(
            Booking.venue_id == venue_id,
            Booking.booking_date == booking_date,
            Booking.status != BookingStatus.CANCELLED
        ).filter(
            db.or_(
                db.and_(
                    Booking.start_time <= start_time,
                    Booking.end_time > start_time
                ),
                db.and_(
                    Booking.start_time < end_time,
                    Booking.end_time >= end_time
                ),
                db.and_(
                    Booking.start_time >= start_time,
                    Booking.end_time <= end_time
                )
            )
        ).first()
        
        if existing_booking:
            return None  # 时间冲突，不创建
        
        # 计算持续时间和价格
        start_dt = datetime.combine(booking_date, start_time)
        end_dt = datetime.combine(booking_date, end_time)
        duration_hours = (end_dt - start_dt).total_seconds() / 3600
        
        # 获取场馆价格
        venue = db.session.get(Venue, venue_id)
        total_price = float(duration_hours) * float(venue.price_per_hour) if venue else 0
        
        # 生成预约编号
        booking_no = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}{user_id:03d}{venue_id:03d}"
        
        # 创建预约
        booking = Booking(
            booking_no=booking_no,
            user_id=user_id,
            venue_id=venue_id,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            duration_hours=duration_hours,
            total_price=total_price,
            status=status,
            description=None,
            cancel_reason=None
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return booking
        
    except Exception as e:
        print(f"❌ 创建预约失败: {e}")
        db.session.rollback()
        return None

def populate_data():
    """主函数：填充所有数据"""
    print("🚀 开始填充数据库...")
    
    try:
        # 添加场馆数据
        populate_venues()
        
        # 添加用户数据
        populate_users()
        
        # 添加预约记录数据
        populate_bookings()
        
        print("\n🎉 所有数据填充完成！")
        
    except Exception as e:
        print(f"\n❌ 数据填充失败: {e}")
        db.session.rollback()

if __name__ == "__main__":
    # 创建应用并运行在应用上下文中
    app = create_app()
    
    with app.app_context():
        populate_data()
"""
数据库初始化和迁移管理模块
"""

import os
import sys
from datetime import datetime, date, time, timedelta
from werkzeug.security import generate_password_hash
from models import db, User, UserRole, VenueCategory, Venue, Booking, BookingStatus, Activity, Event, Coach, CoachBooking, Friendship
from config import DevelopmentConfig

def create_tables(app):
    """
    创建所有数据库表
    """
    with app.app_context():
        try:
            # 创建所有表
            db.create_all()
            print("数据库表创建成功")
            return True
        except Exception as e:
            print(f"创建数据库表失败: {e}")
            return False

def drop_tables(app):
    """
    删除所有数据库表
    """
    with app.app_context():
        try:
            # 删除所有表
            db.drop_all()
            print("数据库表删除成功")
            return True
        except Exception as e:
            print(f"删除数据库表失败: {e}")
            return False

def init_database(app):
    """
    初始化数据库，创建基础数据
    """
    with app.app_context():
        try:
            print("开始初始化数据库...")
            
            # 创建场馆分类
            categories_data = [
                {'name': '足球场', 'description': '标准足球场地，适合11人制和5人制足球', 'icon': 'football', 'sort_order': 1},
                {'name': '篮球场', 'description': '标准篮球场地，室内外场地齐全', 'icon': 'basketball', 'sort_order': 2},
                {'name': '网球场', 'description': '标准网球场地，支持硬地、红土和草地', 'icon': 'tennis', 'sort_order': 3},
                {'name': '羽毛球馆', 'description': '专业羽毛球场地，配备专业照明和通风', 'icon': 'badminton', 'sort_order': 4},
                {'name': '游泳池', 'description': '标准游泳池，长度50米，含深浅水区', 'icon': 'swimming', 'sort_order': 5},
                {'name': '乒乓球室', 'description': '专业乒乓球室，配备专业球台和球网', 'icon': 'pingpong', 'sort_order': 6},
                {'name': '健身房', 'description': '现代化健身房，配备各类健身器材', 'icon': 'fitness', 'sort_order': 7},
                {'name': '排球场', 'description': '标准排球场地，适合室内外排球运动', 'icon': 'volleyball', 'sort_order': 8}
            ]
            
            categories = []
            for cat_data in categories_data:
                category = VenueCategory(**cat_data)
                db.session.add(category)
                categories.append(category)
            
            db.session.commit()
            print(f"创建了 {len(categories)} 个场馆分类")
            
            # 创建场馆
            venues_data = [
                {
                    'name': '奥林匹克体育中心',
                    'category_id': 1,
                    'type': '综合体育中心',
                    'location': '市体育大道1号',
                    'description': '拥有标准足球场、篮球场、网球场等多项设施，是本市最大的综合性体育中心',
                    'price_per_hour': 150,
                    'contact_phone': '400-123-4567',
                    'facilities': '停车场,更衣室,淋浴间,观众席',
                    'image': '/static/images/venue1.jpg',
                    'business_hours': '06:00-22:00'
                },
                {
                    'name': '市民健身中心',
                    'category_id': 1,
                    'type': '社区健身中心',
                    'location': '人民路88号',
                    'description': '位于市中心的现代化健身中心，交通便利，设施齐全',
                    'price_per_hour': 80,
                    'contact_phone': '400-234-5678',
                    'facilities': '停车场,更衣室,淋浴间',
                    'image': '/static/images/venue2.jpg',
                    'business_hours': '07:00-21:00'
                },
                {
                    'name': '大学城体育馆',
                    'category_id': 2,
                    'type': '校园体育设施',
                    'location': '大学城体育路1号',
                    'description': '大学城内最专业的篮球场馆，经常举办各类篮球赛事',
                    'price_per_hour': 60,
                    'contact_phone': '400-345-6789',
                    'facilities': '观众席,更衣室,计分系统',
                    'image': '/static/images/venue3.jpg',
                    'business_hours': '08:00-22:00'
                },
                {
                    'name': '绿色网球俱乐部',
                    'category_id': 3,
                    'type': '专业网球俱乐部',
                    'location': '网球公园内',
                    'description': '拥有8个标准网球场，其中4个为红土场地，4个为硬地场地',
                    'price_per_hour': 120,
                    'contact_phone': '400-456-7890',
                    'facilities': '专业照明,观众席,休息室,咖啡厅',
                    'image': '/static/images/venue4.jpg',
                    'business_hours': '06:00-22:00'
                },
                {
                    'name': '飞翔羽毛球馆',
                    'category_id': 4,
                    'type': '专业羽毛球馆',
                    'location': '体育路168号',
                    'description': '专业的羽毛球场地，场馆高度和照明都符合国际标准',
                    'price_per_hour': 70,
                    'contact_phone': '400-567-8901',
                    'facilities': '专业照明,更衣室,淋浴间,休息区',
                    'image': '/static/images/venue5.jpg',
                    'business_hours': '06:00-23:00'
                },
                {
                    'name': '阳光游泳馆',
                    'category_id': 5,
                    'type': '标准游泳池',
                    'location': '滨河路88号',
                    'description': '50米标准游泳池，分浅水区和深水区，适合各年龄段游泳爱好者',
                    'price_per_hour': 50,
                    'contact_phone': '400-678-9012',
                    'facilities': '消毒设施,更衣室,淋浴间,休息区',
                    'image': '/static/images/venue6.jpg',
                    'business_hours': '06:00-22:00'
                }
            ]
            
            venues = []
            for venue_data in venues_data:
                venue = Venue(**venue_data)
                db.session.add(venue)
                venues.append(venue)
            
            db.session.commit()
            print(f"创建了 {len(venues)} 个场馆")
            
            # 创建测试用户前先检查是否已存在
            existing_admin = User.query.filter_by(email='admin@example.com').first()
            if existing_admin:
                print("管理员用户已存在，跳过创建")
                admin_user = existing_admin
            else:
                print("创建新的管理员用户")
                admin_user = User(
                    username='admin',
                    password_hash=generate_password_hash('admin123'),
                    email='admin@example.com',
                    phone='13800000001',
                    city='上海市',
                    role=UserRole.ADMIN
                )
                db.session.add(admin_user)
            
            # 创建普通用户
            test_users_data = [
                {
                    'username': 'user1',
                    'password_hash': generate_password_hash('123456'),
                    'email': 'user1@example.com',
                    'phone': '13800000002',
                    'city': '上海市',
                    'real_name': '体育爱好者'
                },
                {
                    'username': 'user2',
                    'password_hash': generate_password_hash('123456'),
                    'email': 'user2@example.com',
                    'phone': '13800000003',
                    'city': '北京市',
                    'real_name': '足球小子'
                },
                {
                    'username': 'user3',
                    'password_hash': generate_password_hash('123456'),
                    'email': 'user3@example.com',
                    'phone': '13800000004',
                    'city': '广州市',
                    'real_name': '网球达人'
                }
            ]
            
            test_users = []
            for user_data in test_users_data:
                # 检查用户是否已存在
                existing_user = User.query.filter_by(email=user_data['email']).first()
                if existing_user:
                    print(f"用户 {user_data['email']} 已存在，跳过创建")
                    test_users.append(existing_user)
                else:
                    user = User(**user_data)
                    db.session.add(user)
                    test_users.append(user)
            
            db.session.commit()
            print(f"创建了 {len(test_users) + 1} 个用户")
            
            # 创建示例预约
            tomorrow = date.today() + timedelta(days=1)
            
            def generate_booking_no():
                """生成预约编号"""
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                import random
                return f"BK{timestamp}{random.randint(100, 999)}"
            
            booking_examples = [
                {
                    'booking_no': generate_booking_no(),
                    'user_id': admin_user.id,
                    'venue_id': venues[0].id,  # 奥林匹克体育中心
                    'booking_date': tomorrow,
                    'start_time': time(14, 0),
                    'end_time': time(16, 0),
                    'duration_hours': 2,
                    'total_price': 300,
                    'status': BookingStatus.UPCOMING
                },
                {
                    'booking_no': generate_booking_no(),
                    'user_id': test_users[0].id,
                    'venue_id': venues[2].id,  # 大学城体育馆
                    'booking_date': tomorrow,
                    'start_time': time(19, 0),
                    'end_time': time(21, 0),
                    'duration_hours': 2,
                    'total_price': 120,
                    'status': BookingStatus.UPCOMING
                }
            ]
            
            for booking_data in booking_examples:
                booking = Booking(**booking_data)
                db.session.add(booking)
            
            db.session.commit()
            print("创建了示例预约记录")
            
            # 创建活动
            activities_data = [
                {
                    'title': '春季足球联赛',
                    'description': '一年一度的春季足球联赛，欢迎各业余足球队报名参加',
                    'activity_type': '比赛',
                    'start_date': date.today() + timedelta(days=7),
                    'end_date': date.today() + timedelta(days=30),
                    'start_time': time(9, 0),
                    'end_time': time(18, 0),
                    'location': '奥林匹克体育中心',
                    'max_participants': 16,
                    'current_participants': 8,
                    'organizer_id': admin_user.id
                },
                {
                    'title': '青少年网球夏令营',
                    'description': '专为8-16岁青少年设计的网球训练营，专业教练指导',
                    'activity_type': '训练营',
                    'start_date': date.today() + timedelta(days=14),
                    'end_date': date.today() + timedelta(days=21),
                    'start_time': time(9, 0),
                    'end_time': time(17, 0),
                    'location': '绿色网球俱乐部',
                    'max_participants': 20,
                    'current_participants': 15,
                    'organizer_id': admin_user.id
                }
            ]
            
            activities = []
            for activity_data in activities_data:
                activity = Activity(**activity_data)
                db.session.add(activity)
                activities.append(activity)
            
            db.session.commit()
            print(f"创建了 {len(activities)} 个活动")
            
            print("数据库初始化完成！")
            print("\n测试账户信息:")
            print("管理员账户: admin / admin123")
            print("普通用户1: user1 / 123456")
            print("普通用户2: user2 / 123456")
            print("普通用户3: user3 / 123456")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"数据库初始化失败: {e}")
            return False

def reset_database(app):
    """
    重置数据库（删除所有表并重新创建基础数据）
    """
    with app.app_context():
        print("开始重置数据库...")
        if drop_tables(app):
            if create_tables(app):
                return init_database(app)
        return False

def get_database_info(app):
    """
    获取数据库信息
    """
    with app.app_context():
        try:
            info = {}
            
            # 获取各表记录数量
            tables_info = {
                'users': User.query.count(),
                'venue_categories': VenueCategory.query.count(),
                'venues': Venue.query.count(),
                'bookings': Booking.query.count(),
                'activities': Activity.query.count(),
                'events': Event.query.count()
            }
            
            info['tables'] = tables_info
            info['database_uri'] = app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')
            info['current_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return info
        except Exception as e:
            return {'error': str(e)}

if __name__ == '__main__':
    # 命令行使用方法
    from app import create_app
    
    app = create_app()
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python migrate.py create     - 创建数据库表")
        print("  python migrate.py init       - 初始化数据库")
        print("  python migrate.py reset      - 重置数据库")
        print("  python migrate.py drop       - 删除所有表")
        print("  python migrate.py info       - 查看数据库信息")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'create':
        create_tables(app)
    elif command == 'init':
        init_database(app)
    elif command == 'reset':
        reset_database(app)
    elif command == 'drop':
        drop_tables(app)
    elif command == 'info':
        info = get_database_info(app)
        print("数据库信息:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    else:
        print(f"未知命令: {command}")
        sys.exit(1)
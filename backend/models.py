"""
数据库模型定义
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
import enum

db = SQLAlchemy()

class UserRole(enum.Enum):
    """用户角色枚举"""
    USER = 'user'
    ADMIN = 'admin'

class BookingStatus(enum.Enum):
    """预约状态枚举"""
    UPCOMING = 'upcoming'  # 即将开始
    COMPLETED = 'completed'  # 已完成
    CANCELLED = 'cancelled'  # 已取消
    IN_PROGRESS = 'in_progress'  # 进行中

class SharePermission(enum.Enum):
    """分享权限枚举"""
    VIEW_ONLY = "view_only"      # 仅查看
    CAN_EDIT = "can_edit"        # 可编辑
    CAN_CANCEL = "can_cancel"    # 可取消

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(50), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)
    
    # 用户统计信息
    exercise_days = db.Column(db.Integer, default=0, comment='运动天数')
    friends_count = db.Column(db.Integer, default=0, comment='好友数量')
    points = db.Column(db.Integer, default=0, comment='积分')
    vip_level = db.Column(db.Integer, default=0, comment='VIP等级')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)
    
    # 关系
    # bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    organized_activities = db.relationship('Activity', foreign_keys='Activity.organizer_id', backref='user_activities', lazy='dynamic')
    friendships = db.relationship('Friendship', foreign_keys='Friendship.user_id', backref='user', lazy='dynamic')
    friend_of = db.relationship('Friendship', foreign_keys='Friendship.friend_id', backref='friend', lazy='dynamic')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """检查密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'real_name': self.real_name,
            'avatar': self.avatar,
            'city': self.city,
            'role': self.role.value if self.role else 'user',
            'exercise_days': self.exercise_days,
            'friends_count': self.friends_count,
            'points': self.points,
            'vip_level': self.vip_level,
            'is_active': True,  # 假设默认都是激活状态，后续可以添加is_active字段到数据库
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }

class VenueCategory(db.Model):
    """场馆分类模型"""
    __tablename__ = 'venue_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, comment='分类名称')
    icon = db.Column(db.String(100), nullable=True, comment='分类图标')
    description = db.Column(db.String(200), nullable=True, comment='分类描述')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    is_active = db.Column(db.Boolean, default=True, comment='是否启用')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    venues = db.relationship('Venue', backref='category', lazy='dynamic')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'description': self.description,
            'sort_order': self.sort_order,
            'is_active': self.is_active
        }

class Venue(db.Model):
    """场馆模型"""
    __tablename__ = 'venues'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='场馆名称')
    type = db.Column(db.String(50), nullable=False, comment='场馆类型')
    location = db.Column(db.String(200), nullable=False, comment='场馆地址')
    description = db.Column(db.Text, nullable=True, comment='场馆描述')
    image = db.Column(db.String(255), nullable=True, comment='场馆图片')
    price_per_hour = db.Column(db.Numeric(10, 2), nullable=False, comment='每小时价格')
    capacity = db.Column(db.Integer, default=1, comment='容量/人数')
    facilities = db.Column(db.Text, nullable=True, comment='设施描述')
    contact_phone = db.Column(db.String(20), nullable=True, comment='联系电话')
    business_hours = db.Column(db.String(100), nullable=True, comment='营业时间')
    is_active = db.Column(db.Boolean, default=True, comment='是否启用')
    
    # 外键
    category_id = db.Column(db.Integer, db.ForeignKey('venue_categories.id'), nullable=False)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    bookings = db.relationship('Booking', backref='venue', lazy='dynamic')
    reviews = db.relationship('VenueReview', backref='venue', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'location': self.location,
            'description': self.description,
            'image': self.image,
            'price': str(self.price_per_hour),
            'capacity': self.capacity,
            'facilities': self.facilities,
            'contact_phone': self.contact_phone,
            'business_hours': self.business_hours,
            'category': self.category.to_dict() if self.category else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_average_rating(self):
        """获取平均评分"""
        reviews = self.reviews.filter(VenueReview.is_public == True).all()
        if not reviews:
            return 0.0
        return sum(review.rating for review in reviews) / len(reviews)
    
    def get_review_count(self):
        """获取评价数量"""
        return self.reviews.filter(VenueReview.is_public == True).count()

class VenueReview(db.Model):
    """场馆评价模型"""
    __tablename__ = 'venue_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 外键
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 评价信息
    rating = db.Column(db.Integer, nullable=False, comment='评分(1-5)')
    title = db.Column(db.String(100), nullable=True, comment='评价标题')
    content = db.Column(db.Text, nullable=True, comment='评价内容')
    images = db.Column(db.Text, nullable=True, comment='评价图片(JSON数组)')
    
    # 状态
    is_public = db.Column(db.Boolean, default=True, comment='是否公开')
    is_verified = db.Column(db.Boolean, default=False, comment='是否已验证(基于真实预约)')
    
    # 点赞统计
    like_count = db.Column(db.Integer, default=0, comment='点赞数')
    dislike_count = db.Column(db.Integer, default=0, comment='点踩数')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 添加关系
    review_user = db.relationship('User', backref='venue_reviews')
    # 注意：venue关系通过Venue模型的backref='venue'自动创建，不需要重复定义
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'venue_id': self.venue_id,
            'venue_name': self.venue.name if self.venue else '',
            'user_id': self.user_id,
            'username': self.user.username if self.user else '',
            'user_avatar': self.user.avatar if self.user else '',
            'rating': self.rating,
            'title': self.title,
            'content': self.content,
            'images': self.get_image_list(),
            'is_public': self.is_public,
            'is_verified': self.is_verified,
            'like_count': self.like_count,
            'dislike_count': self.dislike_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_image_list(self):
        """获取图片列表"""
        if not self.images:
            return []
        try:
            import json
            return json.loads(self.images)
        except (json.JSONDecodeError, TypeError):
            return []

class Booking(db.Model):
    """预约模型"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_no = db.Column(db.String(50), unique=True, nullable=False, comment='预约编号')
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    
    # 分摊费用关系
    shares = db.relationship('BookingShare', backref='booking', lazy='dynamic', cascade='all, delete-orphan')
    
    # 预约信息
    booking_date = db.Column(db.Date, nullable=False, comment='预约日期')
    start_time = db.Column(db.Time, nullable=False, comment='开始时间')
    end_time = db.Column(db.Time, nullable=False, comment='结束时间')
    duration_hours = db.Column(db.Numeric(4, 2), nullable=False, comment='预约时长（小时）')
    total_price = db.Column(db.Numeric(10, 2), nullable=False, comment='总价格')
    
    # 状态和备注
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.UPCOMING, nullable=False)
    description = db.Column(db.Text, nullable=True, comment='预约备注')
    cancel_reason = db.Column(db.String(200), nullable=True, comment='取消原因')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancelled_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'booking_no': self.booking_no,
            'user_id': self.user_id,
            'user_name': self.user.username if self.user else '',
            'venue_id': self.venue_id,
            'venue_name': self.venue.name if self.venue else '',
            'venue_type': self.venue.type if self.venue else '',
            'venue_icon': self.get_venue_icon(),
            'date': self.booking_date.isoformat(),
            'time': f'{self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M")}',
            'duration': f'{self.duration_hours}小时',
            'price': str(self.total_price),
            'status': self.status.value,
            'status_text': self.get_status_text(),
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_venue_icon(self):
        """获取场馆图标"""
        if not self.venue or not self.venue.category:
            return '🏟️'
        
        category_name = self.venue.category.name.lower()
        icon_map = {
            '羽毛球': '🏸',
            '篮球': '🏀',
            '游泳': '🏊‍♂️',
            '健身': '💪',
            '网球': '🎾',
            '足球': '⚽',
            '乒乓球': '🏓'
        }
        return icon_map.get(self.venue.category.name, '🏟️')
    
    def get_status_text(self):
        """获取状态文本"""
        status_map = {
            BookingStatus.UPCOMING: '即将开始',
            BookingStatus.IN_PROGRESS: '进行中',
            BookingStatus.COMPLETED: '已完成',
            BookingStatus.CANCELLED: '已取消'
        }
        return status_map.get(self.status, '未知状态')




class Activity(db.Model):
    """活动模型"""
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, comment='活动标题')
    description = db.Column(db.Text, nullable=True, comment='活动描述')
    image = db.Column(db.String(255), nullable=True, comment='活动图片')
    activity_type = db.Column(db.String(50), nullable=False, comment='活动类型')
    
    # 时间信息
    start_date = db.Column(db.Date, nullable=False, comment='开始日期')
    end_date = db.Column(db.Date, nullable=False, comment='结束日期')
    start_time = db.Column(db.Time, nullable=False, comment='开始时间')
    end_time = db.Column(db.Time, nullable=False, comment='结束时间')
    
    # 地点和人数
    location = db.Column(db.String(200), nullable=False, comment='活动地点')
    max_participants = db.Column(db.Integer, nullable=False, comment='最大参与人数')
    current_participants = db.Column(db.Integer, default=0, comment='当前参与人数')
    
    # 状态和费用
    registration_fee=db.Column(db.Numeric(10, 2), nullable=True, comment='报名费')
    status = db.Column(db.String(20), default='upcoming', comment='活动状态: upcoming/ongoing/completed/cancelled')
    is_active = db.Column(db.Boolean, default=True, comment='是否启用')
    
    # 外键
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    organizer = db.relationship('User', foreign_keys=[organizer_id], backref='user_activities')
    participants = db.relationship('ActivityParticipant', backref='activity', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'activity_type': self.activity_type,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M'),
            'location': self.location,
            'max_participants': self.max_participants,
            'current_participants': self.current_participants,
            'registration_fee': str(self.registration_fee) if self.registration_fee else '0',
            'status': self.status,
            'organizer_id': self.organizer_id,
            'organizer': self.organizer.username if self.organizer else '',
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'participants_count': self.participants.filter_by(status='joined').count()
        }
    
    def add_participant(self, user_id):
        """添加参与者"""
        existing = ActivityParticipant.query.filter_by(
            activity_id=self.id, 
            user_id=user_id
        ).first()
        
        if existing:
            return False, '用户已经是参与者'
        
        # 检查人数限制
        if self.current_participants >= self.max_participants:
            return False, '活动人数已满'
        
        participant = ActivityParticipant(
            activity_id=self.id,
            user_id=user_id,
            status='joined'
        )
        db.session.add(participant)
        self.current_participants += 1
        return True, '成功加入活动'
    
    def remove_participant(self, user_id):
        """移除参与者"""
        participant = ActivityParticipant.query.filter_by(
            activity_id=self.id,
            user_id=user_id,
            status='joined'
        ).first()
        
        if not participant:
            return False, '用户不是参与者'
        
        participant.status = 'left'
        self.current_participants = max(0, self.current_participants - 1)
        return True, '成功退出活动'

class ActivityParticipant(db.Model):
    """活动参与者模型"""
    __tablename__ = 'activity_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 外键
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 状态
    status = db.Column(db.String(20), default='joined', comment='参与状态: joined/left/cancelled')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, comment='加入时间')
    left_at = db.Column(db.DateTime, nullable=True, comment='退出时间')
    
    # 关系
    user = db.relationship('User', foreign_keys=[user_id], backref='activity_participations')
    
    # 唯一约束
    __table_args__ = (db.UniqueConstraint('activity_id', 'user_id', name='unique_activity_user'),)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'activity_id': self.activity_id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else '',
            'status': self.status,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'left_at': self.left_at.isoformat() if self.left_at else None
        }

class Friend(db.Model):
    """朋友关系模型"""
    __tablename__ = 'friends'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='发起者ID')
    friend_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='朋友用户ID')
    
    # 状态和消息
    status = db.Column(db.String(20), default='pending', comment='状态: pending/accepted/rejected')
    message = db.Column(db.String(200), nullable=True, comment='验证消息')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    friend_user = db.relationship('User', foreign_keys=[friend_user_id], backref='friend_requests')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'friend_user_id': self.friend_user_id,
            'status': self.status,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Friendship(db.Model):
    """好友关系模型"""
    __tablename__ = 'friendships'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 状态
    status = db.Column(db.String(20), default='active', comment='关系状态')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 确保同一对用户只有一个关系
    __table_args__ = (db.UniqueConstraint('user_id', 'friend_id'),)

class Event(db.Model):
    """赛事模型"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='赛事名称')
    description = db.Column(db.Text, nullable=True, comment='赛事描述')
    image = db.Column(db.String(255), nullable=True, comment='赛事图片')
    event_type = db.Column(db.String(50), nullable=False, comment='赛事类型')
    
    # 时间信息
    event_date = db.Column(db.Date, nullable=False, comment='赛事日期')
    registration_deadline = db.Column(db.Date, nullable=False, comment='报名截止日期')
    
    # 地点和参与
    location = db.Column(db.String(200), nullable=False, comment='赛事地点')
    max_participants = db.Column(db.Integer, nullable=False, comment='最大参赛人数')
    current_participants = db.Column(db.Integer, default=0, comment='当前参赛人数')
    
    # 状态和费用
    status = db.Column(db.String(20), default='upcoming', comment='赛事状态')
    registration_fee = db.Column(db.Numeric(10, 2), default=0, comment='报名费用')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'event_type': self.event_type,
            'event_date': self.event_date.isoformat(),
            'registration_deadline': self.registration_deadline.isoformat(),
            'location': self.location,
            'max_participants': self.max_participants,
            'current_participants': self.current_participants,
            'status': self.status,
            'registration_fee': str(self.registration_fee),
            'time': self.event_date.strftime('%Y-%m-%d'),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class EventRegistration(db.Model):
    """赛事报名模型"""
    __tablename__ = 'event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 外键
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 报名信息
    registration_no = db.Column(db.String(50), unique=True, nullable=False, comment='报名编号')
    status = db.Column(db.String(20), default='pending', comment='报名状态: pending/approved/rejected/cancelled')
    contact_info = db.Column(db.String(200), nullable=True, comment='联系方式')
    additional_info = db.Column(db.Text, nullable=True, comment='附加信息')
    
    # 支付信息
    registration_fee_paid = db.Column(db.Numeric(10, 2), default=0, comment='已付费用')
    is_paid = db.Column(db.Boolean, default=False, comment='是否已付费')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    event = db.relationship('Event', backref='registrations')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'event_id': self.event_id,
            'event_name': self.event.name if self.event else '',
            'registration_no': self.registration_no,
            'status': self.status,
            'contact_info': self.contact_info,
            'additional_info': self.additional_info,
            'registration_fee_paid': str(self.registration_fee_paid),
            'is_paid': self.is_paid,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Coach(db.Model):
    """教练模型"""
    __tablename__ = 'coaches'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, comment='教练姓名')
    specialization = db.Column(db.String(100), nullable=False, comment='专业领域')
    experience_years = db.Column(db.Integer, default=0, comment='从业年限')
    introduction = db.Column(db.Text, nullable=True, comment='教练介绍')
    avatar = db.Column(db.String(255), nullable=True, comment='教练头像')
    phone = db.Column(db.String(20), nullable=True, comment='联系电话')
    
    # 价格信息
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False, comment='每小时费用')
    rating = db.Column(db.Numeric(3, 2), default=5.0, comment='评分')
    total_sessions = db.Column(db.Integer, default=0, comment='总授课次数')
    
    # 状态
    is_active = db.Column(db.Boolean, default=True, comment='是否启用')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'experience_years': self.experience_years,
            'introduction': self.introduction,
            'avatar': self.avatar,
            'phone': self.phone,
            'hourly_rate': str(self.hourly_rate),
            'rating': str(self.rating),
            'total_sessions': self.total_sessions,
            'is_active': self.is_active
        }

class CoachBooking(db.Model):
    """教练预约模型"""
    __tablename__ = 'coach_bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_no = db.Column(db.String(50), unique=True, nullable=False, comment='预约编号')
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False, comment='场馆ID')



    
    # 预约信息
    booking_date = db.Column(db.Date, nullable=False, comment='预约日期')
    start_time = db.Column(db.Time, nullable=False, comment='开始时间')
    end_time = db.Column(db.Time, nullable=False, comment='结束时间')
    duration_hours = db.Column(db.Numeric(4, 2), nullable=False, comment='预约时长（小时）')
    total_price = db.Column(db.Numeric(10, 2), nullable=False, comment='总价格')
    
    # 状态和备注
    status = db.Column(db.String(20), default='upcoming', comment='预约状态')
    description = db.Column(db.Text, nullable=True, comment='预约备注')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='coach_bookings')
    coach = db.relationship('Coach', backref='bookings')
    venue = db.relationship('Venue', backref='coach_bookings')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'booking_no': self.booking_no,
            'user_id': self.user_id,
            'user_name': self.user.username if self.user else '',
            'coach_id': self.coach_id,
            'coach_name': self.coach.name if self.coach else '',
            'coach_specialization': self.coach.specialization if self.coach else '',
            'venue_id': self.venue_id,
            'venue_name': self.venue.name if self.venue else '',
            'date': self.booking_date.isoformat(),
            'time': f'{self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M")}',
            'duration': f'{self.duration_hours}小时',
            'price': str(self.total_price),
            'status': self.status,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class BookingShare(db.Model):
    """费用分摊模型"""
    __tablename__ = 'booking_shares'

    id = db.Column(db.Integer, primary_key=True)

    # 外键
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    event_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # 分摊信息
    share_amount = db.Column(db.Numeric(10, 2), nullable=False, comment='分摊金额')
    paid_amount = db.Column(db.Numeric(10, 2), default=0, comment='已付金额')
    is_paid = db.Column(db.Boolean, default=False, comment='是否已付清')

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 完全不定义任何关系，只定义基本字段
    # 我们将在查询时手动关联

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'event_name': self.event_name,
            'user_id': self.user_id,
            'share_amount': float(self.share_amount),
            'paid_amount': float(self.paid_amount),
            'is_paid': self.is_paid,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class BookingShareOld(db.Model):
    """预约分享模型（原版本）"""
    __tablename__ = 'booking_shares_old'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='分享ID')
    
    # 外键关联
    booking_id = db.Column(db.Integer, db.ForeignKey('coach_bookings.id', ondelete='CASCADE'), 
                          nullable=False, comment='预约ID')
    shared_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), 
                                 nullable=False, comment='分享者用户ID')
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), 
                                   nullable=True, comment='被分享者用户ID（私有分享时使用）')
    
    # 分享设置
    share_token = db.Column(db.String(64), unique=True, nullable=True, comment='分享令牌（公开分享时使用）')
    permission = db.Column(db.Enum(SharePermission), default=SharePermission.VIEW_ONLY, 
                          comment='分享权限')
    
    # 有效期设置
    expires_at = db.Column(db.DateTime, nullable=True, comment='过期时间')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    
    # 分享信息
    share_message = db.Column(db.String(255), comment='分享留言')
    view_count = db.Column(db.Integer, default=0, comment='查看次数')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    booking = db.relationship('CoachBooking', backref='shares_old', foreign_keys=[booking_id])
    shared_by_user = db.relationship('User', foreign_keys=[shared_by_user_id], 
                                   backref='shared_bookings_old', lazy='joined')
    shared_with_user = db.relationship('User', foreign_keys=[shared_with_user_id], 
                                     backref='received_shares_old', lazy='joined')
    
    def __repr__(self):
        return f'<BookingShareOld {self.id}: Booking {self.booking_id} shared by {self.shared_by_user_id}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'shared_by_user_id': self.shared_by_user_id,
            'shared_with_user_id': self.shared_with_user_id,
            'share_token': self.share_token,
            'permission': self.permission.value if self.permission else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active,
            'share_message': self.share_message,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # 关联数据
            'booking': self.booking.to_dict() if self.booking else None,
            'shared_by_user': self.shared_by_user.to_dict() if self.shared_by_user else None,
            'shared_with_user': self.shared_with_user.to_dict() if self.shared_with_user else None
        }
    
    def is_expired(self):
        """检查是否已过期"""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    def can_view(self, user_id):
        """检查用户是否有权限查看"""
        if not self.is_active:
            return False
        
        if self.is_expired():
            return False
        
        # 分享者可以查看
        if self.shared_by_user_id == user_id:
            return True
        
        # 指定用户可以查看
        if self.shared_with_user_id == user_id:
            return True
        
        # 通过分享令牌可以查看（公开分享）
        # 这里需要根据具体的令牌验证逻辑来实现
        return False
    
    def increment_view_count(self):
        """增加查看次数"""
        self.view_count += 1
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def create_share(cls, booking_id, shared_by_user_id, permission=SharePermission.VIEW_ONLY, 
                    shared_with_user_id=None, share_token=None, expires_at=None, share_message=None):
        """创建分享"""
        share = cls(
            booking_id=booking_id,
            shared_by_user_id=shared_by_user_id,
            shared_with_user_id=shared_with_user_id,
            permission=permission,
            share_token=share_token,
            expires_at=expires_at,
            share_message=share_message
        )
        return share
    
    @classmethod
    def get_user_shares(cls, user_id, include_received=True):
        """获取用户的所有分享（包括分享的和接收到的）"""
        query = cls.query.filter_by(is_active=True)
        
        if include_received:
            # 用户分享的或接收到的
            return query.filter(
                (cls.shared_by_user_id == user_id) | 
                (cls.shared_with_user_id == user_id)
            ).all()
        else:
            # 只获取用户分享的
            return query.filter_by(shared_by_user_id=user_id).all()
    
    @classmethod
    def find_by_token(cls, share_token):
        """通过令牌查找分享"""
        return cls.query.filter_by(share_token=share_token, is_active=True).first()
    
    @classmethod
    def find_by_booking_and_user(cls, booking_id, user_id):
        """查找特定预约的用户分享"""
        return cls.query.filter_by(
            booking_id=booking_id,
            shared_by_user_id=user_id,
            is_active=True
        ).first()

def get_current_user():
    pass


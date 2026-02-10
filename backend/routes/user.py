"""
用户中心API模块
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import func, desc, and_
from models import db, User, Booking, BookingStatus, Venue, VenueCategory, Activity, Event
from config import BaseConfig

# 创建蓝图
user_bp = Blueprint('user', __name__, url_prefix='/api/user')

def get_user_id_from_header():
    """从请求头获取用户ID"""
    user_id = request.headers.get('User-Id')
    if not user_id:
        return None
    try:
        return int(user_id)
    except (ValueError, TypeError):
        return None

@user_bp.route('/list', methods=['GET'])
def get_user_list():
    """
    获取用户列表
    ---
    tags:
      - 用户中心
    summary: 获取用户列表
    description: 获取用户列表，支持分页和搜索
    parameters:
      - name: page
        in: query
        description: 页码
        schema:
          type: integer
          default: 1
      - name: page_size
        in: query
        description: 每页数量
        schema:
          type: integer
          default: 20
      - name: username
        in: query
        description: 用户名搜索关键词
        schema:
          type: string
    responses:
      200:
        description: 获取成功
        content:
          application/json:
            schema:
              type: object
              properties:
                code:
                  type: integer
                  example: 0
                data:
                  type: object
                  properties:
                    list:
                      type: array
                      items:
                        $ref: '#/components/schemas/User'
                    total_records:
                      type: integer
                      example: 100
                    current_page:
                      type: integer
                      example: 1
                    total_pages:
                      type: integer
                      example: 5
                message:
                  type: string
                  example: "获取成功"
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        username = request.args.get('username', '')
        
        # 限制每页最大数量
        page_size = min(page_size, 100)
        
        # 构建查询
        query = User.query
        
        # 如果有用户名搜索条件
        if username:
            query = query.filter(User.username.contains(username))
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        users = query.order_by(User.created_at.desc())\
            .offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return jsonify({
            'code': 0,
            'data': {
                'list': [user.to_dict() for user in users],
                'total_records': total,
                'current_page': page,
                'total_pages': total_pages
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取用户列表失败: {str(e)}'
        }), 500

@user_bp.route('/profile', methods=['GET'])
def get_user_profile():
    """
    获取用户基本信息
    ---
    tags:
      - 用户中心
    summary: 获取用户基本信息
    description: 获取当前用户的个人信息
    responses:
      200:
        description: 获取成功
        content:
          application/json:
            schema:
              type: object
              properties:
                code:
                  type: integer
                  example: 0
                data:
                  $ref: '#/components/schemas/User'
                message:
                  type: string
                  example: "获取成功"
      401:
        description: 用户未登录
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'data': user.to_dict(),
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取用户信息失败: {str(e)}'
        }), 500

@user_bp.route('/profile', methods=['PUT'])
def update_user_profile():
    """
    更新用户基本信息
    ---
    tags:
      - 用户中心
    summary: 更新用户基本信息
    description: 更新当前用户的个人信息
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              nickname:
                type: string
                description: 昵称
              avatar:
                type: string
                description: 头像URL
              phone:
                type: string
                description: 手机号
              city:
                type: string
                description: 所在城市
              bio:
                type: string
                description: 个人简介
    responses:
      200:
        description: 更新成功
        content:
          application/json:
            schema:
              type: object
              properties:
                code:
                  type: integer
                  example: 0
                data:
                  $ref: '#/components/schemas/User'
                message:
                  type: string
                  example: "更新成功"
      400:
        description: 请求参数错误
      401:
        description: 用户未登录
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        data = request.get_json()
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404
        
        # 更新字段
        updatable_fields = ['nickname', 'avatar', 'phone', 'city', 'bio']
        for field in updatable_fields:
            if field in data and data[field] is not None:
                setattr(user, field, data[field])
        
        user.updated_at = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': user.to_dict(),
            'message': '更新成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新用户信息失败: {str(e)}'
        }), 500

@user_bp.route('/dashboard', methods=['GET'])
def get_user_dashboard():
    """
    获取用户仪表板数据
    ---
    tags:
      - 用户中心
    summary: 获取用户仪表板数据
    description: 获取用户在个人中心的统计和推荐数据
    responses:
      200:
        description: 获取成功
        content:
          application/json:
            schema:
              type: object
              properties:
                code:
                  type: integer
                  example: 0
                data:
                  type: object
                  properties:
                    total_bookings:
                      type: integer
                      description: 总预约数
                    upcoming_bookings:
                      type: integer
                      description: 即将到来的预约数
                    completed_bookings:
                      type: integer
                      description: 已完成预约数
                    favorite_venues:
                      type: integer
                      description: 收藏的场馆数
                    recent_activities:
                      type: array
                      items:
                        $ref: '#/components/schemas/Activity'
                      description: 最近的活动
                    recommended_venues:
                      type: array
                      items:
                        $ref: '#/components/schemas/Venue'
                      description: 推荐的场馆
                message:
                  type: string
                  example: "获取成功"
      401:
        description: 用户未登录
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 验证用户是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404
        
        # 获取预约统计
        total_bookings = Booking.query.filter_by(user_id=user_id).count()
        
        upcoming_bookings = Booking.query.filter(
            and_(
                Booking.user_id == user_id,
                Booking.booking_date >= datetime.now().date(),
                Booking.status.in_([BookingStatus.UPCOMING, BookingStatus.IN_PROGRESS])
            )
        ).count()
        
        completed_bookings = Booking.query.filter_by(
            user_id=user_id, status=BookingStatus.COMPLETED
        ).count()
        
        # 收藏的场馆数（这里简化处理，实际可以添加用户收藏表）
        favorite_venues = Venue.query.filter_by(is_active=True).count()
        
        # 获取最近的活动（简化处理，实际应该从数据库查询）
        recent_activities = Activity.query.filter_by(is_active=True)\
            .order_by(Activity.start_date.desc())\
            .limit(5)\
            .all()
        
        # 获取推荐的场馆（基于用户历史预约的场馆类型）
        recommended_venues = Venue.query.filter_by(is_active=True)\
            .order_by(desc(Venue.price_per_hour))\
            .limit(6)\
            .all()
        
        dashboard_data = {
            'total_bookings': total_bookings,
            'upcoming_bookings': upcoming_bookings,
            'completed_bookings': completed_bookings,
            'favorite_venues': favorite_venues,
            'recent_activities': [activity.to_dict() for activity in recent_activities],
            'recommended_venues': [venue.to_dict() for venue in recommended_venues]
        }
        
        return jsonify({
            'code': 0,
            'data': dashboard_data,
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取仪表板数据失败: {str(e)}'
        }), 500

@user_bp.route('/my-activities', methods=['GET'])
def get_user_activities():
    """
    获取我的赛事活动
    ---
    tags:
      - 用户中心
    summary: 获取我的赛事活动
    description: 获取用户参与的赛事活动记录
    parameters:
      - name: page
        in: query
        description: 页码
        schema:
          type: integer
          default: 1
      - name: page_size
        in: query
        description: 每页数量
        schema:
          type: integer
          default: 20
      - name: status
        in: query
        description: 状态筛选
        schema:
          type: string
          enum: [upcoming, ongoing, completed]
    responses:
      200:
        description: 获取成功
        content:
          application/json:
            schema:
              type: object
              properties:
                code:
                  type: integer
                  example: 0
                data:
                  type: object
                  properties:
                    activities:
                      type: array
                      items:
                        $ref: '#/components/schemas/Activity'
                    pagination:
                      type: object
                      properties:
                        current_page:
                          type: integer
                          example: 1
                        page_size:
                          type: integer
                          example: 20
                        total:
                          type: integer
                          example: 100
                        total_pages:
                          type: integer
                          example: 5
                message:
                  type: string
                  example: "获取成功"
      401:
        description: 用户未登录
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', BaseConfig.PAGE_SIZE, type=int)
        status_filter = request.args.get('status', '').strip()
        
        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        
        # 构建查询
        query = Activity.query.filter_by(is_active=True)
        
        # 状态筛选
        if status_filter:
            now = datetime.now().date()
            if status_filter == 'upcoming':
                query = query.filter(Activity.start_date > now)
            elif status_filter == 'ongoing':
                query = query.filter(
                    Activity.start_date <= now,
                    Activity.end_date >= now
                )
            elif status_filter == 'completed':
                query = query.filter(Activity.end_date < now)
            else:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'无效的状态值: {status_filter}'
                }), 400
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        activities = query.order_by(Activity.start_date.desc())\
            .offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return jsonify({
            'code': 0,
            'data': {
                'activities': [activity.to_dict() for activity in activities],
                'pagination': {
                    'current_page': page,
                    'page_size': page_size,
                    'total': total,
                    'total_pages': total_pages
                }
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取活动列表失败: {str(e)}'
        }), 500

@user_bp.route('/my-events', methods=['GET'])
def get_user_events():
    """
    获取我的赛事
    ---
    tags:
      - 用户中心
    summary: 获取我的赛事
    description: 获取用户参与或关注的赛事列表
    parameters:
      - name: page
        in: query
        description: 页码
        schema:
          type: integer
          default: 1
      - name: page_size
        in: query
        description: 每页数量
        schema:
          type: integer
          default: 20
    responses:
      200:
        description: 获取成功
        content:
          application/json:
            schema:
              type: object
              properties:
                code:
                  type: integer
                  example: 0
                data:
                  type: object
                  properties:
                    events:
                      type: array
                      items:
                        $ref: '#/components/schemas/Event'
                    pagination:
                      type: object
                      properties:
                        current_page:
                          type: integer
                          example: 1
                        page_size:
                          type: integer
                          example: 20
                        total:
                          type: integer
                          example: 100
                        total_pages:
                          type: integer
                          example: 5
                message:
                  type: string
                  example: "获取成功"
      401:
        description: 用户未登录
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', BaseConfig.PAGE_SIZE, type=int)
        
        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        
        # 构建查询（简化处理，实际应该根据用户参与表查询）
        query = Event.query.filter_by(is_active=True)
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        events = query.order_by(Event.created_at.desc())\
            .offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return jsonify({
            'code': 0,
            'data': {
                'events': [event.to_dict() for event in events],
                'pagination': {
                    'current_page': page,
                    'page_size': page_size,
                    'total': total,
                    'total_pages': total_pages
                }
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取赛事列表失败: {str(e)}'
        }), 500

@user_bp.route('/statistics', methods=['GET'])
def get_user_statistics():
    """
    获取用户统计数据
    ---
    tags:
      - 用户中心
    summary: 获取用户统计数据
    description: 获取用户在个人中心的详细统计数据
    responses:
      200:
        description: 获取成功
        content:
          application/json:
            schema:
              type: object
              properties:
                code:
                  type: integer
                  example: 0
                data:
                  type: object
                  properties:
                    booking_stats:
                      type: object
                      properties:
                        total:
                          type: integer
                        pending:
                          type: integer
                        confirmed:
                          type: integer
                        completed:
                          type: integer
                        cancelled:
                          type: integer
                        this_month:
                          type: integer
                        this_year:
                          type: integer
                    venue_stats:
                      type: object
                      properties:
                        total_venues_visited:
                          type: integer
                        favorite_categories:
                          type: array
                          items:
                            type: object
                            properties:
                              category_name:
                                type: string
                              count:
                                type: integer
                    consumption_stats:
                      type: object
                      properties:
                        total_spent:
                          type: number
                        avg_booking_amount:
                          type: number
                        this_month_spent:
                          type: number
                        this_year_spent:
                          type: number
                    activity_stats:
                      type: object
                      properties:
                        total_activities:
                          type: integer
                        upcoming_activities:
                          type: integer
                        completed_activities:
                          type: integer
                message:
                  type: string
                  example: "获取成功"
      401:
        description: 用户未登录
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 验证用户是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404
        
        now = datetime.now()
        this_month_start = datetime(now.year, now.month, 1).date()
        this_year_start = datetime(now.year, 1, 1).date()
        
        # 预约统计
        total_bookings = Booking.query.filter_by(user_id=user_id).count()
        pending_bookings = Booking.query.filter_by(
            user_id=user_id, status=BookingStatus.UPCOMING
        ).count()
        confirmed_bookings = Booking.query.filter_by(
            user_id=user_id, status=BookingStatus.CONFIRMED
        ).count()
        completed_bookings = Booking.query.filter_by(
            user_id=user_id, status=BookingStatus.COMPLETED
        ).count()
        cancelled_bookings = Booking.query.filter_by(
            user_id=user_id, status=BookingStatus.CANCELLED
        ).count()
        this_month_bookings = Booking.query.filter(
            Booking.user_id == user_id,
            Booking.booking_date >= this_month_start
        ).count()
        this_year_bookings = Booking.query.filter(
            Booking.user_id == user_id,
            Booking.booking_date >= this_year_start
        ).count()
        
        booking_stats = {
            'total': total_bookings,
            'pending': pending_bookings,
            'confirmed': confirmed_bookings,
            'completed': completed_bookings,
            'cancelled': cancelled_bookings,
            'this_month': this_month_bookings,
            'this_year': this_year_bookings
        }
        
        # 场馆统计（简化处理）
        total_venues_visited = db.session.query(func.count(func.distinct(Booking.venue_id))).filter(
            Booking.user_id == user_id,
            Booking.status == BookingStatus.COMPLETED
        ).scalar() or 0
        
        # 获取用户喜欢的场馆类型（基于预约历史）
        favorite_categories = db.session.query(
            VenueCategory.name,
            func.count(Booking.id).label('count')
        ).join(
            Venue, Venue.category_id == VenueCategory.id
        ).join(
            Booking, Booking.venue_id == Venue.id
        ).filter(
            Booking.user_id == user_id,
            Booking.status == BookingStatus.COMPLETED
        ).group_by(
            VenueCategory.id, VenueCategory.name
        ).order_by(desc('count')).limit(5).all()
        
        venue_stats = {
            'total_venues_visited': total_venues_visited,
            'favorite_categories': [
                {'category_name': cat_name, 'count': count}
                for cat_name, count in favorite_categories
            ]
        }
        
        # 消费统计
        total_spent = db.session.query(func.sum(Booking.total_price)).filter(
            Booking.user_id == user_id,
            Booking.status == BookingStatus.COMPLETED
        ).scalar() or 0
        
        avg_booking_amount = db.session.query(func.avg(Booking.total_price)).filter(
            Booking.user_id == user_id,
            Booking.status == BookingStatus.COMPLETED
        ).scalar() or 0
        
        this_month_spent = db.session.query(func.sum(Booking.total_price)).filter(
            Booking.user_id == user_id,
            Booking.status == BookingStatus.COMPLETED,
            Booking.booking_date >= this_month_start
        ).scalar() or 0
        
        this_year_spent = db.session.query(func.sum(Booking.total_price)).filter(
            Booking.user_id == user_id,
            Booking.status == BookingStatus.COMPLETED,
            Booking.booking_date >= this_year_start
        ).scalar() or 0
        
        consumption_stats = {
            'total_spent': float(total_spent),
            'avg_booking_amount': float(avg_booking_amount),
            'this_month_spent': float(this_month_spent),
            'this_year_spent': float(this_year_spent)
        }
        
        # 活动统计
        total_activities = Activity.query.filter_by(is_active=True).count()
        upcoming_activities = Activity.query.filter(
            Activity.start_date > now.date()
        ).count()
        completed_activities = Activity.query.filter(
            Activity.end_date < now.date()
        ).count()
        
        activity_stats = {
            'total_activities': total_activities,
            'upcoming_activities': upcoming_activities,
            'completed_activities': completed_activities
        }
        
        statistics = {
            'booking_stats': booking_stats,
            'venue_stats': venue_stats,
            'consumption_stats': consumption_stats,
            'activity_stats': activity_stats
        }
        
        return jsonify({
            'code': 0,
            'data': statistics,
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取统计信息失败: {str(e)}'
        }), 500

@user_bp.route('/bookings', methods=['GET'])
def get_user_bookings():
    """
    获取用户预约记录
    ---
    tags:
      - 用户中心
    summary: 获取用户预约记录
    description: 获取当前用户的预约记录列表
    parameters:
      - name: page
        in: query
        description: 页码
        schema:
          type: integer
          default: 1
      - name: page_size
        in: query
        description: 每页数量
        schema:
          type: integer
          default: 20
      - name: status
        in: query
        description: 状态筛选
        schema:
          type: string
          enum: [pending, confirmed, completed, cancelled]
    responses:
      200:
        description: 获取成功
        content:
          application/json:
            schema:
              type: object
              properties:
                code:
                  type: integer
                  example: 0
                data:
                  type: object
                  properties:
                    bookings:
                      type: array
                      items:
                        $ref: '#/components/schemas/Booking'
                    pagination:
                      type: object
                      properties:
                        page:
                          type: integer
                        page_size:
                          type: integer
                        total:
                          type: integer
                        pages:
                          type: integer
                message:
                  type: string
                  example: "获取成功"
      401:
        description: 用户未登录
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        status = request.args.get('status')
        
        # 构建查询
        query = Booking.query.filter_by(user_id=user_id)
        
        # 状态筛选
        if status:
            try:
                booking_status = getattr(BookingStatus, status.upper())
                query = query.filter_by(status=booking_status)
            except AttributeError:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'无效的状态: {status}'
                }), 400
        
        # 按预约日期降序排序
        query = query.order_by(desc(Booking.booking_date), desc(Booking.created_at))
        
        # 分页
        pagination = query.paginate(
            page=page, 
            per_page=page_size, 
            error_out=False
        )
        
        bookings = pagination.items
        
        return jsonify({
            'code': 0,
            'data': {
                'bookings': [booking.to_dict() for booking in bookings],
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': pagination.total,
                    'pages': pagination.pages
                }
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取预约记录失败: {str(e)}'
        }), 500

@user_bp.route('/create', methods=['POST'])
def create_user():
    """
    创建用户
    ---
    tags:
      - 用户管理
    summary: 创建新用户
    description: 创建新的用户账号
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
                description: 用户名
              password:
                type: string
                description: 密码
              email:
                type: string
                description: 邮箱
              phone:
                type: string
                description: 手机号
              real_name:
                type: string
                description: 真实姓名
              city:
                type: string
                description: 城市
    responses:
      200:
        description: 创建成功
      400:
        description: 请求参数错误
      409:
        description: 用户名已存在
    """
    try:
        # 获取用户ID（管理员权限检查可以在这里添加）
        user_id = 1  # 默认用户ID，无需验证
        
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['username', 'password', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'缺少必需字段: {field}'
                }), 400
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({
                'code': 409,
                'data': None,
                'message': '用户名已存在'
            }), 409
        
        # 检查邮箱是否已存在
        if data.get('email'):
            existing_email = User.query.filter_by(email=data['email']).first()
            if existing_email:
                return jsonify({
                    'code': 409,
                    'data': None,
                    'message': '邮箱已存在'
                }), 409
        
        # 创建用户
        user = User(
            username=data['username'],
            password=data['password'],  # 注意：实际应用中需要加密
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            real_name=data.get('real_name', ''),
            city=data.get('city', ''),
            is_active=True
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': user.to_dict(),
            'message': '用户创建成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建用户失败: {str(e)}'
        }), 500

@user_bp.route('/update', methods=['POST'])
def update_user():
    """
    更新用户
    ---
    tags:
      - 用户管理
    summary: 更新用户信息
    description: 更新用户基本信息
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              id:
                type: integer
                description: 用户ID
              username:
                type: string
                description: 用户名
              email:
                type: string
                description: 邮箱
              phone:
                type: string
                description: 手机号
              real_name:
                type: string
                description: 真实姓名
              city:
                type: string
                description: 城市
              is_active:
                type: boolean
                description: 是否激活
    responses:
      200:
        description: 更新成功
      400:
        description: 请求参数错误
      404:
        description: 用户不存在
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        data = request.get_json()
        target_user_id = data.get('id')
        
        if not target_user_id:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '用户ID不能为空'
            }), 400
        
        # 查找用户
        user = User.query.get(target_user_id)
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404
        
        # 更新字段（只更新允许的字段）
        updateable_fields = ['username', 'email', 'phone', 'real_name', 'city', 'is_active']
        for field in updateable_fields:
            if field in data:
                if field == 'is_active' and isinstance(data[field], bool):
                    user.is_active = data[field]
                elif field != 'is_active':
                    setattr(user, field, data[field])
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': user.to_dict(),
            'message': '用户更新成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新用户失败: {str(e)}'
        }), 500

@user_bp.route('/delete', methods=['POST'])
def delete_user():
    """
    删除用户
    ---
    tags:
      - 用户管理
    summary: 删除用户
    description: 删除用户（软删除，将is_active设置为false）
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              id:
                type: integer
                description: 用户ID
    responses:
      200:
        description: 删除成功
      404:
        description: 用户不存在
      403:
        description: 无权限删除
    """
    try:
        # 获取用户ID（管理员权限检查可以在这里添加）
        user_id = 1  # 默认用户ID，无需验证
        
        data = request.get_json()
        target_user_id = data.get('id')
        
        if not target_user_id:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '用户ID不能为空'
            }), 400
        
        # 查找用户
        user = User.query.get(target_user_id)
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404
        
        # 防止删除自己
        if user.id == user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '不能删除自己的账号'
            }), 403
        
        # 软删除
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': None,
            'message': '用户删除成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除用户失败: {str(e)}'
        }), 500
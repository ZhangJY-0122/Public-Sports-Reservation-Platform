"""
教练管理API模块
"""

from datetime import datetime, date, time
from flask import Blueprint, request, jsonify
from sqlalchemy import and_
from models import db, Coach, CoachBooking, User, Venue
from config import BaseConfig

# 创建蓝图
coaches_bp = Blueprint('coaches', __name__, url_prefix='/api/coaches')

# 移除用户权限验证，直接操作

def time_to_minutes(time_obj):
    """将时间对象转换为分钟数"""
    if isinstance(time_obj, str):
        time_obj = datetime.strptime(time_obj, '%H:%M').time()
    return time_obj.hour * 60 + time_obj.minute

def minutes_to_time(minutes):
    """将分钟数转换为时间对象"""
    hours = minutes // 60
    mins = minutes % 60
    return time(hours, mins)

def generate_time_slots(start_hour=8, end_hour=22, slot_duration=60):
    """生成时间槽"""
    slots = []
    current_minutes = start_hour * 60
    end_minutes = end_hour * 60
    
    while current_minutes + slot_duration <= end_minutes:
        start_time = minutes_to_time(current_minutes)
        end_time = minutes_to_time(current_minutes + slot_duration)
        slots.append({
            'start_time': start_time.strftime('%H:%M'),
            'end_time': end_time.strftime('%H:%M'),
            'duration': f'{slot_duration}分钟'
        })
        current_minutes += slot_duration
    
    return slots

@coaches_bp.route('/list', methods=['GET'])
def list_coaches():
    """
    获取教练列表
    ---
    tags:
      - 教练管理
    summary: 获取教练列表
    description: 分页获取教练列表，支持专业筛选
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
      - name: specialization
        in: query
        description: 专业筛选
        schema:
          type: string
    responses:
      200:
        description: 获取成功
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', BaseConfig.PAGE_SIZE, type=int)
        specialization_filter = request.args.get('specialization', '').strip()
        
        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        
        # 构建查询
        query = Coach.query.filter(Coach.is_active == True)
        
        # 专业筛选
        if specialization_filter:
            query = query.filter(Coach.specialization.contains(specialization_filter))
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        coaches = query.order_by(Coach.rating.desc(), Coach.total_sessions.desc())\
            .offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return jsonify({
            'code': 0,
            'data': {
                'coaches': [coach.to_dict() for coach in coaches],
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
            'message': f'获取教练列表失败: {str(e)}'
        }), 500

@coaches_bp.route('/<int:coach_id>', methods=['GET'])
def get_coach_detail(coach_id):
    """
    获取教练详情
    ---
    tags:
      - 教练管理
    summary: 获取教练详情
    description: 根据教练ID获取详细信息
    parameters:
      - name: coach_id
        in: path
        required: true
        description: 教练ID
        schema:
          type: integer
    responses:
      200:
        description: 获取成功
      404:
        description: 教练不存在
    """
    try:
        coach = Coach.query.get(coach_id)
        
        if not coach:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '教练不存在'
            }), 404
        
        # 获取预约统计
        booking_stats = {
            'total_bookings': CoachBooking.query.filter_by(coach_id=coach_id).count(),
            'upcoming': CoachBooking.query.filter_by(coach_id=coach_id, status='upcoming').count(),
            'completed': CoachBooking.query.filter_by(coach_id=coach_id, status='completed').count(),
            'cancelled': CoachBooking.query.filter_by(coach_id=coach_id, status='cancelled').count()
        }
        
        return jsonify({
            'code': 0,
            'data': {
                'coach': coach.to_dict(),
                'booking_stats': booking_stats
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取教练详情失败: {str(e)}'
        }), 500

@coaches_bp.route('/<int:coach_id>/availability', methods=['GET'])
def get_coach_availability(coach_id):
    """
    查询教练空闲时段
    ---
    tags:
      - 教练管理
    summary: 查询空闲时段
    description: 查询指定教练在指定日期的空闲时段
    parameters:
      - name: coach_id
        in: path
        required: true
        description: 教练ID
        schema:
          type: integer
      - name: date
        in: query
        required: true
        description: 查询日期 (YYYY-MM-DD)
        schema:
          type: string
          format: date
      - name: duration
        in: query
        description: 预约时长（分钟），默认60
        schema:
          type: integer
          default: 60
    responses:
      200:
        description: 获取成功
      404:
        description: 教练不存在
    """
    try:
        # 验证教练是否存在
        coach = Coach.query.get(coach_id)
        if not coach:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '教练不存在'
            }), 404
        
        # 获取查询参数
        date_str = request.args.get('date')
        duration = request.args.get('duration', 60, type=int)
        
        if not date_str:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '请提供查询日期'
            }), 400
        
        try:
            query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '日期格式不正确，请使用YYYY-MM-DD格式'
            }), 400
        
        # 检查日期不能是过去日期
        if query_date < date.today():
            return jsonify({
                'code': 400,
                'data': None,
                'message': '不能查询过去日期的空闲时段'
            }), 400
        
        # 生成所有可能的时间槽
        all_slots = generate_time_slots(slot_duration=duration)
        
        # 查询该教练在该日期的已预约时段
        existing_bookings = CoachBooking.query.filter(
            and_(
                CoachBooking.coach_id == coach_id,
                CoachBooking.booking_date == query_date,
                CoachBooking.status.in_(['upcoming', 'confirmed'])
            )
        ).all()
        
        # 标记已占用时段
        available_slots = []
        for slot in all_slots:
            is_available = True
            slot_start_minutes = time_to_minutes(slot['start_time'])
            slot_end_minutes = time_to_minutes(slot['end_time'])
            
            for booking in existing_bookings:
                booking_start_minutes = time_to_minutes(booking.start_time.strftime('%H:%M'))
                booking_end_minutes = time_to_minutes(booking.end_time.strftime('%H:%M'))
                
                # 检查时间冲突
                if (slot_start_minutes < booking_end_minutes and 
                    slot_end_minutes > booking_start_minutes):
                    is_available = False
                    break
            
            if is_available:
                available_slots.append({
                    **slot,
                    'available': True
                })
            else:
                available_slots.append({
                    **slot,
                    'available': False
                })
        
        return jsonify({
            'code': 0,
            'data': {
                'coach': coach.to_dict(),
                'date': query_date.isoformat(),
                'duration': duration,
                'total_slots': len(all_slots),
                'available_slots': len([s for s in available_slots if s['available']]),
                'slots': available_slots
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'查询空闲时段失败: {str(e)}'
        }), 500

#预约教练
@coaches_bp.route('/<int:coach_id>/book', methods=['POST'])
def book_coach(coach_id):
    """
    预约教练
    ---
    tags:
      - 教练管理
    summary: 预约教练
    description: 预约指定教练的特定时间段
    parameters:
      - name: coach_id
        in: path
        required: true
        description: 教练ID
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              venue_id:
                type: integer
                description: 场馆ID
                required: true
              date:
                type: string
                format: date
                description: 预约日期
                required: true
              start_time:
                type: string
                format: time
                description: 开始时间 (HH:MM)
                required: true
              end_time:
                type: string
                format: time
                description: 结束时间 (HH:MM)
                required: true
              description:
                type: string
                description: 预约备注
    responses:
      200:
        description: 预约成功
      400:
        description: 请求参数错误
      404:
        description: 教练或场馆不存在
      409:
        description: 时间段已被预约
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
        
        # 验证教练是否存在
        coach = Coach.query.get(coach_id)
        if not coach:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '教练不存在'
            }), 404
        
        # 获取请求数据
        data = request.get_json() or {}
        
        # 验证必需参数（包括venue_id）
        required_fields = ['venue_id', 'date', 'start_time', 'end_time']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'缺少必需参数: {field}'
                }), 400
        
        # 验证场馆是否存在
        venue_id = data['venue_id']
        if not isinstance(venue_id, int) or venue_id <= 0:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '场馆ID无效'
            }), 400
        
        venue = Venue.query.get(venue_id)
        if not venue:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '场馆不存在'
            }), 404
        
        # 解析日期和时间
        try:
            booking_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            start_time = datetime.strptime(data['start_time'], '%H:%M').time()
            end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        except ValueError:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '日期或时间格式不正确'
            }), 400
        
        # 检查日期不能是过去日期
        if booking_date < date.today():
            return jsonify({
                'code': 400,
                'data': None,
                'message': '不能预约过去日期'
            }), 400
        
        # 检查时间逻辑
        if end_time <= start_time:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '结束时间必须晚于开始时间'
            }), 400
        
        # 计算时长和价格
        duration_delta = datetime.combine(date.min, end_time) - datetime.combine(date.min, start_time)
        duration_hours = duration_delta.total_seconds() / 3600
        
        # 计算价格（基础价格 + 场馆额外费用）
        base_price = float(coach.hourly_rate)
        venue_price = float(venue.price_per_hour) if venue.price_per_hour else 0
        total_price = (base_price + venue_price) * duration_hours
        
        # 生成预约编号
        booking_no = f"CB{datetime.now().strftime('%Y%m%d%H%M%S')}{user_id:04d}{coach_id:03d}{venue_id:03d}"
        
        # 创建预约记录
        booking = CoachBooking(
            booking_no=booking_no,
            user_id=user_id,
            coach_id=coach_id,
            venue_id=venue_id,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            duration_hours=duration_hours,
            total_price=total_price,
            description=data.get('description', ''),
            status='upcoming'
        )
        
        db.session.add(booking)
        
        # 更新教练授课次数
        coach.total_sessions += 1
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': booking.to_dict(),
            'message': '教练预约成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'预约失败: {str(e)}'
        }), 500

@coaches_bp.route('/admin/bookings', methods=['GET'])
def get_all_coach_bookings():
    """
    获取所有教练预约（管理员接口）
    ---
    tags:
      - 教练管理
    summary: 获取所有教练预约
    description: 管理员查看所有教练的所有预约记录，支持多维度筛选
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
      - name: coach_id
        in: query
        description: 教练ID筛选
        schema:
          type: integer
      - name: coach_name
        in: query
        description: 教练姓名筛选
        schema:
          type: string
      - name: status
        in: query
        description: 状态筛选
        schema:
          type: string
          enum: [upcoming, confirmed, completed, cancelled]
      - name: user_id
        in: query
        description: 用户ID筛选
        schema:
          type: integer
      - name: booking_date_from
        in: query
        description: 预约开始日期筛选
        schema:
          type: string
          format: date
      - name: booking_date_to
        in: query
        description: 预约结束日期筛选
        schema:
          type: string
          format: date
    responses:
      200:
        description: 获取成功
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', BaseConfig.PAGE_SIZE, type=int)
        coach_id_filter = request.args.get('coach_id', type=int)
        coach_name_filter = request.args.get('coach_name', '').strip()
        status_filter = request.args.get('status', '').strip()
        user_id_filter = request.args.get('user_id', type=int)
        date_from_filter = request.args.get('booking_date_from', '').strip()
        date_to_filter = request.args.get('booking_date_to', '').strip()
        
        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        
        # 构建查询
        query = CoachBooking.query
        
        # 教练ID筛选
        if coach_id_filter:
            query = query.filter(CoachBooking.coach_id == coach_id_filter)
        
        # 教练姓名筛选
        if coach_name_filter:
            query = query.join(Coach).filter(Coach.name.contains(coach_name_filter))
        
        # 状态筛选
        if status_filter:
            query = query.filter(CoachBooking.status == status_filter)
        
        # 用户ID筛选
        if user_id_filter:
            query = query.filter(CoachBooking.user_id == user_id_filter)
        
        # 日期范围筛选
        if date_from_filter:
            try:
                date_from = datetime.strptime(date_from_filter, '%Y-%m-%d').date()
                query = query.filter(CoachBooking.booking_date >= date_from)
            except ValueError:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '开始日期格式不正确，请使用YYYY-MM-DD格式'
                }), 400
        
        if date_to_filter:
            try:
                date_to = datetime.strptime(date_to_filter, '%Y-%m-%d').date()
                query = query.filter(CoachBooking.booking_date <= date_to)
            except ValueError:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '结束日期格式不正确，请使用YYYY-MM-DD格式'
                }), 400
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        bookings = query.order_by(CoachBooking.booking_date.desc(), CoachBooking.start_time.desc())\
            .offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        # 获取统计数据
        stats = {
            'total_bookings': total,
            'total_revenue': sum(booking.total_price for booking in bookings if booking.status != 'cancelled'),
            'status_breakdown': {
                'upcoming': CoachBooking.query.filter_by(status='upcoming').count(),
                'confirmed': CoachBooking.query.filter_by(status='confirmed').count(),
                'completed': CoachBooking.query.filter_by(status='completed').count(),
                'cancelled': CoachBooking.query.filter_by(status='cancelled').count()
            },
            'coach_breakdown': {}
        }
        
        # 教练维度统计
        coach_stats = db.session.query(
            CoachBooking.coach_id,
            Coach.name,
            CoachBooking.status,
            db.func.count(CoachBooking.id).label('count')
        ).join(Coach, CoachBooking.coach_id == Coach.id)\
        .group_by(CoachBooking.coach_id, Coach.name, CoachBooking.status)\
        .all()
        
        for coach_id, coach_name, status, count in coach_stats:
            if coach_id not in stats['coach_breakdown']:
                stats['coach_breakdown'][coach_id] = {
                    'coach_name': coach_name,
                    'total_bookings': 0,
                    'status_breakdown': {}
                }
            stats['coach_breakdown'][coach_id]['total_bookings'] += count
            stats['coach_breakdown'][coach_id]['status_breakdown'][status] = count
        
        return jsonify({
            'code': 0,
            'data': {
                'bookings': [booking.to_dict() for booking in bookings],
                'pagination': {
                    'current_page': page,
                    'page_size': page_size,
                    'total': total,
                    'total_pages': total_pages
                },
                'statistics': stats
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取教练预约列表失败: {str(e)}'
        }), 500

@coaches_bp.route('/my-bookings', methods=['GET'])
def get_my_bookings():
    """
    获取我的教练预约
    ---
    tags:
      - 教练管理
    summary: 获取我的预约
    description: 获取当前用户的教练预约列表
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
          enum: [upcoming, confirmed, completed, cancelled]
    responses:
      200:
        description: 获取成功
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', BaseConfig.PAGE_SIZE, type=int)
        status_filter = request.args.get('status', '').strip()
        
        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        
        # 构建查询
        user_id = 1  # 默认用户ID，无需验证
        query = CoachBooking.query.filter_by(user_id=user_id)
        
        # 状态筛选
        if status_filter:
            query = query.filter(CoachBooking.status == status_filter)
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        bookings = query.order_by(CoachBooking.booking_date.desc(), CoachBooking.start_time.desc())\
            .offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return jsonify({
            'code': 0,
            'data': {
                'bookings': [booking.to_dict() for booking in bookings],
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
            'message': f'获取预约列表失败: {str(e)}'
        }), 500

@coaches_bp.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking_detail(booking_id):
    """
    获取教练预约详情
    ---
    tags:
      - 教练管理
    summary: 获取预约详情
    description: 获取指定预约的详细信息
    parameters:
      - name: booking_id
        in: path
        required: true
        description: 预约ID
        schema:
          type: integer
    responses:
      200:
        description: 获取成功
      404:
        description: 预约不存在
    """
    try:
        # 获取预约记录
        user_id = 1  # 默认用户ID，无需验证
        booking = CoachBooking.query.get(booking_id)
        
        if not booking:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '预约记录不存在'
            }), 404
        
        # 检查权限（只能查看自己的预约）
        # 移除权限检查，直接返回数据
        
        return jsonify({
            'code': 0,
            'data': booking.to_dict(),
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取预约详情失败: {str(e)}'
        }), 500

@coaches_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
def cancel_coach_booking(booking_id):
    """
    取消教练预约
    ---
    tags:
      - 教练管理
    summary: 取消预约
    description: 取消指定的教练预约
    parameters:
      - name: booking_id
        in: path
        required: true
        description: 预约ID
        schema:
          type: integer
    responses:
      200:
        description: 取消成功
    """
    try:
        # 获取预约记录
        user_id = 1  # 默认用户ID，无需验证
        booking = CoachBooking.query.get(booking_id)
        
        if not booking:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '预约记录不存在'
            }), 404
        
        # 检查权限（只能取消自己的预约）
        # 移除权限检查，直接允许操作
        
        # 检查状态
        if booking.status in ['completed', 'cancelled']:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '无法取消已完成或已取消的预约'
            }), 400
        
        # 检查预约时间（不能取消已开始或已过的预约）
        now = datetime.now()
        booking_datetime = datetime.combine(booking.booking_date, booking.start_time)
        
        if booking_datetime <= now:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '无法取消已开始或已过的预约'
            }), 400
        
        # 取消预约
        booking.status = 'cancelled'
        
        # 更新教练授课次数
        if booking.coach:
            booking.coach.total_sessions = max(0, booking.coach.total_sessions - 1)
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': booking.to_dict(),
            'message': '预约已取消'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'取消预约失败: {str(e)}'
        }), 500

@coaches_bp.route('/', methods=['POST'])
def create_coach():
    """
    创建教练
    ---
    tags:
      - 教练管理
    summary: 创建教练
    description: 创建新的教练信息
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: 教练姓名
                required: true
              specialization:
                type: string
                description: 专业领域
                required: true
              experience_years:
                type: integer
                description: 从业年限
                default: 0
              introduction:
                type: string
                description: 教练介绍
              avatar:
                type: string
                description: 教练头像
              phone:
                type: string
                description: 联系电话
              hourly_rate:
                type: number
                format: float
                description: 每小时费用
                required: true
              rating:
                type: number
                format: float
                description: 评分
                default: 5.0
    responses:
      201:
        description: 创建成功
      400:
        description: 请求参数错误
      409:
        description: 教练已存在
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取请求数据
        data = request.get_json() or {}
        
        # 验证必需参数
        required_fields = ['name', 'specialization', 'hourly_rate']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'缺少必需参数: {field}'
                }), 400
        
        # 验证教练姓名长度
        name = data['name'].strip()
        if len(name) < 1 or len(name) > 50:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '教练姓名长度必须在1-50字符之间'
            }), 400
        
        # 验证专业领域长度
        specialization = data['specialization'].strip()
        if len(specialization) < 1 or len(specialization) > 100:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '专业领域长度必须在1-100字符之间'
            }), 400
        
        # 验证价格格式
        try:
            hourly_rate = float(data['hourly_rate'])
            if hourly_rate <= 0:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '每小时费用必须大于0'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'code': 400,
                'data': None,
                'message': '每小时费用格式不正确'
            }), 400
        
        # 验证从业年限
        experience_years = data.get('experience_years', 0)
        if experience_years is not None:
            try:
                experience_years = int(experience_years)
                if experience_years < 0:
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '从业年限不能为负数'
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '从业年限必须是整数'
                }), 400
        
        # 验证评分
        rating = data.get('rating', 5.0)
        if rating is not None:
            try:
                rating = float(rating)
                if rating < 0 or rating > 5:
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '评分必须在0-5之间'
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '评分格式不正确'
                }), 400
        
        # 验证手机号格式（如果提供）
        phone = data.get('phone', '').strip()
        if phone and not phone.isdigit():
            return jsonify({
                'code': 400,
                'data': None,
                'message': '联系电话只能包含数字'
            }), 400
        
        # 创建教练记录
        coach = Coach(
            name=name,
            specialization=specialization,
            experience_years=experience_years or 0,
            introduction=data.get('introduction', '').strip(),
            avatar=data.get('avatar', '').strip(),
            phone=phone,
            hourly_rate=hourly_rate,
            rating=rating,
            total_sessions=0,
            is_active=True
        )
        
        db.session.add(coach)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': coach.to_dict(),
            'message': '教练创建成功'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建教练失败: {str(e)}'
        }), 500

@coaches_bp.route('/<int:coach_id>', methods=['PUT'])
def update_coach(coach_id):
    """
    更新教练信息
    ---
    tags:
      - 教练管理
    summary: 更新教练
    description: 更新指定教练的信息
    parameters:
      - name: coach_id
        in: path
        required: true
        description: 教练ID
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: 教练姓名
              specialization:
                type: string
                description: 专业领域
              experience_years:
                type: integer
                description: 从业年限
              introduction:
                type: string
                description: 教练介绍
              avatar:
                type: string
                description: 教练头像
              phone:
                type: string
                description: 联系电话
              hourly_rate:
                type: number
                format: float
                description: 每小时费用
              rating:
                type: number
                format: float
                description: 评分
              is_active:
                type: boolean
                description: 是否启用
    responses:
      200:
        description: 更新成功
      400:
        description: 请求参数错误
      404:
        description: 教练不存在
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 验证教练是否存在
        coach = Coach.query.get(coach_id)
        if not coach:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '教练不存在'
            }), 404
        
        # 获取请求数据
        data = request.get_json() or {}
        
        # 验证并更新字段
        updated_fields = []
        
        # 更新教练姓名
        if 'name' in data:
            name = data['name'].strip()
            if len(name) < 1 or len(name) > 50:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '教练姓名长度必须在1-50字符之间'
                }), 400
            coach.name = name
            updated_fields.append('name')
        
        # 更新专业领域
        if 'specialization' in data:
            specialization = data['specialization'].strip()
            if len(specialization) < 1 or len(specialization) > 100:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '专业领域长度必须在1-100字符之间'
                }), 400
            coach.specialization = specialization
            updated_fields.append('specialization')
        
        # 更新每小时费用
        if 'hourly_rate' in data:
            try:
                hourly_rate = float(data['hourly_rate'])
                if hourly_rate <= 0:
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '每小时费用必须大于0'
                    }), 400
                coach.hourly_rate = hourly_rate
                updated_fields.append('hourly_rate')
            except (ValueError, TypeError):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '每小时费用格式不正确'
                }), 400
        
        # 更新从业年限
        if 'experience_years' in data:
            experience_years = data['experience_years']
            if experience_years is not None:
                try:
                    experience_years = int(experience_years)
                    if experience_years < 0:
                        return jsonify({
                            'code': 400,
                            'data': None,
                            'message': '从业年限不能为负数'
                        }), 400
                    coach.experience_years = experience_years
                    updated_fields.append('experience_years')
                except (ValueError, TypeError):
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '从业年限必须是整数'
                    }), 400
        
        # 更新评分
        if 'rating' in data:
            rating = data['rating']
            if rating is not None:
                try:
                    rating = float(rating)
                    if rating < 0 or rating > 5:
                        return jsonify({
                            'code': 400,
                            'data': None,
                            'message': '评分必须在0-5之间'
                        }), 400
                    coach.rating = rating
                    updated_fields.append('rating')
                except (ValueError, TypeError):
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '评分格式不正确'
                    }), 400
        
        # 更新手机号
        if 'phone' in data:
            phone = data['phone'].strip()
            if phone and not phone.isdigit():
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '联系电话只能包含数字'
                }), 400
            coach.phone = phone
            updated_fields.append('phone')
        
        # 更新介绍
        if 'introduction' in data:
            coach.introduction = data.get('introduction', '').strip()
            updated_fields.append('introduction')
        
        # 更新头像
        if 'avatar' in data:
            coach.avatar = data.get('avatar', '').strip()
            updated_fields.append('avatar')
        
        # 更新启用状态
        if 'is_active' in data:
            coach.is_active = bool(data['is_active'])
            updated_fields.append('is_active')
        
        # 检查是否有字段被更新
        if not updated_fields:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '未提供需要更新的字段'
            }), 400
        
        # 更新修改时间
        coach.updated_at = datetime.utcnow()
        
        # 提交更改
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': {
                'coach': coach.to_dict(),
                'updated_fields': updated_fields
            },
            'message': f'教练信息更新成功，更新了 {len(updated_fields)} 个字段'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新教练失败: {str(e)}'
        }), 500
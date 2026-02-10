"""
赛事管理API模块
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db, Event, EventRegistration, User
from config import BaseConfig

# 创建蓝图
events_bp = Blueprint('events', __name__, url_prefix='/api/events')

def get_user_id_from_header():
    """从请求头获取用户ID"""
    user_id = request.headers.get('User-Id')
    if not user_id:
        return None
    try:
        return int(user_id)
    except (ValueError, TypeError):
        return None

@events_bp.route('/list', methods=['GET'])
def list_events():
    """
    获取赛事列表
    ---
    tags:
      - 赛事管理
    summary: 获取赛事列表
    description: 分页获取赛事列表，支持状态和类型筛选
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
          enum: [upcoming, ongoing, completed, cancelled]
      - name: event_type
        in: query
        description: 类型筛选
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
        status_filter = request.args.get('status', '').strip()
        event_type_filter = request.args.get('event_type', '').strip()
        
        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        
        # 构建查询
        query = Event.query
        
        # 状态筛选
        if status_filter:
            query = query.filter(Event.status == status_filter)
        
        # 类型筛选
        if event_type_filter:
            query = query.filter(Event.event_type.contains(event_type_filter))
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        events = query.order_by(Event.event_date.desc())\
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

@events_bp.route('', methods=['POST'])
def create_event():
    """
    创建赛事
    ---
    tags:
      - 赛事管理
    summary: 创建赛事
    description: 创建一个新的赛事
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: 赛事名称
              description:
                type: string
                description: 赛事描述
              event_type:
                type: string
                description: 赛事类型
              event_date:
                type: string
                format: date
                description: 赛事日期
              registration_deadline:
                type: string
                format: date
                description: 报名截止日期
              location:
                type: string
                description: 赛事地点
              max_participants:
                type: integer
                description: 最大参与人数
              registration_fee:
                type: number
                description: 报名费用
              status:
                type: string
                enum: [upcoming, ongoing, completed, cancelled]
                description: 赛事状态
    responses:
      201:
        description: 创建成功
      400:
        description: 请求参数错误
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取请求数据
        data = request.get_json() or {}
        
        # 验证必填字段
        required_fields = ['name', 'event_type', 'event_date', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'缺少必填字段: {field}'
                }), 400
        
        # 创建赛事
        event = Event(
            name=data.get('name'),
            description=data.get('description', ''),
            event_type=data.get('event_type'),
            event_date=datetime.strptime(data.get('event_date'), '%Y-%m-%d').date(),
            registration_deadline=datetime.strptime(data.get('registration_deadline'), '%Y-%m-%d').date() if data.get('registration_deadline') else None,
            location=data.get('location'),
            max_participants=data.get('max_participants', 100),
            current_participants=0,
            registration_fee=data.get('registration_fee', 0.0),
            status=data.get('status', 'upcoming')
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': event.to_dict(),
            'message': '赛事创建成功'
        }), 201
        
    except ValueError as e:
        return jsonify({
            'code': 400,
            'data': None,
            'message': f'日期格式错误: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建赛事失败: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event_detail(event_id):
    """
    获取赛事详情
    ---
    tags:
      - 赛事管理
    summary: 获取赛事详情
    description: 根据赛事ID获取详细信息
    parameters:
      - name: event_id
        in: path
        required: true
        description: 赛事ID
        schema:
          type: integer
    responses:
      200:
        description: 获取成功
      404:
        description: 赛事不存在
    """
    try:
        event = Event.query.get(event_id)
        
        if not event:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '赛事不存在'
            }), 404
        
        # 获取报名统计
        registration_stats = {
            'total_registrations': EventRegistration.query.filter_by(event_id=event_id).count(),
            'approved': EventRegistration.query.filter_by(event_id=event_id, status='approved').count(),
            'pending': EventRegistration.query.filter_by(event_id=event_id, status='pending').count(),
            'rejected': EventRegistration.query.filter_by(event_id=event_id, status='rejected').count()
        }
        
        return jsonify({
            'code': 0,
            'data': {
                'event': event.to_dict(),
                'registration_stats': registration_stats
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取赛事详情失败: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """
    更新赛事信息
    ---
    tags:
      - 赛事管理
    summary: 更新赛事
    description: 更新指定赛事的信息
    parameters:
      - name: event_id
        in: path
        required: true
        description: 赛事ID
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
                description: 赛事名称
              description:
                type: string
                description: 赛事描述
              event_type:
                type: string
                description: 赛事类型
              event_date:
                type: string
                format: date
                description: 赛事日期
              registration_deadline:
                type: string
                format: date
                description: 报名截止日期
              location:
                type: string
                description: 赛事地点
              max_participants:
                type: integer
                description: 最大参与人数
              registration_fee:
                type: number
                description: 报名费用
              status:
                type: string
                enum: [upcoming, ongoing, completed, cancelled]
                description: 赛事状态
    responses:
      200:
        description: 更新成功
      400:
        description: 请求参数错误
      404:
        description: 赛事不存在
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取请求数据
        data = request.get_json() or {}
        
        # 验证赛事是否存在
        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '赛事不存在'
            }), 404
        
        # 更新字段（只更新提供的字段）
        if 'name' in data:
            event.name = data['name']
        if 'description' in data:
            event.description = data['description']
        if 'event_type' in data:
            event.event_type = data['event_type']
        if 'event_date' in data:
            event.event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
        if 'registration_deadline' in data:
            event.registration_deadline = datetime.strptime(data['registration_deadline'], '%Y-%m-%d').date() if data['registration_deadline'] else None
        if 'location' in data:
            event.location = data['location']
        if 'max_participants' in data:
            event.max_participants = data['max_participants']
        if 'registration_fee' in data:
            event.registration_fee = data['registration_fee']
        if 'status' in data:
            event.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': event.to_dict(),
            'message': '赛事更新成功'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'code': 400,
            'data': None,
            'message': f'日期格式错误: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新赛事失败: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>/register', methods=['POST'])
def register_for_event(event_id):
    """
    申请加入赛事
    ---
    tags:
      - 赛事管理
    summary: 申请加入赛事
    description: 用户申请加入指定赛事
    parameters:
      - name: event_id
        in: path
        required: true
        description: 赛事ID
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              contact_info:
                type: string
                description: 联系方式
              additional_info:
                type: string
                description: 附加信息
    responses:
      200:
        description: 申请成功
      400:
        description: 请求参数错误
      404:
        description: 赛事不存在
      409:
        description: 已经报名或人数已满
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
        
        # 验证赛事是否存在
        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '赛事不存在'
            }), 404
        
        # 检查报名截止时间
        # if event.registration_deadline < date.today():
        #     return jsonify({
        #         'code': 400,
        #         'data': None,
        #         'message': '报名已截止'
        #     }), 400
        #
        # 检查是否已经报名
        existing_registration = EventRegistration.query.filter_by(
            event_id=event_id, 
            user_id=user_id
        ).first()
        
        # if existing_registration:
        #     return jsonify({
        #         'code': 409,
        #         'data': None,
        #         'message': '已经报名该赛事'
        #     }), 409
        
        # 检查人数限制
        # if event.current_participants >= event.max_participants:
        #     return jsonify({
        #         'code': 409,
        #         'data': None,
        #         'message': '报名人数已满'
        #     }), 409
        
        # 获取请求数据
        data = request.get_json() or {}
        
        # 生成报名编号
        registration_no = f"ER{datetime.now().strftime('%Y%m%d%H%M%S')}{user_id:04d}{event_id:03d}"
        
        # 创建报名记录
        registration = EventRegistration(
            event_id=event_id,
            user_id=user_id,
            registration_no=registration_no,
            status='pending',
            contact_info=data.get('contact_info', ''),
            additional_info=data.get('additional_info', '')
        )
        
        db.session.add(registration)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': registration.to_dict(),
            'message': '赛事申请提交成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'申请失败: {str(e)}'
        }), 500

@events_bp.route('/my-registrations', methods=['GET'])
def get_my_registrations():
    """
    获取我的赛事申请
    ---
    tags:
      - 赛事管理
    summary: 获取我的申请
    description: 获取当前用户的赛事申请列表
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
          enum: [pending, approved, rejected, cancelled]
    responses:
      200:
        description: 获取成功
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
        query = EventRegistration.query.filter_by(user_id=user_id)
        
        # 状态筛选
        if status_filter:
            query = query.filter(EventRegistration.status == status_filter)
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        registrations = query.order_by(EventRegistration.created_at.desc())\
            .offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return jsonify({
            'code': 0,
            'data': {
                'registrations': [reg.to_dict() for reg in registrations],
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
            'message': f'获取申请列表失败: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>/registrations', methods=['GET'])
def get_event_registrations(event_id):
    """
    获取赛事报名列表
    ---
    tags:
      - 赛事管理
    summary: 获取报名列表
    description: 获取指定赛事的报名列表（管理员功能）
    parameters:
      - name: event_id
        in: path
        required: true
        description: 赛事ID
        schema:
          type: integer
      - name: status
        in: query
        description: 状态筛选
        schema:
          type: string
          enum: [pending, approved, rejected, cancelled]
    responses:
      200:
        description: 获取成功
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 验证赛事是否存在
        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '赛事不存在'
            }), 404
        
        # 获取查询参数
        status_filter = request.args.get('status', '').strip()
        
        # 构建查询
        query = EventRegistration.query.filter_by(event_id=event_id)
        
        # 状态筛选
        if status_filter:
            query = query.filter(EventRegistration.status == status_filter)
        
        registrations = query.order_by(EventRegistration.created_at.desc()).all()
        
        return jsonify({
            'code': 0,
            'data': {
                'event': event.to_dict(),
                'registrations': [reg.to_dict() for reg in registrations],
                'stats': {
                    'total': len(registrations),
                    'pending': len([r for r in registrations if r.status == 'pending']),
                    'approved': len([r for r in registrations if r.status == 'approved']),
                    'rejected': len([r for r in registrations if r.status == 'rejected'])
                }
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取报名列表失败: {str(e)}'
        }), 500

@events_bp.route('/registrations/<int:registration_id>/approve', methods=['POST'])
def approve_registration(registration_id):
    """
    批准报名申请
    ---
    tags:
      - 赛事管理
    summary: 批准报名
    description: 批准指定的用户报名申请
    parameters:
      - name: registration_id
        in: path
        required: true
        description: 报名ID
        schema:
          type: integer
    responses:
      200:
        description: 批准成功
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        registration = EventRegistration.query.get(registration_id)
        if not registration:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '报名记录不存在'
            }), 404
        
        # 检查状态
        if registration.status != 'pending':
            return jsonify({
                'code': 400,
                'data': None,
                'message': '只能批准待审核的申请'
            }), 400
        
        # 检查赛事人数限制
        event = registration.event
        if event.current_participants >= event.max_participants:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '赛事报名人数已满'
            }), 400
        
        # 批准报名
        registration.status = 'approved'
        event.current_participants += 1
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': registration.to_dict(),
            'message': '报名批准成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'批准失败: {str(e)}'
        }), 500

@events_bp.route('/registrations/<int:registration_id>/reject', methods=['POST'])
def reject_registration(registration_id):
    """
    拒绝报名申请
    ---
    tags:
      - 赛事管理
    summary: 拒绝报名
    description: 拒绝指定的用户报名申请
    parameters:
      - name: registration_id
        in: path
        required: true
        description: 报名ID
        schema:
          type: integer
    responses:
      200:
        description: 拒绝成功
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        registration = EventRegistration.query.get(registration_id)
        if not registration:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '报名记录不存在'
            }), 404
        
        # 检查状态
        if registration.status != 'pending':
            return jsonify({
                'code': 400,
                'data': None,
                'message': '只能拒绝待审核的申请'
            }), 400
        
        # 拒绝报名
        registration.status = 'rejected'
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': registration.to_dict(),
            'message': '报名已拒绝'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'拒绝失败: {str(e)}'
        }), 500
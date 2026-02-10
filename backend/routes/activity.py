"""
活动管理API模块
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from models import db, Activity
from config import BaseConfig

# 创建蓝图
activity_bp = Blueprint('activity', __name__, url_prefix='/api/activity')

# 移除用户权限验证，直接操作

@activity_bp.route('/create', methods=['POST'])
def create_activity():
    """
    创建活动
    ---
    tags:
      - 活动管理
    summary: 创建新活动
    description: 用户创建新的体育活动
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
                description: 活动标题
              description:
                type: string
                description: 活动描述
              activity_type:
                type: string
                description: 活动类型
              start_date:
                type: string
                format: date
                description: 开始日期 (YYYY-MM-DD)
              end_date:
                type: string
                format: date
                description: 结束日期 (YYYY-MM-DD)
              start_time:
                type: string
                format: time
                description: 开始时间 (HH:MM)
              end_time:
                type: string
                format: time
                description: 结束时间 (HH:MM)
              location:
                type: string
                description: 活动地点
              max_participants:
                type: integer
                description: 最大参与人数
    responses:
      200:
        description: 创建成功
      400:
        description: 请求参数错误
    """
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        data = request.get_json()
        
        # 验证必需字段
        required_fields = [
            'title', 'activity_type', 'start_date', 'end_date',
            'start_time', 'end_time', 'location', 'max_participants'
        ]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'缺少必需字段: {field}'
                }), 400
        
        # 移除用户验证
        # user = User.query.get(user_id)
        # if not user:
        #     return jsonify({
        #         'code': 404,
        #         'data': None,
        #         'message': '用户不存在'
        #     }), 404
        
        # 解析日期和时间
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            start_time = datetime.strptime(data['start_time'], '%H:%M').time()
            end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        except ValueError:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '日期或时间格式错误'
            }), 400
        
        # 验证时间合理性
        if start_time >= end_time:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '结束时间必须晚于开始时间'
            }), 400
        
        if start_date > end_date:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '开始日期不能晚于结束日期'
            }), 400
        
        # 验证最大参与人数
        try:
            max_participants = int(data['max_participants'])
            if max_participants <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return jsonify({
                'code': 400,
                'data': None,
                'message': '最大参与人数必须是正整数'
            }), 400
        
        # 创建活动
        activity = Activity(
            title=data['title'],
            description=data.get('description', ''),
            activity_type=data['activity_type'],
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            location=data['location'],
            max_participants=max_participants,
            organizer_id=user_id,
            status='upcoming'
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': activity.to_dict(),
            'message': '活动创建成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建活动失败: {str(e)}'
        }), 500

@activity_bp.route('/list', methods=['GET'])
def list_activities():
    """
    获取活动列表
    ---
    tags:
      - 活动管理
    summary: 获取活动列表
    description: 分页获取活动列表，支持类型和状态筛选
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
      - name: activity_type
        in: query
        description: 活动类型筛选
        schema:
          type: string
      - name: status
        in: query
        description: 状态筛选
        schema:
          type: string
          enum: [upcoming, ongoing, completed, cancelled]
    responses:
      200:
        description: 获取成功
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        activity_type = request.args.get('activity_type', '').strip()
        status_filter = request.args.get('status', '').strip()
        
        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        
        # 构建查询
        query = Activity.query.filter_by(is_active=True)
        
        # 类型筛选
        if activity_type:
            query = query.filter(Activity.activity_type == activity_type)
        
        # 状态筛选
        if status_filter:
            query = query.filter(Activity.status == status_filter)
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        activities = query.order_by(desc(Activity.created_at))\
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

@activity_bp.route('/my-activities', methods=['GET'])
def get_my_activities():
    """
    获取我的活动
    ---
    tags:
      - 活动管理
    summary: 获取我的活动
    description: 获取当前用户创建的活动列表
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
    responses:
      200:
        description: 获取成功
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        status_filter = request.args.get('status', '').strip()
        
        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        
        # 构建查询
        query = Activity.query.filter_by(organizer_id=user_id, is_active=True)
        
        # 状态筛选
        if status_filter:
            query = query.filter(Activity.status == status_filter)
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        activities = query.order_by(desc(Activity.created_at))\
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
            'message': f'获取我的活动失败: {str(e)}'
        }), 500

@activity_bp.route('/<int:activity_id>', methods=['GET'])
def get_activity_detail(activity_id):
    """
    获取活动详情
    ---
    tags:
      - 活动管理
    summary: 获取活动详情
    description: 根据活动ID获取详细信息
    parameters:
      - name: activity_id
        in: path
        required: true
        description: 活动ID
        schema:
          type: integer
    responses:
      200:
        description: 获取成功
      404:
        description: 活动不存在
    """
    try:
        activity = Activity.query.get(activity_id)
        
        if not activity or not activity.is_active:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '活动不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'data': activity.to_dict(),
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取活动详情失败: {str(e)}'
        }), 500

@activity_bp.route('/<int:activity_id>/join', methods=['POST'])
def join_activity(activity_id):
    """
    参与活动
    ---
    tags:
      - 活动管理
    summary: 参与活动
    description: 用户参与指定的活动
    parameters:
      - name: activity_id
        in: path
        required: true
        description: 活动ID
        schema:
          type: integer
    responses:
      200:
        description: 参与成功
      400:
        description: 活动已满或已结束
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        activity = Activity.query.get(activity_id)
        
        if not activity or not activity.is_active:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '活动不存在'
            }), 404
        
        # 检查活动状态
        if activity.status == 'completed':
            return jsonify({
                'code': 400,
                'data': None,
                'message': '活动已结束'
            }), 400
        
        if activity.status == 'cancelled':
            return jsonify({
                'code': 400,
                'data': None,
                'message': '活动已取消'
            }), 400
        
        # 检查是否已满员
        if activity.current_participants >= activity.max_participants:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '活动人数已满'
            }), 400
        
        # 检查是否已经参与过
        # 这里可以添加参与记录表，暂时简化为更新参与人数
        if activity.current_participants < activity.max_participants:
            activity.current_participants += 1
            db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': activity.to_dict(),
            'message': '参与活动成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'参与活动失败: {str(e)}'
        }), 500

@activity_bp.route('/<int:activity_id>/update', methods=['PUT'])
def update_activity(activity_id):
    """
    更新活动
    ---
    tags:
      - 活动管理
    summary: 更新活动
    description: 更新活动信息（仅活动创建者）
    parameters:
      - name: activity_id
        in: path
        required: true
        description: 活动ID
        schema:
          type: integer
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
              description:
                type: string
              max_participants:
                type: integer
    responses:
      200:
        description: 更新成功
      403:
        description: 无权限更新
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '活动不存在'
            }), 404
        
        # 验证权限
        # 移除权限检查，直接允许操作
        
        data = request.get_json()
        
        # 更新允许的字段
        updatable_fields = ['title', 'description', 'max_participants']
        updated = False
        
        for field in updatable_fields:
            if field in data:
                if field == 'max_participants':
                    try:
                        new_value = int(data[field])
                        if new_value <= 0:
                            return jsonify({
                                'code': 400,
                                'data': None,
                                'message': '最大参与人数必须是正整数'
                            }), 400
                        # 确保不能小于当前参与人数
                        if new_value < activity.current_participants:
                            return jsonify({
                                'code': 400,
                                'data': None,
                                'message': '最大参与人数不能小于当前参与人数'
                            }), 400
                        setattr(activity, field, new_value)
                        updated = True
                    except (ValueError, TypeError):
                        return jsonify({
                            'code': 400,
                            'data': None,
                            'message': '最大参与人数必须是正整数'
                        }), 400
                else:
                    setattr(activity, field, data[field])
                    updated = True
        
        if not updated:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '没有提供有效的更新字段'
            }), 400
        
        activity.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': activity.to_dict(),
            'message': '活动更新成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新活动失败: {str(e)}'
        }), 500

@activity_bp.route('/delete', methods=['POST'])
def delete_activity():
    """
    删除活动
    ---
    tags:
      - 活动管理
    summary: 删除活动
    description: 删除活动（软删除，将is_active设置为false）
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              id:
                type: integer
                description: 活动ID
    responses:
      200:
        description: 删除成功
      404:
        description: 活动不存在
      403:
        description: 无权限删除
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        data = request.get_json()
        activity_id = data.get('id')
        
        if not activity_id:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '活动ID不能为空'
            }), 400
        
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '活动不存在'
            }), 404
        
        # 验证权限（只有创建者或管理员可以删除）
        # 移除权限检查，直接允许操作
        
        # 软删除
        activity.is_active = False
        activity.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': None,
            'message': '活动删除成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除活动失败: {str(e)}'
        }), 500

@activity_bp.route('/batchDelete', methods=['POST'])
def batch_delete_activities():
    """
    批量删除活动
    ---
    tags:
      - 活动管理
    summary: 批量删除活动
    description: 批量删除活动（软删除）
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              ids:
                type: array
                items:
                  type: integer
                description: 活动ID列表
    responses:
      200:
        description: 批量删除成功
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        data = request.get_json()
        activity_ids = data.get('ids', [])
        
        if not activity_ids or not isinstance(activity_ids, list):
            return jsonify({
                'code': 400,
                'data': None,
                'message': '请提供有效的活动ID列表'
            }), 400
        
        # 查找用户创建的活动
        activities = Activity.query.filter(
            Activity.id.in_(activity_ids),
            Activity.organizer_id == user_id
        ).all()
        
        if not activities:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '没有找到可删除的活动'
            }), 404
        
        # 批量软删除
        for activity in activities:
            activity.is_active = False
            activity.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': {
                'deleted_count': len(activities)
            },
            'message': f'成功删除 {len(activities)} 个活动'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'批量删除活动失败: {str(e)}'
        }), 500

@activity_bp.route('/types', methods=['GET'])
def get_activity_types():
    """
    获取活动类型列表
    ---
    tags:
      - 活动管理
    summary: 获取活动类型
    description: 获取所有可用的活动类型
    responses:
      200:
        description: 获取成功
    """
    try:
        activity_types = [
            {'id': 'training', 'name': '训练营'},
            {'id': 'competition', 'name': '比赛'},
            {'id': 'lecture', 'name': '讲座'},
            {'id': 'trial', 'name': '体验课'},
            {'id': 'other', 'name': '其他'}
        ]
        
        return jsonify({
            'code': 0,
            'data': activity_types,
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取活动类型失败: {str(e)}'
        }), 500

@activity_bp.route('/<int:activity_id>/participants', methods=['GET'])
def get_activity_participants(activity_id):
    """
    获取活动参与者列表
    ---
    tags:
      - 活动管理
    summary: 获取活动参与者
    description: 获取指定活动的参与者列表
    parameters:
      - name: activity_id
        in: path
        required: true
        description: 活动ID
        schema:
          type: integer
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
      404:
        description: 活动不存在
    """
    try:
        activity = Activity.query.get(activity_id)
        
        if not activity or not activity.is_active:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '活动不存在'
            }), 404
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        
        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        
        # 查询参与者
        query = activity.participants.filter_by(status='joined')
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        participants = query.order_by(ActivityParticipant.joined_at)\
            .offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return jsonify({
            'code': 0,
            'data': {
                'participants': [participant.to_dict() for participant in participants],
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
            'message': f'获取活动参与者失败: {str(e)}'
        }), 500

@activity_bp.route('/<int:activity_id>/participants', methods=['GET'])
def get_participants(activity_id):
    """
    获取活动参与者列表
    ---
    tags:
      - 活动管理
    summary: 获取活动参与者
    description: 获取指定活动的参与者列表
    parameters:
      - name: activity_id
        in: path
        required: true
        description: 活动ID
        schema:
          type: integer
    responses:
      200:
        description: 获取成功
      404:
        description: 活动不存在
    """
    try:
        activity = Activity.query.get(activity_id)
        
        if not activity or not activity.is_active:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '活动不存在'
            }), 404
        
        # 获取参与者信息
        participants = []
        try:
            # 如果有参与者关系表，在这里查询
            # 目前返回模拟数据
            participants = [
                {
                    'id': i,
                    'username': f'用户{i}',
                    'avatar': f'/static/avatar/{i}.jpg',
                    'join_time': datetime.utcnow().isoformat()
                } for i in range(1, min(activity.current_participants + 1, 6))
            ]
        except Exception as e:
            print(f"获取参与者信息时出错: {e}")
            participants = []
        
        return jsonify({
            'code': 0,
            'data': {
                'participants': participants,
                'total': activity.current_participants,
                'max_participants': activity.max_participants
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取活动参与者失败: {str(e)}'
        }), 500

@activity_bp.route('/<int:activity_id>/leave', methods=['POST'])
def leave_activity(activity_id):
    """
    退出活动
    ---
    tags:
      - 活动管理
    summary: 退出活动
    description: 用户退出指定的活动
    parameters:
      - name: activity_id
        in: path
        required: true
        description: 活动ID
        schema:
          type: integer
    responses:
      200:
        description: 退出成功
      400:
        description: 未加入活动
      404:
        description: 活动不存在
    """
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        activity = Activity.query.get(activity_id)
        
        if not activity or not activity.is_active:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '活动不存在'
            }), 404
        
        # 移除参与者
        success, message = activity.remove_participant(user_id)
        
        if not success:
            return jsonify({
                'code': 400,
                'data': None,
                'message': message
            }), 400
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': activity.to_dict(),
            'message': '成功退出活动'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'退出活动失败: {str(e)}'
        }), 500

@activity_bp.route('/<int:activity_id>/status', methods=['PUT'])
def update_activity_status(activity_id):
    """
    更新活动状态
    ---
    tags:
      - 活动管理
    summary: 更新活动状态
    description: 更新活动的状态（组织者权限）
    parameters:
      - name: activity_id
        in: path
        required: true
        description: 活动ID
        schema:
          type: integer
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              status:
                type: string
                enum: [upcoming, ongoing, completed, cancelled]
                description: 活动状态
    responses:
      200:
        description: 更新成功
      400:
        description: 状态无效
      404:
        description: 活动不存在
    """
    try:
        activity = Activity.query.get(activity_id)
        
        if not activity or not activity.is_active:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '活动不存在'
            }), 404
        
        data = request.get_json()
        new_status = data.get('status')
        
        valid_statuses = ['upcoming', 'ongoing', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({
                'code': 400,
                'data': None,
                'message': f'无效的活动状态，可选状态: {", ".join(valid_statuses)}'
            }), 400
        
        activity.status = new_status
        activity.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': activity.to_dict(),
            'message': '活动状态更新成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新活动状态失败: {str(e)}'
        }), 500
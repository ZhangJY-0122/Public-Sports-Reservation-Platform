"""
朋友管理API模块
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import and_, or_, func
from models import db, User, Friend
from config import BaseConfig

# 创建蓝图
friends_bp = Blueprint('friends', __name__, url_prefix='/api/friends')

def get_user_id_from_header():
    """从请求头获取用户ID"""
    user_id = request.headers.get('User-Id')
    if not user_id:
        return None
    try:
        return int(user_id)
    except (ValueError, TypeError):
        return None


@friends_bp.route('/list', methods=['GET'])
def get_all_users():
    """获取除当前用户外的所有用户列表"""
    try:
        current_user_id = get_user_id_from_header()  # 默认用户ID，实际应用中应从认证信息获取

        # 查询除当前用户外的所有用户
        users = User.query.filter(User.id != current_user_id).all()

        # 构建用户数据
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'real_name': user.real_name,
                'avatar': user.avatar,
                'city': user.city,
                'exercise_days': user.exercise_days,
                'friends_count': user.friends_count,
                'points': user.points,
                'vip_level': user.vip_level,
                'last_login_at': user.last_login_at.isoformat() if user.last_login_at else None
            })

        return jsonify({
            'code': 0,
            'data': users_data,
            'message': '获取成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取用户列表失败: {str(e)}'
        }), 500

@friends_bp.route('/add', methods=['POST'])
def add_friend():
    """
    添加朋友
    ---
    tags:
      - 朋友管理
    summary: 添加朋友
    description: 向其他用户发送好友请求
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              friend_user_id:
                type: integer
                description: 朋友的用户ID
              message:
                type: string
                description: 验证消息
    responses:
      200:
        description: 添加成功
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
                    id:
                      type: integer
                    status:
                      type: string
                      example: "pending"
                message:
                  type: string
                  example: "好友请求已发送"
      400:
        description: 请求参数错误或关系已存在
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        data = request.get_json()
        
        # 验证必填字段
        if 'friend_user_id' not in data:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '缺少必填字段: friend_user_id'
            }), 400
        
        friend_user_id = data['friend_user_id']
        message = data.get('message', '')
        
        # 验证用户ID有效性
        if friend_user_id == user_id:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '不能添加自己为好友'
            }), 400
        
        # 验证目标用户是否存在
        friend_user = User.query.get(friend_user_id)
        if not friend_user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404
        
        # 检查是否已存在好友关系
        existing_friend = Friend.query.filter(
            or_(
                and_(Friend.user_id == user_id, Friend.friend_user_id == friend_user_id),
                and_(Friend.user_id == friend_user_id, Friend.friend_user_id == user_id)
            )
        ).first()
        
        if existing_friend:
            if existing_friend.status == 'accepted':
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '已经是好友关系'
                }), 400
            elif existing_friend.status == 'pending':
                if existing_friend.user_id == user_id:
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '已发送过好友请求，请等待对方同意'
                    }), 400
                else:
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '对方已发送好友请求，请先处理该请求'
                    }), 400
        
        # 创建好友关系
        friend_relationship = Friend(
            user_id=user_id,
            friend_user_id=friend_user_id,
            status='pending',
            message=message
        )
        
        db.session.add(friend_relationship)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': {
                'id': friend_relationship.id,
                'status': friend_relationship.status
            },
            'message': '好友请求已发送'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'添加好友失败: {str(e)}'
        }), 500

@friends_bp.route('/requests', methods=['GET'])
def get_friend_requests():
    """
    获取好友请求列表
    ---
    tags:
      - 朋友管理
    summary: 获取好友请求列表
    description: 获取收到的和发送的好友请求
    parameters:
      - name: type
        in: query
        description: 请求类型
        schema:
          type: string
          enum: [received, sent]
          default: received
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
                    requests:
                      type: array
                      items:
                        type: object
                        properties:
                          id:
                            type: integer
                          requester_user_id:
                            type: integer
                          requester_name:
                            type: string
                          requester_nickname:
                            type: string
                          requester_avatar:
                            type: string
                          status:
                            type: string
                          message:
                            type: string
                          created_at:
                            type: string
                      description: 请求列表
                    total:
                      type: integer
                      description: 请求总数
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
        request_type = request.args.get('type', 'received')
        
        # 构建查询
        if request_type == 'received':
            # 收到的请求（自己是接受者）
            query = Friend.query.filter(
                Friend.friend_user_id == user_id,
                Friend.status == 'pending'
            )
        elif request_type == 'sent':
            # 发送的请求（自己是发起者）
            query = Friend.query.filter(
                Friend.user_id == user_id,
                Friend.status == 'pending'
            )
        else:
            return jsonify({
                'code': 400,
                'data': None,
                'message': f'无效的请求类型: {request_type}'
            }), 400
        
        requests = query.order_by(Friend.created_at.desc()).all()
        
        # 构建请求数据
        requests_data = []
        for req in requests:
            if request_type == 'received':
                requester_user = User.query.get(req.user_id)
                user_id_field = 'requester_user_id'
                name_field = 'requester_name'
                nickname_field = 'requester_nickname'
                avatar_field = 'requester_avatar'
            else:
                requester_user = User.query.get(req.friend_user_id)
                user_id_field = 'requester_user_id'
                name_field = 'requester_name'
                nickname_field = 'requester_nickname'
                avatar_field = 'requester_avatar'
            
            if requester_user:
                requests_data.append({
                    'id': req.id,
                    user_id_field: requester_user.id,
                    name_field: requester_user.username,
                    nickname_field: requester_user.nickname,
                    avatar_field: requester_user.avatar,
                    'status': req.status,
                    'message': req.message,
                    'created_at': req.created_at.isoformat()
                })
        
        return jsonify({
            'code': 0,
            'data': {
                'requests': requests_data,
                'total': len(requests_data)
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取好友请求失败: {str(e)}'
        }), 500

@friends_bp.route('/<int:request_id>/accept', methods=['POST'])
def accept_friend_request(request_id):
    """
    接受好友请求
    ---
    tags:
      - 朋友管理
    summary: 接受好友请求
    description: 接受其他用户的好友请求
    parameters:
      - name: request_id
        in: path
        description: 好友请求ID
        schema:
          type: integer
    responses:
      200:
        description: 接受成功
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
                    status:
                      type: string
                      example: "accepted"
                message:
                  type: string
                  example: "好友请求已接受"
      400:
        description: 请求参数错误或权限不足
      404:
        description: 好友请求不存在
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 查找好友请求
        friend_request = Friend.query.get(request_id)
        if not friend_request:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '好友请求不存在'
            }), 404
        
        # 验证权限（只有接受者可以接受请求）
        if friend_request.friend_user_id != user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '没有权限操作该请求'
            }), 403
        
        # 验证请求状态
        if friend_request.status != 'pending':
            return jsonify({
                'code': 400,
                'data': None,
                'message': '该请求已被处理'
            }), 400
        
        # 更新请求状态
        friend_request.status = 'accepted'
        friend_request.updated_at = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': {
                'status': friend_request.status
            },
            'message': '好友请求已接受'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'接受好友请求失败: {str(e)}'
        }), 500

@friends_bp.route('/<int:request_id>/reject', methods=['POST'])
def reject_friend_request(request_id):
    """
    拒绝好友请求
    ---
    tags:
      - 朋友管理
    summary: 拒绝好友请求
    description: 拒绝其他用户的好友请求
    parameters:
      - name: request_id
        in: path
        description: 好友请求ID
        schema:
          type: integer
    responses:
      200:
        description: 拒绝成功
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
                    status:
                      type: string
                      example: "rejected"
                message:
                  type: string
                  example: "好友请求已拒绝"
      400:
        description: 请求参数错误或权限不足
      404:
        description: 好友请求不存在
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 查找好友请求
        friend_request = Friend.query.get(request_id)
        if not friend_request:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '好友请求不存在'
            }), 404
        
        # 验证权限（只有接受者可以拒绝请求）
        if friend_request.friend_user_id != user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '没有权限操作该请求'
            }), 403
        
        # 验证请求状态
        if friend_request.status != 'pending':
            return jsonify({
                'code': 400,
                'data': None,
                'message': '该请求已被处理'
            }), 400
        
        # 更新请求状态
        friend_request.status = 'rejected'
        friend_request.updated_at = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': {
                'status': friend_request.status
            },
            'message': '好友请求已拒绝'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'拒绝好友请求失败: {str(e)}'
        }), 500

@friends_bp.route('/<int:friend_id>/remove', methods=['DELETE'])
def remove_friend(friend_id):
    """
    删除好友
    ---
    tags:
      - 朋友管理
    summary: 删除好友
    description: 删除好友关系
    parameters:
      - name: friend_id
        in: path
        description: 好友关系ID
        schema:
          type: integer
    responses:
      200:
        description: 删除成功
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
                    status:
                      type: string
                      example: "deleted"
                message:
                  type: string
                  example: "好友已删除"
      400:
        description: 请求参数错误或权限不足
      404:
        description: 好友关系不存在
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 查找好友关系
        friend_relationship = Friend.query.get(friend_id)
        if not friend_relationship:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '好友关系不存在'
            }), 404
        
        # 验证权限（双方都可以删除好友关系）
        if friend_relationship.user_id != user_id and friend_relationship.friend_user_id != user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '没有权限操作该好友关系'
            }), 403
        
        # 验证好友关系状态
        if friend_relationship.status != 'accepted':
            return jsonify({
                'code': 400,
                'data': None,
                'message': '该好友关系未建立'
            }), 400
        
        # 删除好友关系
        db.session.delete(friend_relationship)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': {
                'status': 'deleted'
            },
            'message': '好友已删除'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除好友失败: {str(e)}'
        }), 500

@friends_bp.route('/search', methods=['GET'])
def search_users():
    """
    搜索用户
    ---
    tags:
      - 朋友管理
    summary: 搜索用户
    description: 根据用户名或昵称搜索用户
    parameters:
      - name: keyword
        in: query
        description: 搜索关键词
        required: true
        schema:
          type: string
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
        description: 搜索成功
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
                    users:
                      type: array
                      items:
                        type: object
                        properties:
                          id:
                            type: integer
                          username:
                            type: string
                          nickname:
                            type: string
                          avatar:
                            type: string
                          is_friend:
                            type: boolean
                      description: 用户列表
                    pagination:
                      type: object
                      properties:
                        current_page:
                          type: integer
                        page_size:
                          type: integer
                        total:
                          type: integer
                        total_pages:
                          type: integer
                message:
                  type: string
                  example: "搜索成功"
      400:
        description: 请求参数错误
    """
    try:
        # 获取用户ID
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取查询参数
        keyword = request.args.get('keyword', '').strip()
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', BaseConfig.PAGE_SIZE, type=int)
        
        # 验证搜索关键词
        if not keyword:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '搜索关键词不能为空'
            }), 400
        
        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        
        # 构建搜索查询（排除当前用户）
        query = User.query.filter(
            User.id != user_id,
            or_(
                User.username.like(f'%{keyword}%'),
                User.nickname.like(f'%{keyword}%')
            )
        )
        
        # 总数查询
        total = query.count()
        
        # 分页查询
        users = query.offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        # 构建用户数据
        users_data = []
        for user in users:
            # 检查是否为好友
            is_friend = Friend.query.filter(
                or_(
                    and_(Friend.user_id == user_id, Friend.friend_user_id == user.id),
                    and_(Friend.user_id == user.id, Friend.friend_user_id == user_id)
                ),
                Friend.status == 'accepted'
            ).first() is not None
            
            users_data.append({
                'id': user.id,
                'username': user.username,
                'nickname': user.nickname,
                'avatar': user.avatar,
                'is_friend': is_friend
            })
        
        return jsonify({
            'code': 0,
            'data': {
                'users': users_data,
                'pagination': {
                    'current_page': page,
                    'page_size': page_size,
                    'total': total,
                    'total_pages': total_pages
                }
            },
            'message': '搜索成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'搜索用户失败: {str(e)}'
        }), 500
"""
用户认证API模块
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, Unauthorized
from models import db, User, UserRole
from config import BaseConfig

# 创建蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    ---
    tags:
      - 用户认证
    summary: 用户注册
    description: 创建新的用户账号
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - email
              - password
              - phone
              - city
            properties:
              username:
                type: string
                description: 用户名
                example: "zhangsan"
              email:
                type: string
                description: 邮箱地址
                example: "zhangsan@example.com"
              phone:
                type: string
                description: 手机号
                example: "13800138000"
              city:
                type: string
                description: 所在城市
                example: "北京市"
              password:
                type: string
                description: 密码
                example: "123456"
              real_name:
                type: string
                description: 真实姓名
                example: "张三"
    responses:
      200:
        description: 注册成功
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
                    user_id:
                      type: integer
                      example: 1
                    username:
                      type: string
                      example: "zhangsan"
                message:
                  type: string
                  example: "注册成功"
      400:
        description: 请求参数错误
      409:
        description: 用户名或邮箱已存在
    """
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['username', 'email', 'password', 'phone', 'city']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'缺少必需字段: {field}'
                }), 400
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'code': 409,
                'data': None,
                'message': '用户名已存在'
            }), 409
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'code': 409,
                'data': None,
                'message': '邮箱已存在'
            }), 409
        
        # 检查手机号是否已存在
        if data.get('phone') and User.query.filter_by(phone=data['phone']).first():
            return jsonify({
                'code': 409,
                'data': None,
                'message': '手机号已存在'
            }), 409
        
        # 创建新用户
        user = User(
            username=data['username'],
            email=data['email'],
            phone=data['phone'],
            city=data['city'],
            real_name=data.get('real_name', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': {
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            },
            'message': '注册成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'注册失败: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    ---
    tags:
      - 用户认证
    summary: 用户登录
    description: 用户登录获取访问权限
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
                description: 用户名或邮箱
                example: "zhangsan"
              password:
                type: string
                description: 密码
                example: "123456"
    responses:
      200:
        description: 登录成功
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
                    user_id:
                      type: integer
                      example: 1
                    username:
                      type: string
                      example: "zhangsan"
                    email:
                      type: string
                      example: "zhangsan@example.com"
                    token:
                      type: string
                      example: "user_1"
                message:
                  type: string
                  example: "登录成功"
      400:
        description: 请求参数错误
      401:
        description: 用户名或密码错误
    """
    try:
        data = request.get_json()
        
        # 验证必需字段
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'code': 400,
                'data': None,
                'message': '用户名和密码不能为空'
            }), 400
        
        # 查找用户（支持用户名或邮箱登录）
        username = data['username']
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'code': 401,
                'data': None,
                'message': '用户名或密码错误'
            }), 401
        
        # 更新最后登录时间
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        
        # 返回用户信息（在实际生产环境中应该返回JWT token）
        # 这里简化为返回用户ID作为token
        return jsonify({
            'code': 0,
            'data': {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'token': f'user_{user.id}'  # 简单token，实际应使用JWT
            },
            'message': '登录成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'登录失败: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    获取用户信息
    ---
    tags:
      - 用户认证
    summary: 获取当前用户信息
    description: 根据请求头中的用户ID获取用户详细信息
    security:
      - ApiKeyAuth: []
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
        description: 未授权访问
      404:
        description: 用户不存在
    """
    try:
        # 从请求头获取用户ID
        user_id = request.headers.get(BaseConfig.USER_ID_HEADER)
        if not user_id:
            return jsonify({
                'code': 401,
                'data': None,
                'message': '缺少用户身份信息'
            }), 401
        
        # 查找用户
        user = User.query.get(int(user_id))
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
        
    except ValueError:
        return jsonify({
            'code': 401,
            'data': None,
            'message': '无效的用户ID'
        }), 401
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取用户信息失败: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    """
    更新用户信息
    ---
    tags:
      - 用户认证
    summary: 更新当前用户信息
    description: 更新当前用户的个人信息
    security:
      - ApiKeyAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              real_name:
                type: string
                description: 真实姓名
              phone:
                type: string
                description: 手机号
              city:
                type: string
                description: 所在城市
              avatar:
                type: string
                description: 头像URL
    responses:
      200:
        description: 更新成功
      400:
        description: 请求参数错误
      401:
        description: 未授权访问
      404:
        description: 用户不存在
    """
    try:
        # 从请求头获取用户ID
        user_id = request.headers.get(BaseConfig.USER_ID_HEADER)
        if not user_id:
            return jsonify({
                'code': 401,
                'data': None,
                'message': '缺少用户身份信息'
            }), 401
        
        # 查找用户
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404
        
        # 获取更新数据
        data = request.get_json()
        
        # 更新允许的字段
        allowed_fields = ['real_name', 'phone', 'city', 'avatar']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': user.to_dict(),
            'message': '更新成功'
        }), 200
        
    except ValueError:
        return jsonify({
            'code': 401,
            'data': None,
            'message': '无效的用户ID'
        }), 401
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新失败: {str(e)}'
        }), 500
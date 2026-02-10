"""
Venue模型的增删改查API模块
包含分页处理
"""

from datetime import datetime
import json
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy import or_, and_, desc, asc
from sqlalchemy.orm import contains_eager
from models import db, Venue, VenueCategory, VenueReview
from config import BaseConfig

# 创建蓝图
venue_crud_bp = Blueprint('venue_crud', __name__, url_prefix='/api/venues')


@venue_crud_bp.route('', methods=['GET'])
def get_venues():
    """
    获取场馆列表（分页）
    ---
    tags:
      - 场馆管理
    summary: 获取场馆列表
    description: 获取场馆列表，支持搜索和分页
    parameters:
      - name: page
        in: query
        type: integer
        description: 页码（从1开始）
        default: 1
      - name: limit
        in: query
        type: integer
        description: 每页数量
        default: 10
      - name: search
        in: query
        type: string
        description: 搜索关键词（场馆名称、地址、类型）
      - name: category_id
        in: query
        type: integer
        description: 分类ID
      - name: is_active
        in: query
        type: boolean
        description: 是否启用状态
      - name: sort_field
        in: query
        type: string
        description: 排序字段（id, name, created_at, price）
        default: id
      - name: sort_order
        in: query
        type: string
        description: 排序方向（asc, desc）
        default: desc
    responses:
      200:
        description: 获取成功
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '').strip()
        category_id = request.args.get('category_id', type=int)
        is_active = request.args.get('is_active', type=bool)
        sort_field = request.args.get('sort_field', 'id')
        sort_order = request.args.get('sort_order', 'desc')

        # 验证排序字段
        allowed_sort_fields = ['id', 'name', 'created_at', 'price', 'capacity']
        if sort_field not in allowed_sort_fields:
            sort_field = 'id'

        # 验证排序方向
        if sort_order not in ['asc', 'desc']:
            sort_order = 'desc'

        # 构建基础查询
        query = Venue.query.join(VenueCategory)

        # 添加搜索条件
        if search:
            query = query.filter(
                or_(
                    Venue.name.like(f'%{search}%'),
                    Venue.location.like(f'%{search}%'),
                    Venue.type.like(f'%{search}%'),
                    Venue.description.like(f'%{search}%')
                )
            )

        # 添加分类过滤
        if category_id:
            query = query.filter(Venue.category_id == category_id)

        # 添加状态过滤
        if is_active is not None:
            query = query.filter(Venue.is_active == is_active)

        # 设置排序
        sort_column = getattr(Venue, sort_field, Venue.id)
        if sort_field == 'price':
            sort_column = Venue.price_per_hour
        elif sort_field == 'created_at':
            sort_column = Venue.created_at
        
        if sort_order == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # 执行分页查询
        pagination = query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )

        # 准备响应数据
        data = {
            'venues': [venue.to_dict() for venue in pagination.items],
            'pagination': {
                'current_page': page,
                'per_page': limit,
                'total': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }

        return jsonify({
            'code': 0,
            'data': data,
            'message': '获取成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取场馆列表失败: {str(e)}'
        }), 500


@venue_crud_bp.route('/<int:venue_id>', methods=['GET'])
def get_venue(venue_id):
    """
    获取单个场馆详情
    ---
    tags:
      - 场馆管理
    summary: 获取场馆详情
    description: 根据ID获取场馆详细信息
    parameters:
      - name: venue_id
        in: path
        required: true
        description: 场馆ID
        schema:
          type: integer
    responses:
      200:
        description: 获取成功
      404:
        description: 场馆不存在
    """
    try:
        venue = Venue.query.get_or_404(venue_id)
        
        # 添加评分统计信息
        venue_dict = venue.to_dict()
        venue_dict['average_rating'] = venue.get_average_rating()
        venue_dict['review_count'] = venue.get_review_count()

        return jsonify({
            'code': 0,
            'data': venue_dict,
            'message': '获取成功'
        }), 200

    except NotFound:
        return jsonify({
            'code': 404,
            'data': None,
            'message': '场馆不存在'
        }), 404
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取场馆详情失败: {str(e)}'
        }), 500


@venue_crud_bp.route('/add', methods=['POST'])
def create_venue():
    """
    创建新场馆
    ---
    tags:
      - 场馆管理
    summary: 创建场馆
    description: 创建一个新的场馆
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: 场馆名称
                example: "阳光体育馆"
              type:
                type: string
                description: 场馆类型
                example: "篮球场"
              location:
                type: string
                description: 场馆地址
                example: "北京市朝阳区xxx路xxx号"
              description:
                type: string
                description: 场馆描述
                example: "设施完善，环境优雅"
              image:
                type: string
                description: 场馆图片URL
                example: "http://example.com/image.jpg"
              price_per_hour:
                type: number
                description: 每小时价格
                example: 100.00
              capacity:
                type: integer
                description: 容量/人数
                example: 20
              facilities:
                type: string
                description: 设施描述
                example: "空调、更衣室、停车场"
              contact_phone:
                type: string
                description: 联系电话
                example: "13800138000"
              business_hours:
                type: string
                description: 营业时间
                example: "08:00-22:00"
              category_id:
                type: integer
                description: 分类ID
                example: 1
              is_active:
                type: boolean
                description: 是否启用
                default: true
    responses:
      200:
        description: 创建成功
      400:
        description: 请求参数错误
      409:
        description: 场馆名称已存在
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '请求数据不能为空'
            }), 400

        # 验证必填字段
        required_fields = ['name', 'type', 'location', 'price_per_hour', 'category_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'{field}不能为空'
                }), 400

        # 检查场馆名称是否已存在
        existing_venue = Venue.query.filter_by(name=data['name'].strip()).first()
        if existing_venue:
            return jsonify({
                'code': 409,
                'data': None,
                'message': '场馆名称已存在'
            }), 409

        # 检查分类是否存在
        category = VenueCategory.query.get(data['category_id'])
        if not category:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '分类不存在'
            }), 400

        # 创建新场馆
        venue = Venue(
            name=data['name'].strip(),
            type=data['type'].strip(),
            location=data['location'].strip(),
            description=data.get('description', '').strip(),
            image=data.get('image', '').strip(),
            price_per_hour=float(data['price_per_hour']),
            capacity=int(data.get('capacity', 1)),
            facilities=data.get('facilities', '').strip(),
            contact_phone=data.get('contact_phone', '').strip(),
            business_hours=data.get('business_hours', '').strip(),
            category_id=int(data['category_id']),
            is_active=data.get('is_active', True)
        )

        db.session.add(venue)
        db.session.commit()

        return jsonify({
            'code': 0,
            'data': venue.to_dict(),
            'message': '创建成功'
        }), 200

    except ValueError as e:
        return jsonify({
            'code': 400,
            'data': None,
            'message': f'数据类型错误: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建场馆失败: {str(e)}'
        }), 500


@venue_crud_bp.route('/<int:venue_id>', methods=['PUT'])
def update_venue(venue_id):
    """
    更新场馆信息
    ---
    tags:
      - 场馆管理
    summary: 更新场馆
    description: 更新指定场馆的信息
    parameters:
      - name: venue_id
        in: path
        required: true
        description: 场馆ID
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
                description: 场馆名称
              type:
                type: string
                description: 场馆类型
              location:
                type: string
                description: 场馆地址
              description:
                type: string
                description: 场馆描述
              image:
                type: string
                description: 场馆图片URL
              price_per_hour:
                type: number
                description: 每小时价格
              capacity:
                type: integer
                description: 容量/人数
              facilities:
                type: string
                description: 设施描述
              contact_phone:
                type: string
                description: 联系电话
              business_hours:
                type: string
                description: 营业时间
              category_id:
                type: integer
                description: 分类ID
              is_active:
                type: boolean
                description: 是否启用
    responses:
      200:
        description: 更新成功
      404:
        description: 场馆不存在
      409:
        description: 场馆名称已存在
    """
    try:
        venue = Venue.query.get_or_404(venue_id)
        data = request.get_json()

        if not data:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '请求数据不能为空'
            }), 400

        # 检查场馆名称是否已存在（排除当前场馆）
        if 'name' in data and data['name'].strip() != venue.name:
            existing_venue = Venue.query.filter_by(name=data['name'].strip()).first()
            if existing_venue:
                return jsonify({
                    'code': 409,
                    'data': None,
                    'message': '场馆名称已存在'
                }), 409

        # 检查分类是否存在
        if 'category_id' in data:
            category = VenueCategory.query.get(data['category_id'])
            if not category:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '分类不存在'
                }), 400

        # 更新字段
        updateable_fields = [
            'name', 'type', 'location', 'description', 'image', 
            'price_per_hour', 'capacity', 'facilities', 'contact_phone', 
            'business_hours', 'category_id', 'is_active'
        ]

        for field in updateable_fields:
            if field in data:
                if field == 'name':
                    venue.name = data[field].strip()
                elif field == 'type':
                    venue.type = data[field].strip()
                elif field == 'location':
                    venue.location = data[field].strip()
                elif field == 'description':
                    venue.description = data[field].strip()
                elif field == 'image':
                    venue.image = data[field].strip()
                elif field == 'price_per_hour':
                    venue.price_per_hour = float(data[field])
                elif field == 'capacity':
                    venue.capacity = int(data[field])
                elif field == 'facilities':
                    venue.facilities = data[field].strip()
                elif field == 'contact_phone':
                    venue.contact_phone = data[field].strip()
                elif field == 'business_hours':
                    venue.business_hours = data[field].strip()
                elif field == 'category_id':
                    venue.category_id = int(data[field])
                elif field == 'is_active':
                    venue.is_active = bool(data[field])

        venue.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'code': 0,
            'data': venue.to_dict(),
            'message': '更新成功'
        }), 200

    except NotFound:
        return jsonify({
            'code': 404,
            'data': None,
            'message': '场馆不存在'
        }), 404
    except ValueError as e:
        return jsonify({
            'code': 400,
            'data': None,
            'message': f'数据类型错误: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新场馆失败: {str(e)}'
        }), 500


@venue_crud_bp.route('/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    """
    删除场馆
    ---
    tags:
      - 场馆管理
    summary: 删除场馆
    description: 删除指定的场馆（软删除，设置is_active为false）
    parameters:
      - name: venue_id
        in: path
        required: true
        description: 场馆ID
        schema:
          type: integer
    responses:
      200:
        description: 删除成功
      404:
        description: 场馆不存在
    """
    try:
        venue = Venue.query.get_or_404(venue_id)

        # 软删除：设置为不活跃状态
        venue.is_active = False
        venue.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'code': 0,
            'data': None,
            'message': '删除成功'
        }), 200

    except NotFound:
        return jsonify({
            'code': 404,
            'data': None,
            'message': '场馆不存在'
        }), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除场馆失败: {str(e)}'
        }), 500


@venue_crud_bp.route('/toggle-status/<int:venue_id>', methods=['PATCH'])
def toggle_venue_status(venue_id):
    """
    切换场馆状态
    ---
    tags:
      - 场馆管理
    summary: 切换场馆状态
    description: 切换场馆的启用/禁用状态
    parameters:
      - name: venue_id
        in: path
        required: true
        description: 场馆ID
        schema:
          type: integer
    responses:
      200:
        description: 状态切换成功
      404:
        description: 场馆不存在
    """
    try:
        venue = Venue.query.get_or_404(venue_id)

        # 切换状态
        venue.is_active = not venue.is_active
        venue.updated_at = datetime.utcnow()

        db.session.commit()

        status_text = '启用' if venue.is_active else '禁用'

        return jsonify({
            'code': 0,
            'data': {
                'id': venue.id,
                'is_active': venue.is_active,
                'status_text': status_text
            },
            'message': f'{status_text}成功'
        }), 200

    except NotFound:
        return jsonify({
            'code': 404,
            'data': None,
            'message': '场馆不存在'
        }), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'状态切换失败: {str(e)}'
        }), 500


@venue_crud_bp.route('/stats', methods=['GET'])
def get_venue_stats():
    """
    获取场馆统计信息
    ---
    tags:
      - 场馆管理
    summary: 获取场馆统计
    description: 获取场馆总数、启用状态统计等
    responses:
      200:
        description: 获取成功
    """
    try:
        # 获取基础统计
        total_venues = Venue.query.count()
        active_venues = Venue.query.filter_by(is_active=True).count()
        inactive_venues = total_venues - active_venues

        # 按分类统计
        category_stats = db.session.query(
            VenueCategory.name,
            db.func.count(Venue.id).label('count')
        ).outerjoin(Venue, VenueCategory.id == Venue.category_id)\
         .filter(Venue.is_active == True)\
         .group_by(VenueCategory.id, VenueCategory.name)\
         .all()

        stats = {
            'total_venues': total_venues,
            'active_venues': active_venues,
            'inactive_venues': inactive_venues,
            'category_stats': [
                {'category_name': stat[0], 'count': stat[1]} 
                for stat in category_stats
            ]
        }

        return jsonify({
            'code': 0,
            'data': stats,
            'message': '获取成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取统计信息失败: {str(e)}'
        }), 500
"""
场馆管理API模块
"""

from datetime import datetime
import json
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy import or_, and_
from sqlalchemy.orm import contains_eager
from models import db, Venue, VenueCategory, Booking, BookingStatus, User, VenueReview
from config import BaseConfig

# 创建蓝图
venue_bp = Blueprint('venue', __name__, url_prefix='/api/venue')


def get_user_id_from_header():
    """从请求头获取用户ID"""
    user_id = request.headers.get('User-Id')
    if not user_id:
        return None
    try:
        return int(user_id)
    except (ValueError, TypeError):
        return None


@venue_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        # 获取查询参数
        name = request.args.get('name', '').strip()

        # 构建基础查询
        query = VenueCategory.query.filter_by(is_active=True)

        # 如果传入了name参数，添加名称过滤条件
        if name:
            query = query.filter(VenueCategory.name.like(f'%{name}%'))

        # 执行查询并排序
        categories = query.order_by(
            VenueCategory.sort_order.asc(),
            VenueCategory.id.asc()
        ).all()

        return jsonify({
            'code': 0,
            'data': [category.to_dict() for category in categories],
            'message': '获取成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取分类失败: {str(e)}'
        }), 500


@venue_bp.route('/categories', methods=['POST'])
def create_category():
    """
    新增场馆分类
    ---
    tags:
      - 场馆管理
    summary: 新增场馆分类
    description: 创建一个新的场馆分类
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: 分类名称
                example: "篮球场"
              description:
                type: string
                description: 分类描述
                example: "室内外篮球场地"
              icon:
                type: string
                description: 图标类名
                example: "basketball"
              sort_order:
                type: integer
                description: 排序顺序，数字越小越靠前
                example: 1
              is_active:
                type: boolean
                description: 是否启用
                example: true
    responses:
      200:
        description: 创建成功
      400:
        description: 请求参数错误
      409:
        description: 分类名称已存在
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

        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        icon = data.get('icon', '').strip()
        sort_order = data.get('sort_order', 0)
        is_active = data.get('is_active', True)

        # 验证必填字段
        if not name:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '分类名称不能为空'
            }), 400

        # 检查分类名称是否已存在
        existing_category = VenueCategory.query.filter_by(name=name).first()
        if existing_category:
            return jsonify({
                'code': 409,
                'data': None,
                'message': '分类名称已存在'
            }), 409

        # 创建新分类
        category = VenueCategory(
            name=name,
            description=description,
            icon=icon,
            sort_order=sort_order,
            is_active=is_active
        )

        db.session.add(category)
        db.session.commit()

        return jsonify({
            'code': 0,
            'data': category.to_dict(),
            'message': '创建成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建分类失败: {str(e)}'
        }), 500


@venue_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """
    编辑场馆分类
    ---
    tags:
      - 场馆管理
    summary: 编辑场馆分类
    description: 更新指定分类的信息
    parameters:
      - name: category_id
        in: path
        required: true
        description: 分类ID
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
                description: 分类名称
                example: "篮球场"
              description:
                type: string
                description: 分类描述
                example: "室内外篮球场地"
              icon:
                type: string
                description: 图标类名
                example: "basketball"
              sort_order:
                type: integer
                description: 排序顺序
                example: 1
              is_active:
                type: boolean
                description: 是否启用
                example: true
    responses:
      200:
        description: 更新成功
      400:
        description: 请求参数错误
      404:
        description: 分类不存在
      409:
        description: 分类名称已存在
    """
    try:
        # 获取当前用户（这里可以添加管理员权限验证）
        user_id = 1  # 默认用户ID，无需验证

        # 检查分类是否存在
        category = VenueCategory.query.get(category_id)
        if not category:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '分类不存在'
            }), 404

        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '请求数据不能为空'
            }), 400

        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        icon = data.get('icon', '').strip()
        sort_order = data.get('sort_order')
        is_active = data.get('is_active')

        # 验证分类名称（如果提供了）
        if name and name != category.name:
            # 检查新名称是否已被其他分类使用
            existing_category = VenueCategory.query.filter_by(name=name).filter(VenueCategory.id != category_id).first()
            if existing_category:
                return jsonify({
                    'code': 409,
                    'data': None,
                    'message': '分类名称已存在'
                }), 409
            category.name = name

        # 更新其他字段
        if description is not None:
            category.description = description

        if icon is not None:
            category.icon = icon

        if sort_order is not None:
            category.sort_order = sort_order

        if is_active is not None:
            category.is_active = is_active

        db.session.commit()

        return jsonify({
            'code': 0,
            'data': category.to_dict(),
            'message': '更新成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新分类失败: {str(e)}'
        }), 500


@venue_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        # 获取当前用户（这里可以添加管理员权限验证）
        user_id = 1  # 默认用户ID，无需验证

        # 检查分类是否存在
        category = VenueCategory.query.get(category_id)
        if not category:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '分类不存在'
            }), 404

        # 检查该分类下是否还有活跃的场馆
        active_venues = Venue.query.filter_by(
            category_id=category_id,
            is_active=True
        ).count()

        if active_venues > 0:
            return jsonify({
                'code': 409,
                'data': None,
                'message': f'该分类下还有 {active_venues} 个活跃场馆，无法删除'
            }), 409

        # 软删除：将分类设置为不活跃状态
        category.is_active = False
        db.session.commit()

        return jsonify({
            'code': 0,
            'data': None,
            'message': '删除成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除分类失败: {str(e)}'
        }), 500


@venue_bp.route('/list', methods=['GET'])
def get_venues():
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', BaseConfig.PAGE_SIZE, type=int)
        keyword = request.args.get('keyword', '').strip()
        category_id = request.args.get('category_id', type=int)
        is_hot = request.args.get('is_hot', 0, type=int)

        # 限制每页最大数量
        page_size = min(page_size, BaseConfig.MAX_PAGE_SIZE)
        page = max(1, page)  # 确保页码至少为1

        # 构建查询
        query = Venue.query.filter_by(is_active=True)

        # 搜索关键词
        if keyword:
            query = query.filter(
                or_(
                    Venue.name.contains(keyword),
                    Venue.type.contains(keyword),
                    Venue.location.contains(keyword),
                    Venue.description.contains(keyword)
                )
            )

        # 分类筛选
        if category_id:
            query = query.filter(Venue.category_id == category_id)

        # 热门筛选（这里简化为按价格范围判断热门）
        if is_hot:
            query = query.filter(Venue.price_per_hour >= 80)

        # 总数查询
        total = query.count()

        # 分页查询
        venues = query.order_by(Venue.created_at.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()

        # 计算总页数
        total_pages = (total + page_size - 1) // page_size

        return jsonify({
            'code': 0,
            'data': {
                'venues': [venue.to_dict() for venue in venues],
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
            'message': f'获取场馆列表失败: {str(e)}'
        }), 500


@venue_bp.route('/create', methods=['POST'])
def create_venue():
    """
    创建场馆
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
                example: "奥体中心羽毛球馆"
              type:
                type: string
                description: 场馆类型
                example: "羽毛球"
              location:
                type: string
                description: 场馆地址
                example: "北京市朝阳区奥体中心"
              price:
                type: number
                description: 每小时价格
                example: 80.0
              capacity:
                type: integer
                description: 容量（人数）
                example: 4
              contact_phone:
                type: string
                description: 联系电话
                example: "13800138000"
              business_hours:
                type: string
                description: 营业时间
                example: "09:00-22:00"
              description:
                type: string
                description: 场馆描述
                example: "专业羽毛球场地，设施完善"
              facilities:
                type: string
                description: 设施描述
                example: "新风系统、专业照明、更衣室"
              is_active:
                type: boolean
                description: 是否启用
                example: true
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

        name = data.get('name', '').strip()
        venue_type = data.get('type', '').strip()
        location = data.get('location', '').strip()
        price = data.get('price', 0)
        capacity = data.get('capacity', 1)
        contact_phone = data.get('contact_phone', '').strip()
        business_hours = data.get('business_hours', '').strip()
        description = data.get('description', '').strip()
        facilities = data.get('facilities', '').strip()
        is_active = data.get('is_active', True)

        # 验证必填字段
        if not name:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '场馆名称不能为空'
            }), 400

        if not venue_type:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '场馆类型不能为空'
            }), 400

        if not location:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '场馆地址不能为空'
            }), 400

        if price <= 0:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '价格必须大于0'
            }), 400

        if capacity <= 0:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '容量必须大于0'
            }), 400

        # 检查场馆名称是否已存在
        existing_venue = Venue.query.filter_by(name=name).first()
        if existing_venue:
            return jsonify({
                'code': 409,
                'data': None,
                'message': '场馆名称已存在'
            }), 409

        # 创建新场馆（使用第一个分类或创建默认分类）
        category = VenueCategory.query.filter_by(is_active=True).first()
        if not category:
            category = VenueCategory(name="其他", description="其他类型场馆", is_active=True)
            db.session.add(category)
            db.session.flush()

        # 创建新场馆
        venue = Venue(
            name=name,
            type=venue_type,
            location=location,
            price_per_hour=price,
            capacity=capacity,
            contact_phone=contact_phone,
            business_hours=business_hours,
            description=description,
            facilities=facilities,
            is_active=is_active,
            category_id=category.id
        )

        db.session.add(venue)
        db.session.commit()

        return jsonify({
            'code': 0,
            'data': venue.to_dict(),
            'message': '创建成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建场馆失败: {str(e)}'
        }), 500


@venue_bp.route('/update', methods=['POST'])
def update_venue():
    """
    更新场馆
    ---
    tags:
      - 场馆管理
    summary: 更新场馆
    description: 更新指定场馆的信息
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              id:
                type: integer
                description: 场馆ID
                example: 1
              name:
                type: string
                description: 场馆名称
                example: "奥体中心羽毛球馆"
              type:
                type: string
                description: 场馆类型
                example: "羽毛球"
              location:
                type: string
                description: 场馆地址
                example: "北京市朝阳区奥体中心"
              price:
                type: number
                description: 每小时价格
                example: 80.0
              capacity:
                type: integer
                description: 容量（人数）
                example: 4
              contact_phone:
                type: string
                description: 联系电话
                example: "13800138000"
              business_hours:
                type: string
                description: 营业时间
                example: "09:00-22:00"
              description:
                type: string
                description: 场馆描述
                example: "专业羽毛球场地，设施完善"
              facilities:
                type: string
                description: 设施描述
                example: "新风系统、专业照明、更衣室"
              is_active:
                type: boolean
                description: 是否启用
                example: true
    responses:
      200:
        description: 更新成功
      400:
        description: 请求参数错误
      404:
        description: 场馆不存在
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

        venue_id = data.get('id')
        if not venue_id:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '场馆ID不能为空'
            }), 400

        # 查找场馆
        venue = Venue.query.get(venue_id)
        if not venue:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '场馆不存在'
            }), 404

        name = data.get('name', '').strip()
        venue_type = data.get('type', '').strip()
        location = data.get('location', '').strip()
        price = data.get('price', 0)
        capacity = data.get('capacity', 1)
        contact_phone = data.get('contact_phone', '').strip()
        business_hours = data.get('business_hours', '').strip()
        description = data.get('description', '').strip()
        facilities = data.get('facilities', '').strip()
        is_active = data.get('is_active', True)

        # 验证必填字段
        if not name:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '场馆名称不能为空'
            }), 400

        if not venue_type:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '场馆类型不能为空'
            }), 400

        if not location:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '场馆地址不能为空'
            }), 400

        if price <= 0:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '价格必须大于0'
            }), 400

        if capacity <= 0:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '容量必须大于0'
            }), 400

        # 检查场馆名称是否已存在（排除当前场馆）
        existing_venue = Venue.query.filter(
            Venue.name == name,
            Venue.id != venue_id
        ).first()
        if existing_venue:
            return jsonify({
                'code': 409,
                'data': None,
                'message': '场馆名称已存在'
            }), 409

        # 更新场馆信息
        venue.name = name
        venue.type = venue_type
        venue.location = location
        venue.price_per_hour = price
        venue.capacity = capacity
        venue.contact_phone = contact_phone
        venue.business_hours = business_hours
        venue.description = description
        venue.facilities = facilities
        venue.is_active = is_active

        db.session.commit()

        return jsonify({
            'code': 0,
            'data': venue.to_dict(),
            'message': '更新成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新场馆失败: {str(e)}'
        }), 500


@venue_bp.route('/delete', methods=['POST'])
def delete_venue():
    """
    删除场馆
    ---
    tags:
      - 场馆管理
    summary: 删除场馆
    description: 删除指定的场馆（软删除，设置is_active为false）
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              id:
                type: integer
                description: 场馆ID
                example: 1
    responses:
      200:
        description: 删除成功
      400:
        description: 请求参数错误
      404:
        description: 场馆不存在
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

        venue_id = data.get('id')
        if not venue_id:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '场馆ID不能为空'
            }), 400

        # 查找场馆
        venue = Venue.query.get(venue_id)
        if not venue:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '场馆不存在'
            }), 404

        # 软删除：设置为不可用
        venue.is_active = False
        db.session.commit()

        return jsonify({
            'code': 0,
            'data': None,
            'message': '删除成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除场馆失败: {str(e)}'
        }), 500


@venue_bp.route('/batchDelete', methods=['POST'])
def batch_delete_venues():
    """
    批量删除场馆
    ---
    tags:
      - 场馆管理
    summary: 批量删除场馆
    description: 批量删除指定的场馆（软删除）
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              ids:
                type: array
                description: 场馆ID列表
                items:
                  type: integer
                example: [1, 2, 3]
    responses:
      200:
        description: 批量删除成功
      400:
        description: 请求参数错误
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

        ids = data.get('ids', [])
        if not ids:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '请选择要删除的场馆'
            }), 400

        # 查找并批量删除场馆
        venues = Venue.query.filter(Venue.id.in_(ids)).all()
        if not venues:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '未找到要删除的场馆'
            }), 404

        # 软删除：设置为不可用
        for venue in venues:
            venue.is_active = False

        db.session.commit()

        return jsonify({
            'code': 0,
            'data': {
                'deleted_count': len(venues)
            },
            'message': f'成功删除 {len(venues)} 个场馆'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'批量删除场馆失败: {str(e)}'
        }), 500


@venue_bp.route('/hot', methods=['GET'])
def get_hot_venues():
    """
    获取热门场馆
    ---
    tags:
      - 场馆管理
    summary: 获取热门场馆
    description: 获取推荐的高评分或高热度场馆
    parameters:
      - name: limit
        in: query
        description: 返回数量限制
        schema:
          type: integer
          default: 10
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
                  type: array
                  items:
                    $ref: '#/components/schemas/Venue'
                message:
                  type: string
                  example: "获取成功"
    """
    try:
        limit = request.args.get('limit', 10, type=int)

        # 获取热门场馆（按创建时间和价格综合判断）
        venues = Venue.query.filter_by(is_active=True) \
            .order_by(Venue.price_per_hour.desc(), Venue.created_at.desc()) \
            .limit(limit) \
            .all()

        return jsonify({
            'code': 0,
            'data': [venue.to_dict() for venue in venues],
            'message': '获取成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取热门场馆失败: {str(e)}'
        }), 500


@venue_bp.route('/<int:venue_id>', methods=['GET'])
def get_venue_detail(venue_id):
    """
    获取场馆详情
    ---
    tags:
      - 场馆管理
    summary: 获取场馆详情
    description: 根据场馆ID获取详细信息
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
        content:
          application/json:
            schema:
              type: object
              properties:
                code:
                  type: integer
                  example: 0
                data:
                  $ref: '#/components/schemas/Venue'
                message:
                  type: string
                  example: "获取成功"
      404:
        description: 场馆不存在
    """
    try:
        venue = Venue.query.get(venue_id)

        if not venue or not venue.is_active:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '场馆不存在'
            }), 404

        return jsonify({
            'code': 0,
            'data': venue.to_dict(),
            'message': '获取成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取场馆详情失败: {str(e)}'
        }), 500


@venue_bp.route('/<int:venue_id>/availability', methods=['GET'])
def check_venue_availability(venue_id):
    """
    检查场馆可用时间
    ---
    tags:
      - 场馆管理
    summary: 检查场馆可用时间
    description: 检查指定场馆在指定日期的可用时间段
    parameters:
      - name: venue_id
        in: path
        required: true
        description: 场馆ID
        schema:
          type: integer
      - name: date
        in: query
        required: true
        description: 查询日期 (YYYY-MM-DD)
        schema:
          type: string
          format: date
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
                    date:
                      type: string
                      format: date
                    venue_id:
                      type: integer
                    available_slots:
                      type: array
                      items:
                        type: object
                        properties:
                          start_time:
                            type: string
                            format: time
                          end_time:
                            type: string
                            format: time
                          available:
                            type: boolean
                message:
                  type: string
                  example: "获取成功"
      404:
        description: 场馆不存在
      400:
        description: 请求参数错误
    """
    try:
        # 检查场馆是否存在
        venue = Venue.query.get(venue_id)
        if not venue or not venue.is_active:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '场馆不存在'
            }), 404

        # 获取查询日期
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '缺少查询日期'
            }), 400

        try:
            query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '日期格式错误，请使用YYYY-MM-DD格式'
            }), 400

        # 获取该日期的所有预约
        bookings = Booking.query.filter(
            and_(
                Booking.venue_id == venue_id,
                Booking.booking_date == query_date,
                Booking.status != BookingStatus.CANCELLED
            )
        ).all()

        # 生成可用时间段（假设营业时间为8:00-22:00，每小时一个时间段）
        time_slots = []
        from datetime import time
        start_hour = 8
        end_hour = 22

        for hour in range(start_hour, end_hour):
            slot_start = time(hour, 0)
            slot_end = time(hour + 1, 0)

            # 检查该时间段是否可用
            is_available = True
            for booking in bookings:
                # 如果预约时间与当前时间段重叠，则不可用
                if not (booking.end_time <= slot_start or booking.start_time >= slot_end):
                    is_available = False
                    break

            time_slots.append({
                'start_time': slot_start.strftime('%H:%M'),
                'end_time': slot_end.strftime('%H:%M'),
                'available': is_available
            })

        return jsonify({
            'code': 0,
            'data': {
                'date': date_str,
                'venue_id': venue_id,
                'available_slots': time_slots
            },
            'message': '获取成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'检查可用时间失败: {str(e)}'
        }), 500


@venue_bp.route('/banners', methods=['GET'])
def get_banners():
    """
    获取轮播图数据
    ---
    tags:
      - 场馆管理
    summary: 获取轮播图数据
    description: 获取首页展示的轮播图信息
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
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      image:
                        type: string
                        description: 图片URL
                      title:
                        type: string
                        description: 图片标题
                      link:
                        type: string
                        description: 跳转链接
                message:
                  type: string
                  example: "获取成功"
    """
    try:
        # 模拟轮播图数据（实际应该从数据库读取）
        banners = [
            {
                'id': 1,
                'image': '/static/banner/1.jpg',
                'title': '奥林匹克体育中心',
                'link': '/venue/1'
            },
            {
                'id': 2,
                'image': '/static/banner/2.jpg',
                'title': '市民健身中心',
                'link': '/venue/2'
            },
            {
                'id': 3,
                'image': '/static/banner/3.jpg',
                'title': '大学城体育馆',
                'link': '/venue/3'
            }
        ]

        return jsonify({
            'code': 0,
            'data': banners,
            'message': '获取成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取轮播图失败: {str(e)}'
        }), 500


@venue_bp.route('/search', methods=['GET'])
def search_venues():
    """
    搜索场馆
    ---
    tags:
      - 场馆管理
    summary: 搜索场馆
    description: 根据关键词搜索场馆
    parameters:
      - name: q
        in: query
        required: true
        description: 搜索关键词
        schema:
          type: string
      - name: category
        in: query
        required: false
        description: 场馆分类ID
        schema:
          type: integer
      - name: location
        in: query
        required: false
        description: 地理位置
        schema:
          type: string
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
                  type: array
                  items:
                    $ref: '#/components/schemas/Venue'
                message:
                  type: string
                  example: "搜索成功"
      400:
        description: 请求参数错误
    """
    try:
        q = request.args.get('q', '').strip()
        if not q:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '搜索关键词不能为空'
            }), 400

        category_id = request.args.get('category', type=int)
        location = request.args.get('location', '').strip()

        query = Venue.query.filter(
            and_(
                Venue.is_active == True,
                or_(
                    Venue.name.contains(q),
                    Venue.description.contains(q),
                    Venue.location.contains(q)
                )
            )
        )

        if category_id:
            query = query.filter(Venue.category_id == category_id)

        if location:
            query = query.filter(Venue.location.contains(location))

        venues = query.limit(20).all()

        return jsonify({
            'code': 0,
            'data': [venue.to_dict() for venue in venues],
            'message': '搜索成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'搜索失败: {str(e)}'
        }), 500


@venue_bp.route('/<int:venue_id>/reviews', methods=['POST'])
def create_venue_review(venue_id):
    """
    创建场馆评价
    ---
    tags:
      - 场馆管理
    summary: 创建场馆评价
    description: 用户对场馆进行评价
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
              rating:
                type: integer
                minimum: 1
                maximum: 5
                description: 评分（1-5星）
                example: 5
              comment:
                type: string
                description: 评价内容
                example: "场地很棒，设施完善，服务态度很好！"
              images:
                type: array
                items:
                  type: string
                description: 评价图片URL列表
                example: ["/uploads/review1.jpg", "/uploads/review2.jpg"]
    responses:
      200:
        description: 评价创建成功
      400:
        description: 请求参数错误
      404:
        description: 场馆不存在
      409:
        description: 已评价过该场馆
    """
    try:
        # 获取当前用户
        user_id = 1  # 默认用户ID，无需验证

        # 检查场馆是否存在
        venue = Venue.query.get(venue_id)
        if not venue or not venue.is_active:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '场馆不存在'
            }), 404

        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '请求数据不能为空'
            }), 400

        rating = data.get('rating')
        content = data.get('comment', '').strip()
        images = data.get('images', [])

        # 验证评分
        if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '评分必须是1-5的整数'
            }), 400

        # 验证评价内容
        if not content.strip():
            return jsonify({
                'code': 400,
                'data': None,
                'message': '评价内容不能为空'
            }), 400

        # 检查是否已经评价过该场馆
        existing_review = VenueReview.query.filter_by(
            venue_id=venue_id,
            user_id=user_id
        ).first()

        if existing_review:
            return jsonify({
                'code': 409,
                'data': None,
                'message': '您已经评价过该场馆'
            }), 409

        # 创建评价
        review = VenueReview(
            venue_id=venue_id,
            user_id=user_id,
            rating=rating,
            title='',  # 暂时设为空，未来可扩展
            content=content,
            images=json.dumps(images) if images else None,
            is_public=True,
            is_verified=False
        )

        db.session.add(review)
        db.session.commit()

        return jsonify({
            'code': 0,
            'data': review.to_dict(),
            'message': '评价创建成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建评价失败: {str(e)}'
        }), 500


@venue_bp.route('/<int:venue_id>/reviews', methods=['GET'])
def get_venue_reviews(venue_id):
    """
    获取场馆评价列表
    ---
    tags:
      - 场馆管理
    summary: 获取场馆评价列表
    description: 获取指定场馆的所有评价，支持分页和筛选
    parameters:
      - name: venue_id
        in: path
        required: true
        description: 场馆ID
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
          default: 10
      - name: rating
        in: query
        description: 评分筛选（1-5）
        schema:
          type: integer
      - name: sort_by
        in: query
        description: 排序方式（latest:最新 first:最早 highest:最高分 lowest:最低分）
        schema:
          type: string
          default: latest
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
                    reviews:
                      type: array
                      items:
                        $ref: '#/components/schemas/VenueReview'
                    pagination:
                      type: object
                      properties:
                        current_page:
                          type: integer
                          example: 1
                        page_size:
                          type: integer
                          example: 10
                        total:
                          type: integer
                          example: 50
                        total_pages:
                          type: integer
                          example: 5
                    rating_summary:
                      type: object
                      properties:
                        average_rating:
                          type: number
                          example: 4.5
                        total_reviews:
                          type: integer
                          example: 50
                        rating_distribution:
                          type: object
                          properties:
                            "5":
                              type: integer
                              example: 25
                            "4":
                              type: integer
                              example: 15
                            "3":
                              type: integer
                              example: 8
                            "2":
                              type: integer
                              example: 2
                            "1":
                              type: integer
                              example: 0
                message:
                  type: string
                  example: "获取成功"
      404:
        description: 场馆不存在
    """
    try:
        # 检查场馆是否存在
        venue = Venue.query.get(venue_id)
        if not venue or not venue.is_active:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '场馆不存在'
            }), 404

        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        rating = request.args.get('rating', type=int)
        sort_by = request.args.get('sort_by', 'latest')

        # 限制每页最大数量
        page_size = min(page_size, 50)
        page = max(1, page)  # 确保页码至少为1

        # 构建查询 - 不使用join加载用户信息，而是分别查询
        query = VenueReview.query.filter_by(venue_id=venue_id, is_public=True)

        # 评分筛选
        if rating:
            query = query.filter(VenueReview.rating == rating)

        # 排序
        if sort_by == 'latest':
            query = query.order_by(VenueReview.created_at.desc())
        elif sort_by == 'first':
            query = query.order_by(VenueReview.created_at.asc())
        elif sort_by == 'highest':
            query = query.order_by(VenueReview.rating.desc(), VenueReview.created_at.desc())
        elif sort_by == 'lowest':
            query = query.order_by(VenueReview.rating.asc(), VenueReview.created_at.desc())

        # 总数查询
        total = query.count()

        # 分页查询
        reviews = query.offset((page - 1) * page_size).limit(page_size).all()

        # 收集用户ID列表以便一次性查询所有相关用户
        user_ids = [review.user_id for review in reviews]
        users = User.query.filter(User.id.in_(user_ids)).all()
        user_dict = {user.id: user for user in users}

        # 计算总页数
        total_pages = (total + page_size - 1) // page_size

        # 获取评分统计
        rating_stats = db.session.query(
            VenueReview.rating,
            db.func.count(VenueReview.id)
        ).filter_by(venue_id=venue_id, is_public=True) \
            .group_by(VenueReview.rating).all()

        rating_distribution = {str(i): 0 for i in range(1, 6)}
        total_reviews = 0
        rating_sum = 0

        for rating_val, count in rating_stats:
            rating_distribution[str(rating_val)] = count
            total_reviews += count
            rating_sum += rating_val * count

        average_rating = round(rating_sum / total_reviews, 1) if total_reviews > 0 else 0

        # 构建返回数据
        reviews_data = []
        for review in reviews:
            user = user_dict.get(review.user_id)
            review_data = {
                'id': review.id,
                'rating': review.rating,
                'title': review.title,
                'content': review.content,
                'images': json.loads(review.images) if review.images else [],
                'is_verified': review.is_verified,
                'like_count': review.like_count,
                'dislike_count': review.dislike_count,
                'created_at': review.created_at.isoformat() if review.created_at else None,
                'updated_at': review.updated_at.isoformat() if review.updated_at else None,
                'user': {
                    'id': user.id if user else review.user_id,
                    'username': user.username if user else '',
                    'avatar': user.avatar if user and hasattr(user, 'avatar') else None,
                    'nickname': user.nickname if user and hasattr(user, 'nickname') else (user.username if user else '')
                } if user else None
            }
            reviews_data.append(review_data)

        return jsonify({
            'code': 0,
            'data': {
                'reviews': reviews_data,
                'pagination': {
                    'current_page': page,
                    'page_size': page_size,
                    'total': total,
                    'total_pages': total_pages
                },
                'rating_summary': {
                    'average_rating': average_rating,
                    'total_reviews': total_reviews,
                    'rating_distribution': rating_distribution
                }
            },
            'message': '获取成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取评价列表失败: {str(e)}'
        }), 500


@venue_bp.route('/reviews/<int:review_id>/helpful', methods=['POST'])
def mark_review_helpful(review_id):
    """
    标记评价为有用
    ---
    tags:
      - 场馆管理
    summary: 标记评价为有用
    description: 用户认为某条评价有用，可以标记它
    parameters:
      - name: review_id
        in: path
        required: true
        description: 评价ID
        schema:
          type: integer
    responses:
      200:
        description: 标记成功
      404:
        description: 评价不存在
      409:
        description: 已经标记过该评价
    """
    try:
        # 获取当前用户
        user_id = 1  # 默认用户ID，无需验证

        # 检查评价是否存在
        review = VenueReview.query.get(review_id)
        if not review or not review.is_public:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '评价不存在'
            }), 404

        # 更新点赞数量
        review.like_count += 1
        db.session.commit()

        return jsonify({
            'code': 0,
            'data': {
                'like_count': review.like_count
            },
            'message': '标记成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'标记失败: {str(e)}'
        }), 500


@venue_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    删除评价
    ---
    tags:
      - 场馆管理
    summary: 删除评价
    description: 用户删除自己的评价
    parameters:
      - name: review_id
        in: path
        required: true
        description: 评价ID
        schema:
          type: integer
    responses:
      200:
        description: 删除成功
      404:
        description: 评价不存在或无权限删除
    """
    try:
        # 获取当前用户
        user_id = 1  # 默认用户ID，无需验证

        # 检查评价是否存在且属于当前用户
        review = VenueReview.query.filter_by(
            id=review_id,
            user_id=user_id
        ).first()

        if not review:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '评价不存在或无权限删除'
            }), 404

        # 删除评价
        db.session.delete(review)
        db.session.commit()

        return jsonify({
            'code': 0,
            'data': None,
            'message': '删除成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除评价失败: {str(e)}'
        }), 500


# ====== 管理员接口 ======

@venue_bp.route('/venue_reviews', methods=['POST'])
def create_venue_review_admin():
    """
    创建场馆评价（管理员接口）
    ---
    tags:
      - 场馆管理
    summary: 创建场馆评价
    description: 管理员创建新的场馆评价
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
              user_id:
                type: integer
                description: 用户ID
              rating:
                type: integer
                description: 评分(1-5)
              title:
                type: string
                description: 评价标题
              content:
                type: string
                description: 评价内容
              images:
                type: array
                items:
                  type: string
                description: 评价图片列表
              is_verified:
                type: boolean
                description: 是否已验证
              is_public:
                type: boolean
                description: 是否公开
    responses:
      200:
        description: 创建成功
      400:
        description: 请求参数错误
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '请求数据不能为空'
            }), 400

        # 验证必填字段
        required_fields = ['venue_id', 'user_id', 'rating', 'content']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'{field}不能为空'
                }), 400

        # 检查场馆和用户是否存在
        venue = Venue.query.get(data['venue_id'])
        if not venue:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '场馆不存在'
            }), 404

        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404

        # 创建评价
        review = VenueReview(
            venue_id=data['venue_id'],
            user_id=data['user_id'],
            rating=data['rating'],
            title=data.get('title', ''),
            content=data['content'],
            images=json.dumps(data.get('images', [])),
            is_verified=data.get('is_verified', False),
            is_public=data.get('is_public', True)
        )

        db.session.add(review)
        db.session.commit()

        return jsonify({
            'code': 200,
            'data': {
                'id': review.id,
                'venue_id': review.venue_id,
                'user_id': review.user_id,
                'rating': review.rating,
                'title': review.title,
                'content': review.content,
                'images': json.loads(review.images) if review.images else [],
                'is_verified': review.is_verified,
                'is_public': review.is_public,
                'like_count': review.like_count,
                'dislike_count': review.dislike_count,
                'created_at': review.created_at.isoformat() if review.created_at else None
            },
            'message': '创建成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建评价失败: {str(e)}'
        }), 500


@venue_bp.route('/venue_reviews/<int:review_id>', methods=['PUT'])
def update_venue_review(review_id):
    """
    更新场馆评价（管理员接口）
    ---
    tags:
      - 场馆管理
    summary: 更新场馆评价
    description: 管理员更新指定的场馆评价
    parameters:
      - name: review_id
        in: path
        required: true
        description: 评价ID
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              rating:
                type: integer
                description: 评分(1-5)
              title:
                type: string
                description: 评价标题
              content:
                type: string
                description: 评价内容
              images:
                type: array
                items:
                  type: string
                description: 评价图片列表
              is_verified:
                type: boolean
                description: 是否已验证
              is_public:
                type: boolean
                description: 是否公开
    responses:
      200:
        description: 更新成功
      404:
        description: 评价不存在
    """
    try:
        # 获取评价
        review = VenueReview.query.get(review_id)
        if not review:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '评价不存在'
            }), 404

        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '请求数据不能为空'
            }), 400

        # 更新字段
        if 'rating' in data:
            review.rating = data['rating']
        if 'title' in data:
            review.title = data['title']
        if 'content' in data:
            review.content = data['content']
        if 'images' in data:
            review.images = json.dumps(data['images'])
        if 'is_verified' in data:
            review.is_verified = data['is_verified']
        if 'is_public' in data:
            review.is_public = data['is_public']

        review.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'code': 200,
            'data': {
                'id': review.id,
                'venue_id': review.venue_id,
                'user_id': review.user_id,
                'rating': review.rating,
                'title': review.title,
                'content': review.content,
                'images': json.loads(review.images) if review.images else [],
                'is_verified': review.is_verified,
                'is_public': review.is_public,
                'like_count': review.like_count,
                'dislike_count': review.dislike_count,
                'created_at': review.created_at.isoformat() if review.created_at else None,
                'updated_at': review.updated_at.isoformat() if review.updated_at else None
            },
            'message': '更新成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新评价失败: {str(e)}'
        }), 500


@venue_bp.route('/venue_reviews/<int:review_id>', methods=['DELETE'])
def delete_venue_review_admin(review_id):
    """
    删除场馆评价（管理员接口）
    ---
    tags:
      - 场馆管理
    summary: 删除场馆评价
    description: 管理员删除指定的场馆评价
    parameters:
      - name: review_id
        in: path
        required: true
        description: 评价ID
        schema:
          type: integer
    responses:
      200:
        description: 删除成功
      404:
        description: 评价不存在
    """
    try:
        # 获取评价
        review = VenueReview.query.get(review_id)
        if not review:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '评价不存在'
            }), 404

        # 删除评价
        db.session.delete(review)
        db.session.commit()

        return jsonify({
            'code': 200,
            'data': None,
            'message': '删除成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除评价失败: {str(e)}'
        }), 500


@venue_bp.route('/venue_reviews/list', methods=['GET'])
def get_all_venue_reviews():
    """
    获取所有场馆评价列表（管理员接口）
    ---
    tags:
      - 场馆管理
    summary: 获取所有场馆评价列表
    description: 管理员查询所有场馆评价信息
    parameters:
      - name: user_id
        in: query
        description: 用户ID过滤
        schema:
          type: integer
      - name: venue_id
        in: query
        description: 场馆ID过滤
        schema:
          type: integer
      - name: rating
        in: query
        description: 评分过滤
        schema:
          type: integer
      - name: page
        in: query
        description: 页码
        schema:
          type: integer
          default: 1
      - name: size
        in: query
        description: 每页数量
        schema:
          type: integer
          default: 10
    responses:
      200:
        description: 获取成功
      500:
        description: 获取失败
    """
    try:
        # 获取查询参数
        user_id = request.args.get('user_id', type=int)
        venue_id = request.args.get('venue_id', type=int)
        rating = request.args.get('rating', type=int)
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)

        # 构建查询 - 直接查询不尝试预加载关系
        query = VenueReview.query

        # 添加过滤条件
        if user_id:
            query = query.filter(VenueReview.user_id == user_id)
        if venue_id:
            query = query.filter(VenueReview.venue_id == venue_id)
        if rating:
            query = query.filter(VenueReview.rating == rating)

        # 排序
        query = query.order_by(VenueReview.created_at.desc())

        # 总数查询
        total = query.count()

        # 分页查询
        reviews = query.offset((page - 1) * size).limit(size).all()

        # 构建返回数据
        venue_reviews = []
        for review in reviews:
            # 获取用户信息
            user = User.query.get(review.user_id) if review.user_id else None
            venue = Venue.query.get(review.venue_id) if review.venue_id else None

            review_data = {
                'id': review.id,
                'user_id': review.user_id,
                'venue_id': review.venue_id,
                'rating': review.rating,
                'title': review.title,
                'comment': review.content,  # 使用comment字段匹配前端期望
                'content': review.content,
                'images': json.loads(review.images) if review.images else [],
                'is_verified': review.is_verified,
                'like_count': review.like_count,
                'dislike_count': review.dislike_count,
                'helpful_count': review.like_count,  # 兼容字段
                'created_at': review.created_at.isoformat() if review.created_at else None,
                'updated_at': review.updated_at.isoformat() if review.updated_at else None,
                'user': {
                    'id': user.id if user else 0,
                    'username': user.username if user else '',
                    'avatar': user.avatar if user and hasattr(user, 'avatar') else None,
                    'nickname': user.nickname if user and hasattr(user, 'nickname') else (user.username if user else '')
                } if user else None,
                'venue': {
                    'id': venue.id if venue else 0,
                    'name': venue.name if venue else '',
                    'location': venue.location if venue else ''
                } if venue else None
            }
            venue_reviews.append(review_data)

        return jsonify({
            'code': 200,
            'data': {
                'venue_reviews': venue_reviews,
                'pagination': {
                    'page': page,
                    'size': size,
                    'total': total,
                    'pages': (total + size - 1) // size
                }
            },
            'message': '获取成功'
        }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取场馆评价列表失败: {str(e)}'
        }), 500
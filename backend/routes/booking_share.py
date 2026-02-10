#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
费用分摊API模块
基于用户提供的BookingShare模型提供完整的CRUD操作
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import and_, or_, desc
from models import db, User, BookingShare

# 创建蓝图
booking_share_bp = Blueprint('booking_share', __name__, url_prefix='/api/booking-share')

def get_user_id_from_header():
    """从请求头获取用户ID"""
    user_id = request.headers.get('User-Id')
    if not user_id:
        return None
    try:
        return int(user_id)
    except (ValueError, TypeError):
        return None

@booking_share_bp.route('/create', methods=['POST'])
def create_booking_share():
    """创建费用分摊记录"""
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['booking_id', 'event_name', 'user_id', 'share_amount']
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'缺少必需字段: {field}'
                }), 400
        
        # 验证用户是否存在
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': f'用户ID {data["user_id"]} 不存在'
            }), 404
        
        # 验证分摊金额
        try:
            share_amount = float(data['share_amount'])
            if share_amount <= 0:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '分摊金额必须大于0'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'code': 400,
                'data': None,
                'message': '分摊金额格式错误'
            }), 400
        
        # 验证已付金额
        paid_amount = float(data.get('paid_amount', 0))
        if paid_amount < 0:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '已付金额不能为负数'
            }), 400
        
        if paid_amount > share_amount:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '已付金额不能超过分摊金额'
            }), 400
        
        # 创建费用分摊记录
        share = BookingShare(
            booking_id=data['booking_id'],
            event_name=data['event_name'],
            user_id=data['user_id'],
            share_amount=share_amount,
            paid_amount=paid_amount,
            is_paid=paid_amount >= share_amount
        )
        
        db.session.add(share)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': share.to_dict(),
            'message': '费用分摊记录创建成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建费用分摊失败: {str(e)}'
        }), 500

@booking_share_bp.route('/event/<event_name>/shares', methods=['GET'])
def get_event_shares(event_name):
    """获取指定事件的费用分摊列表"""
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        
        # 查询该事件的所有分摊记录
        shares = BookingShare.query.filter_by(event_name=event_name).order_by(
            desc(BookingShare.created_at)
        ).paginate(
            page=page,
            per_page=page_size,
            error_out=False
        )
        
        # 手动关联用户信息
        share_data = []
        for share in shares.items:
            share_dict = share.to_dict()
            # 手动获取用户信息
            user = User.query.get(share.user_id)
            if user:
                share_dict['user'] = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            share_data.append(share_dict)
        
        return jsonify({
            'code': 0,
            'data': {
                'shares': share_data,
                'total': shares.total,
                'pages': shares.pages,
                'current_page': page,
                'page_size': page_size
            },
            'message': f'获取事件 "{event_name}" 的费用分摊列表成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取费用分摊列表失败: {str(e)}'
        }), 500

@booking_share_bp.route('/user/<int:user_id>/shares', methods=['GET'])
def get_user_shares(user_id):
    """获取指定用户的费用分摊记录"""
    try:
        # 验证用户身份
        current_user_id = 1  # 默认用户ID，无需验证
        
        # 只能查看自己的记录
        if current_user_id != user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '只能查看自己的费用分摊记录'
            }), 403
        
        # 验证用户是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404
        
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        
        # 查询用户的分摊记录
        shares = BookingShare.query.filter_by(user_id=user_id).order_by(
            desc(BookingShare.created_at)
        ).paginate(
            page=page,
            per_page=page_size,
            error_out=False
        )
        
        share_data = [share.to_dict() for share in shares.items]
        
        return jsonify({
            'code': 0,
            'data': {
                'shares': share_data,
                'total': shares.total,
                'pages': shares.pages,
                'current_page': page,
                'page_size': page_size
            },
            'message': '获取用户分摊记录成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取用户分摊记录失败: {str(e)}'
        }), 500

@booking_share_bp.route('/<int:share_id>/update', methods=['PUT', 'PATCH'])
def update_booking_share(share_id):
    """更新费用分摊记录"""
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        data = request.get_json()
        
        # 查找费用分摊记录
        share = BookingShare.query.get(share_id)
        if not share:
            return jsonify({
                'code': 404,
                'data': None,
                'message': f'费用分摊记录 ID {share_id} 不存在'
            }), 404
        
        # 只能更新自己的记录
        if share.user_id != user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '只能更新自己的费用分摊记录'
            }), 403
        
        # 更新字段
        if 'share_amount' in data:
            try:
                share_amount = float(data['share_amount'])
                if share_amount <= 0:
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '分摊金额必须大于0'
                    }), 400
                share.share_amount = share_amount
            except (ValueError, TypeError):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '分摊金额格式错误'
                }), 400
        
        if 'paid_amount' in data:
            try:
                paid_amount = float(data['paid_amount'])
                if paid_amount < 0:
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '已付金额不能为负数'
                    }), 400
                
                if paid_amount > float(share.share_amount):
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '已付金额不能超过分摊金额'
                    }), 400
                
                share.paid_amount = paid_amount
                share.is_paid = paid_amount >= float(share.share_amount)
            except (ValueError, TypeError):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '已付金额格式错误'
                }), 400
        
        share.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': share.to_dict(),
            'message': '费用分摊记录更新成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新费用分摊失败: {str(e)}'
        }), 500

@booking_share_bp.route('/<int:share_id>/delete', methods=['DELETE'])
def delete_booking_share(share_id):
    """删除费用分摊记录"""
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        # 查找费用分摊记录
        share = BookingShare.query.get(share_id)
        if not share:
            return jsonify({
                'code': 404,
                'data': None,
                'message': f'费用分摊记录 ID {share_id} 不存在'
            }), 404
        
        # 只能删除自己的记录
        if share.user_id != user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '只能删除自己的费用分摊记录'
            }), 403
        
        db.session.delete(share)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': None,
            'message': '费用分摊记录删除成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除费用分摊失败: {str(e)}'
        }), 500

@booking_share_bp.route('/event/<event_name>/summary', methods=['GET'])
def get_event_summary(event_name):
    """获取事件费用分摊汇总"""
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        # 查询该事件的所有分摊记录
        shares = BookingShare.query.filter_by(event_name=event_name).all()
        
        if not shares:
            return jsonify({
                'code': 404,
                'data': None,
                'message': f'事件 "{event_name}" 没有费用分摊记录'
            }), 404
        
        # 计算汇总信息
        total_shares = len(shares)
        total_amount = sum(float(share.share_amount) for share in shares)
        total_paid = sum(float(share.paid_amount) for share in shares)
        paid_count = sum(1 for share in shares if share.is_paid)
        
        return jsonify({
            'code': 0,
            'data': {
                'event_name': event_name,
                'total_shares': total_shares,
                'total_amount': total_amount,
                'total_paid': total_paid,
                'unpaid_amount': total_amount - total_paid,
                'paid_count': paid_count,
                'unpaid_count': total_shares - paid_count,
                'completion_rate': round(paid_count / total_shares * 100, 2) if total_shares > 0 else 0
            },
            'message': f'获取事件 "{event_name}" 费用汇总成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取费用汇总失败: {str(e)}'
        }), 500

@booking_share_bp.route('/<int:share_id>', methods=['GET'])
def get_booking_share(share_id):
    """获取单个费用分摊记录详情"""
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        # 查找费用分摊记录
        share = BookingShare.query.get(share_id)
        if not share:
            return jsonify({
                'code': 404,
                'data': None,
                'message': f'费用分摊记录 ID {share_id} 不存在'
            }), 404
        
        # 只能查看自己的记录
        if share.user_id != user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '只能查看自己的费用分摊记录'
            }), 403
        
        # 手动关联用户信息
        share_dict = share.to_dict()
        user = User.query.get(share.user_id)
        if user:
            share_dict['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        
        return jsonify({
            'code': 0,
            'data': share_dict,
            'message': '获取费用分摊记录详情成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取费用分摊详情失败: {str(e)}'
        }), 500
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取用户分摊记录失败: {str(e)}'
        }), 500

@booking_share_bp.route('/<int:share_id>/pay', methods=['PUT'])
def update_payment(share_id):
    """更新支付信息"""
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取分摊记录
        share = BookingShare.query.get(share_id)
        if not share:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '费用分摊记录不存在'
            }), 404
        
        # 只能更新自己的记录
        if share.user_id != user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '无权修改此分摊记录'
            }), 403
        
        data = request.get_json()
        
        # 验证支付金额
        if 'paid_amount' in data:
            try:
                paid_amount = float(data['paid_amount'])
                if paid_amount < 0 or paid_amount > float(share.share_amount):
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '已付金额不能为负数或超过分摊金额'
                    }), 400
                share.paid_amount = paid_amount
                share.is_paid = paid_amount >= float(share.share_amount)
            except (ValueError, TypeError):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '已付金额格式错误'
                }), 400
        
        # 如果只传了is_paid字段，则根据分摊金额更新已付金额
        if 'is_paid' in data and 'paid_amount' not in data:
            if data['is_paid']:
                share.paid_amount = share.share_amount
                share.is_paid = True
            else:
                share.is_paid = False
        
        share.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': share.to_dict(),
            'message': '支付信息更新成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新支付信息失败: {str(e)}'
        }), 500



@booking_share_bp.route('/<int:share_id>', methods=['PUT'])
def update_share(share_id):
    """更新费用分摊记录"""
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取分摊记录
        share = BookingShare.query.get(share_id)
        if not share:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '费用分摊记录不存在'
            }), 404
        
        # 只能更新自己的记录
        if share.user_id != user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '无权修改此分摊记录'
            }), 403
        
        data = request.get_json()
        
        # 更新允许的字段
        if 'share_amount' in data:
            try:
                share_amount = float(data['share_amount'])
                if share_amount <= 0:
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '分摊金额必须大于0'
                    }), 400
                share.share_amount = share_amount
                # 重新计算是否已付清
                share.is_paid = float(share.paid_amount) >= share_amount
            except (ValueError, TypeError):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '分摊金额格式错误'
                }), 400
        
        if 'paid_amount' in data:
            try:
                paid_amount = float(data['paid_amount'])
                if paid_amount < 0 or paid_amount > float(share.share_amount):
                    return jsonify({
                        'code': 400,
                        'data': None,
                        'message': '已付金额不能为负数或超过分摊金额'
                    }), 400
                share.paid_amount = paid_amount
                share.is_paid = paid_amount >= float(share.share_amount)
            except (ValueError, TypeError):
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '已付金额格式错误'
                }), 400
        
        share.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': share.to_dict(),
            'message': '费用分摊记录更新成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新费用分摊记录失败: {str(e)}'
        }), 500

@booking_share_bp.route('/<int:share_id>', methods=['DELETE'])
def delete_share(share_id):
    """删除费用分摊记录"""
    try:
        user_id = 1  # 默认用户ID，无需验证
        
        # 获取分摊记录
        share = BookingShare.query.get(share_id)
        if not share:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '费用分摊记录不存在'
            }), 404
        
        # 只能删除自己的记录
        if share.user_id != user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '无权删除此分摊记录'
            }), 403
        
        db.session.delete(share)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'data': None,
            'message': '费用分摊记录删除成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除费用分摊记录失败: {str(e)}'
        }), 500

@booking_share_bp.route('/user/<int:user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    """获取用户费用分摊统计信息"""
    try:
        current_user_id = 1  # 默认用户ID，无需验证
        
        # 只能查看自己的统计信息
        if user_id != current_user_id:
            return jsonify({
                'code': 403,
                'data': None,
                'message': '无权查看此用户统计信息'
            }), 403
        
        # 获取用户的分摊记录
        shares = BookingShare.query.filter_by(user_id=user_id).all()
        
        if not shares:
            return jsonify({
                'code': 0,
                'data': {
                    'total_events': 0,
                    'total_amount': 0,
                    'total_paid': 0,
                    'total_unpaid': 0,
                    'paid_events': 0,
                    'unpaid_events': 0,
                    'completion_rate': 0
                },
                'message': '该用户没有分摊记录'
            }), 200
        
        # 计算统计信息
        total_amount = sum(float(share.share_amount) for share in shares)
        total_paid = sum(float(share.paid_amount) for share in shares)
        total_unpaid = total_amount - total_paid
        paid_events = sum(1 for share in shares if share.is_paid)
        unpaid_events = len(shares) - paid_events
        unique_events = len(set(share.event_name for share in shares))
        
        return jsonify({
            'code': 0,
            'data': {
                'total_events': unique_events,
                'total_records': len(shares),
                'total_amount': round(total_amount, 2),
                'total_paid': round(total_paid, 2),
                'total_unpaid': round(total_unpaid, 2),
                'paid_events': paid_events,
                'unpaid_events': unpaid_events,
                'completion_rate': round(paid_events / len(shares) * 100, 2) if shares else 0
            },
            'message': '获取用户统计信息成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取用户统计信息失败: {str(e)}'
        }), 500
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
体育预约系统 - 简化版后端API服务
使用SQLite数据库，减少依赖
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 数据库配置
DATABASE = 'sports_booking.db'

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # 允许按列名访问
    return conn

# 初始化数据库
def init_db():
    """初始化数据库表"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            phone TEXT,
            avatar TEXT,
            role TEXT DEFAULT 'user',
            is_active INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建场馆分类表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS venue_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            icon_url TEXT,
            sort_order INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建场馆表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS venues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            address TEXT,
            latitude REAL,
            longitude REAL,
            images TEXT,
            facilities TEXT,
            operating_hours TEXT,
            price_per_hour REAL,
            max_booking_hours INTEGER DEFAULT 2,
            is_active INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES venue_categories (id)
        )
    ''')
    
    # 创建预约表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            venue_id INTEGER NOT NULL,
            booking_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            duration INTEGER NOT NULL,
            total_price REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            payment_status TEXT DEFAULT 'unpaid',
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (venue_id) REFERENCES venues (id)
        )
    ''')
    
    # 创建活动表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            activity_type TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            location TEXT NOT NULL,
            max_participants INTEGER NOT NULL,
            current_participants INTEGER DEFAULT 0,
            status TEXT DEFAULT 'upcoming',
            is_active INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建教练表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coaches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            experience_years INTEGER DEFAULT 0,
            phone TEXT,
            email TEXT,
            description TEXT,
            hourly_rate REAL DEFAULT 0.0,
            is_active INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 添加示例数据
def add_sample_data():
    """添加示例数据"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # 添加默认管理员用户
    password_hash = generate_password_hash('123456')
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, full_name, phone, role)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('admin', 'admin@example.com', password_hash, '管理员', '13800138000', 'admin'))
    
    # 添加普通用户
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, full_name, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', ('user1', 'user1@example.com', password_hash, '张三', '13800138001'))
    
    # 添加场馆分类
    categories = [
        ('篮球', '篮球场馆'),
        ('足球', '足球场馆'),
        ('羽毛球', '羽毛球场地'),
        ('网球', '网球场'),
        ('游泳', '游泳池'),
        ('健身', '健身房')
    ]
    
    for name, desc in categories:
        cursor.execute('''
            INSERT INTO venue_categories (name, description)
            VALUES (?, ?)
        ''', (name, desc))
    
    # 添加场馆
    venues = [
        ('朝阳篮球馆', '专业篮球场地，设施完善', 1, '朝阳区建国路88号', 150.0),
        ('绿茵足球场', '标准11人足球场，草皮优良', 2, '海淀区中关村大街1号', 200.0),
        ('羽毛球中心', '专业羽毛球场地，防滑地板', 3, '东城区王府井大街100号', 80.0)
    ]
    
    for venue in venues:
        cursor.execute('''
            INSERT INTO venues (name, description, category_id, address, price_per_hour)
            VALUES (?, ?, ?, ?, ?)
        ''', venue)
    
    # 添加示例活动
    activities = [
        ('篮球训练营', '专业篮球技能训练', 'training', '2024-01-15', '2024-01-15', '14:00', '16:00', '朝阳篮球馆', 20),
        ('足球友谊赛', '周末足球友谊比赛', 'competition', '2024-01-20', '2024-01-20', '09:00', '11:00', '绿茵足球场', 22),
        ('羽毛球培训班', '羽毛球基础技能培训', 'training', '2024-01-22', '2024-01-22', '19:00', '21:00', '羽毛球中心', 16)
    ]
    
    for activity in activities:
        cursor.execute('''
            INSERT INTO activities (title, description, activity_type, start_date, end_date,
                                  start_time, end_time, location, max_participants)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', activity)
    
    conn.commit()
    conn.close()

# 添加示例数据
add_sample_data()

@app.route('/')
def index():
    """首页"""
    return jsonify({
        'message': '体育预约系统API服务',
        'version': '1.0',
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'message': '服务运行正常',
        'timestamp': datetime.now().isoformat()
    })

# 用户认证相关API
@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'code': 400,
            'data': None,
            'message': '用户名和密码不能为空'
        }), 400
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, email, password_hash, full_name, phone, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user[3], password):
            return jsonify({
                'code': 401,
                'data': None,
                'message': '用户名或密码错误'
            }), 401
        
        user_data = {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'full_name': user[4],
            'phone': user[5],
            'role': user[6]
        }
        
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': user_data,
            'message': '登录成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'登录失败: {str(e)}'
        }), 500

# 场馆分类管理API
@app.route('/api/venue/categories', methods=['GET'])
def get_venue_categories():
    """获取场馆分类列表"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, icon_url, sort_order, is_active, created_at
            FROM venue_categories
            ORDER BY sort_order ASC, id ASC
        ''')
        
        categories = cursor.fetchall()
        result = []
        
        for category in categories:
            result.append({
                'id': category[0],
                'name': category[1],
                'description': category[2],
                'icon_url': category[3],
                'sort_order': category[4],
                'is_active': bool(category[5]),
                'created_at': category[6]
            })
        
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': result,
            'message': '获取成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取失败: {str(e)}'
        }), 500

@app.route('/api/venue/categories', methods=['POST'])
def create_venue_category():
    """创建场馆分类"""
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description', '')
    
    if not name:
        return jsonify({
            'code': 400,
            'data': None,
            'message': '分类名称不能为空'
        }), 400
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO venue_categories (name, description)
            VALUES (?, ?)
        ''', (name, description))
        
        category_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': {'id': category_id},
            'message': '创建成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建失败: {str(e)}'
        }), 500

@app.route('/api/venue/categories/<int:category_id>', methods=['PUT'])
def update_venue_category(category_id):
    """更新场馆分类"""
    data = request.get_json()
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # 检查分类是否存在
        cursor.execute("SELECT id FROM venue_categories WHERE id = ?", (category_id,))
        if not cursor.fetchone():
            return jsonify({
                'code': 404,
                'data': None,
                'message': '分类不存在'
            }), 404
        
        # 构建更新字段
        update_fields = []
        params = []
        
        if 'name' in data:
            update_fields.append('name = ?')
            params.append(data['name'])
        
        if 'description' in data:
            update_fields.append('description = ?')
            params.append(data['description'])
        
        if 'is_active' in data:
            update_fields.append('is_active = ?')
            params.append(1 if data['is_active'] else 0)
        
        if not update_fields:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '没有有效的更新字段'
            }), 400
        
        params.append(category_id)
        
        cursor.execute(f'''
            UPDATE venue_categories SET {', '.join(update_fields)} 
            WHERE id = ?
        ''', params)
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': {'id': category_id},
            'message': '更新成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新失败: {str(e)}'
        }), 500

@app.route('/api/venue/categories/<int:category_id>', methods=['DELETE'])
def delete_venue_category(category_id):
    """删除场馆分类"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM venue_categories WHERE id = ?", (category_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({
                'code': 404,
                'data': None,
                'message': '分类不存在'
            }), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': None,
            'message': '删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除失败: {str(e)}'
        }), 500

@app.route('/api/venue/categories/batch_delete', methods=['POST'])
def batch_delete_venue_categories():
    """批量删除场馆分类"""
    data = request.get_json()
    ids = data.get('ids', [])
    
    if not ids:
        return jsonify({
            'code': 400,
            'data': None,
            'message': '没有选择要删除的分类'
        }), 400
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in ids])
        cursor.execute(f'DELETE FROM venue_categories WHERE id IN ({placeholders})', ids)
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': {'deleted_count': deleted_count},
            'message': f'成功删除 {deleted_count} 个分类'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'批量删除失败: {str(e)}'
        }), 500

# 场馆管理API
@app.route('/api/venue/list', methods=['GET'])
def get_venues():
    """获取场馆列表"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        keyword = request.args.get('keyword', '').strip()
        category_id = request.args.get('category_id')
        
        offset = (page - 1) * size
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if keyword:
            where_conditions.append('v.name LIKE ?')
            params.append(f'%{keyword}%')
        
        if category_id:
            where_conditions.append('v.category_id = ?')
            params.append(category_id)
        
        where_clause = ''
        if where_conditions:
            where_clause = 'WHERE ' + ' AND '.join(where_conditions)
        
        # 查询总数
        cursor.execute(f'SELECT COUNT(*) FROM venues v {where_clause}', params)
        total = cursor.fetchone()[0]
        
        # 查询数据
        query = f'''
            SELECT v.id, v.name, v.description, v.category_id, vc.name as category_name,
                   v.address, v.price_per_hour, v.images, v.operating_hours
            FROM venues v
            LEFT JOIN venue_categories vc ON v.category_id = vc.id
            {where_clause}
            ORDER BY v.created_at DESC
            LIMIT ? OFFSET ?
        '''
        
        cursor.execute(query, params + [size, offset])
        venues = cursor.fetchall()
        
        result = []
        for venue in venues:
            # 处理images字段
            images = []
            if venue[6]:  # images字段
                try:
                    import json
                    images = json.loads(venue[6])
                except:
                    images = []
            
            result.append({
                'id': venue[0],
                'name': venue[1],
                'description': venue[2],
                'category_id': venue[3],
                'category_name': venue[4],
                'address': venue[5],
                'price_per_hour': venue[6] if len(venue) > 6 else 0,
                'images': images,
                'operating_hours': venue[8] if len(venue) > 8 else ''
            })
        
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': result,
            'total': total,
            'message': '获取成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取失败: {str(e)}'
        }), 500

# 活动管理API
@app.route('/api/activity/list', methods=['GET'])
def get_activities():
    """获取活动列表"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        title = request.args.get('title', '').strip()
        activity_type = request.args.get('activity_type', '').strip()
        status = request.args.get('status', '').strip()
        
        offset = (page - 1) * size
        
        # 构建查询
        where_conditions = []
        params = []
        
        if title:
            where_conditions.append('title LIKE ?')
            params.append(f'%{title}%')
        
        if activity_type:
            where_conditions.append('activity_type = ?')
            params.append(activity_type)
            
        if status:
            where_conditions.append('status = ?')
            params.append(status)
        
        where_clause = ''
        if where_conditions:
            where_clause = 'WHERE ' + ' AND '.join(where_conditions)
        
        # 查询总数
        cursor.execute(f'SELECT COUNT(*) FROM activities {where_clause}', params)
        total = cursor.fetchone()[0]
        
        # 查询数据
        query = f'''
            SELECT id, title, description, activity_type, start_date, end_date,
                   start_time, end_time, location, max_participants, current_participants,
                   status, is_active, created_at
            FROM activities 
            {where_clause}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        '''
        
        cursor.execute(query, params + [size, offset])
        activities = cursor.fetchall()
        
        result = []
        for activity in activities:
            result.append({
                'id': activity[0],
                'title': activity[1],
                'description': activity[2],
                'activity_type': activity[3],
                'start_date': activity[4],
                'end_date': activity[5],
                'start_time': activity[6],
                'end_time': activity[7],
                'location': activity[8],
                'max_participants': activity[9],
                'current_participants': activity[10],
                'status': activity[11],
                'is_active': bool(activity[12]),
                'created_at': activity[13]
            })
        
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': result,
            'total': total,
            'message': '获取成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取失败: {str(e)}'
        }), 500

@app.route('/api/activity', methods=['POST'])
def create_activity():
    """创建活动"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['title', 'activity_type', 'start_date', 'end_date', 'start_time', 'end_time', 'location', 'max_participants']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'缺少必需字段: {field}'
                }), 400
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activities (title, description, activity_type, start_date, end_date,
                                  start_time, end_time, location, max_participants, 
                                  current_participants, status, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 'upcoming', 1)
        ''', (
            data['title'],
            data.get('description', ''),
            data['activity_type'],
            data['start_date'],
            data['end_date'],
            data['start_time'],
            data['end_time'],
            data['location'],
            data['max_participants']
        ))
        
        activity_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': {'id': activity_id},
            'message': '创建成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建失败: {str(e)}'
        }), 500

@app.route('/api/activity/<int:activity_id>', methods=['PUT'])
def update_activity(activity_id):
    """更新活动"""
    try:
        data = request.get_json()
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # 构建更新语句
        update_fields = []
        params = []
        
        allowed_fields = ['title', 'description', 'activity_type', 'start_date', 'end_date',
                        'start_time', 'end_time', 'location', 'max_participants', 'status', 'is_active']
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f'{field} = ?')
                params.append(data[field])
        
        if not update_fields:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '没有有效的更新字段'
            }), 400
        
        params.append(activity_id)
        
        cursor.execute(f'''
            UPDATE activities SET {', '.join(update_fields)} 
            WHERE id = ?
        ''', params)
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({
                'code': 404,
                'data': None,
                'message': '活动不存在'
            }), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': {'id': activity_id},
            'message': '更新成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新失败: {str(e)}'
        }), 500

@app.route('/api/activity/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    """删除活动"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({
                'code': 404,
                'data': None,
                'message': '活动不存在'
            }), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': None,
            'message': '删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除失败: {str(e)}'
        }), 500

@app.route('/api/activity/batch_delete', methods=['POST'])
def batch_delete_activities():
    """批量删除活动"""
    try:
        data = request.get_json()
        ids = data.get('ids', [])
        
        if not ids:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '没有选择要删除的活动'
            }), 400
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # 构建占位符
        placeholders = ','.join(['?' for _ in ids])
        cursor.execute(f'DELETE FROM activities WHERE id IN ({placeholders})', ids)
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': {'deleted_count': deleted_count},
            'message': f'成功删除 {deleted_count} 个活动'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'批量删除失败: {str(e)}'
        }), 500

# 用户管理API
@app.route('/api/user/list', methods=['GET'])
def get_user_list():
    """获取用户列表"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        username = request.args.get('username', '').strip()
        
        offset = (page - 1) * size
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if username:
            where_conditions.append('username LIKE ?')
            params.append(f'%{username}%')
        
        where_clause = ''
        if where_conditions:
            where_clause = 'WHERE ' + ' AND '.join(where_conditions)
        
        # 查询总数
        cursor.execute(f'SELECT COUNT(*) FROM users {where_clause}', params)
        total = cursor.fetchone()[0]
        
        # 查询数据
        query = f'''
            SELECT id, username, email, full_name, phone, avatar, role, is_active, created_at, updated_at
            FROM users
            {where_clause}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        '''
        
        cursor.execute(query, params + [size, offset])
        users = cursor.fetchall()
        
        result = []
        for user in users:
            result.append({
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3],
                'phone': user[4],
                'avatar': user[5],
                'role': user[6],
                'is_active': bool(user[7]),
                'created_at': user[8],
                'updated_at': user[9]
            })
        
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': {
                'list': result,
                'total_records': total,
                'current_page': page,
                'total_pages': (total + size - 1) // size
            },
            'message': '获取成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取失败: {str(e)}'
        }), 500

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """获取用户基本信息"""
    try:
        user_id = request.headers.get('User-Id')
        if not user_id:
            return jsonify({
                'code': 401,
                'data': None,
                'message': '用户身份验证失败'
            }), 401
        
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return jsonify({
                'code': 401,
                'data': None,
                'message': '用户身份验证失败'
            }), 401
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, full_name, phone, avatar, role, is_active, created_at, updated_at
            FROM users WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '用户不存在'
            }), 404
        
        return jsonify({
            'code': 0,
            'data': {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3],
                'phone': user[4],
                'avatar': user[5],
                'role': user[6],
                'is_active': bool(user[7]),
                'created_at': user[8],
                'updated_at': user[9]
            },
            'message': '获取成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取用户信息失败: {str(e)}'
        }), 500

# 预约管理API
@app.route('/api/bookings/list', methods=['GET'])
def get_booking_list():
    """获取预约列表"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        status = request.args.get('status', '').strip()
        
        offset = (page - 1) * size
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if status:
            where_conditions.append('status = ?')
            params.append(status)
        
        where_clause = ''
        if where_conditions:
            where_clause = 'WHERE ' + ' AND '.join(where_conditions)
        
        # 查询总数
        cursor.execute(f'SELECT COUNT(*) FROM bookings {where_clause}', params)
        total = cursor.fetchone()[0]
        
        # 查询数据
        query = f'''
            SELECT b.id, b.booking_date, b.start_time, b.end_time, b.duration, 
                   b.total_price, b.status, b.payment_status, b.notes,
                   u.username as user_name, v.name as venue_name
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN venues v ON b.venue_id = v.id
            {where_clause}
            ORDER BY b.created_at DESC
            LIMIT ? OFFSET ?
        '''
        
        cursor.execute(query, params + [size, offset])
        bookings = cursor.fetchall()
        
        result = []
        for booking in bookings:
            result.append({
                'id': booking[0],
                'booking_date': booking[1],
                'start_time': booking[2],
                'end_time': booking[3],
                'duration': booking[4],
                'total_price': booking[5],
                'status': booking[6],
                'payment_status': booking[7],
                'notes': booking[8],
                'user_name': booking[9],
                'venue_name': booking[10]
            })
        
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': {
                'list': result,
                'total_records': total,
                'current_page': page,
                'total_pages': (total + size - 1) // size
            },
            'message': '获取成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取失败: {str(e)}'
        }), 500

@app.route('/api/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    """更新预约状态"""
    try:
        data = request.get_json()
        status = data.get('status')
        notes = data.get('notes', '')
        
        if not status:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '状态不能为空'
            }), 400
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE bookings 
            SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, notes, booking_id))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({
                'code': 404,
                'data': None,
                'message': '预约不存在'
            }), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': None,
            'message': '更新成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新失败: {str(e)}'
        }), 500

@app.route('/api/bookings/batch-delete', methods=['POST'])
def batch_delete_bookings():
    """批量删除预约"""
    try:
        data = request.get_json()
        ids = data.get('ids', [])
        
        if not ids:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '没有选择要删除的预约'
            }), 400
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # 构建占位符
        placeholders = ','.join(['?' for _ in ids])
        cursor.execute(f'DELETE FROM bookings WHERE id IN ({placeholders})', ids)
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': {'deleted_count': deleted_count},
            'message': f'成功删除 {deleted_count} 个预约'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'批量删除失败: {str(e)}'
        }), 500

# 教练管理API
@app.route('/api/coaches', methods=['GET'])
def get_coach_list():
    """获取教练列表"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        name = request.args.get('name', '').strip()
        specialization = request.args.get('specialization', '').strip()
        
        offset = (page - 1) * size
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        # 注意：在简化版本中，我们先假设一个基本的coaches表结构
        # 如果表不存在，会返回空列表
        try:
            if name:
                where_conditions.append('name LIKE ?')
                params.append(f'%{name}%')
            
            if specialization:
                where_conditions.append('specialization LIKE ?')
                params.append(f'%{specialization}%')
            
            where_clause = ''
            if where_conditions:
                where_clause = 'WHERE ' + ' AND '.join(where_conditions)
            
            # 查询总数
            cursor.execute(f'SELECT COUNT(*) FROM coaches {where_clause}', params)
            total = cursor.fetchone()[0]
            
            # 查询数据
            query = f'''
                SELECT id, name, specialization, experience_years, phone, 
                       email, description, hourly_rate, is_active, created_at
                FROM coaches
                {where_clause}
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            '''
            
            cursor.execute(query, params + [size, offset])
            coaches = cursor.fetchall()
            
            result = []
            for coach in coaches:
                result.append({
                    'id': coach[0],
                    'name': coach[1],
                    'specialization': coach[2],
                    'experience_years': coach[3],
                    'phone': coach[4],
                    'email': coach[5],
                    'description': coach[6],
                    'hourly_rate': coach[7],
                    'is_active': bool(coach[8]),
                    'created_at': coach[9]
                })
            
        except sqlite3.OperationalError:
            # 如果coaches表不存在，返回空列表
            result = []
            total = 0
        
        conn.close()
        
        return jsonify({
            'code': 0,
            'data': {
                'list': result,
                'total_records': total,
                'current_page': page,
                'total_pages': (total + size - 1) // size if size > 0 else 0
            },
            'message': '获取成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取失败: {str(e)}'
        }), 500

@app.route('/api/coaches', methods=['POST'])
def create_coach():
    """创建教练"""
    try:
        data = request.get_json()
        name = data.get('name')
        specialization = data.get('specialization', '')
        experience_years = data.get('experience_years', 0)
        phone = data.get('phone', '')
        email = data.get('email', '')
        description = data.get('description', '')
        hourly_rate = data.get('hourly_rate', 0.0)
        
        if not name:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '教练姓名不能为空'
            }), 400
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO coaches (name, specialization, experience_years, phone, 
                                   email, description, hourly_rate, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            ''', (name, specialization, experience_years, phone, email, description, hourly_rate))
            
            coach_id = cursor.lastrowid
            conn.commit()
            
            return jsonify({
                'code': 0,
                'data': {'id': coach_id},
                'message': '创建成功'
            }), 201
            
        except sqlite3.OperationalError:
            # 如果coaches表不存在，返回错误
            return jsonify({
                'code': 500,
                'data': None,
                'message': '教练表不存在，请先初始化数据库'
            }), 500
        
        finally:
            conn.close()
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'创建失败: {str(e)}'
        }), 500

@app.route('/api/coaches/<int:coach_id>', methods=['PUT'])
def update_coach(coach_id):
    """更新教练信息"""
    try:
        data = request.get_json()
        
        # 构建动态更新字段
        update_fields = []
        update_values = []
        
        for field in ['name', 'specialization', 'experience_years', 'phone', 
                     'email', 'description', 'hourly_rate', 'is_active']:
            if field in data:
                update_fields.append(f'{field} = ?')
                update_values.append(data[field])
        
        if not update_fields:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '没有提供要更新的字段'
            }), 400
        
        update_values.append(coach_id)
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            update_sql = f'''
                UPDATE coaches 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            '''
            cursor.execute(update_sql, update_values)
            
            if cursor.rowcount == 0:
                conn.close()
                return jsonify({
                    'code': 404,
                    'data': None,
                    'message': '教练不存在'
                }), 404
            
            conn.commit()
            
            return jsonify({
                'code': 0,
                'data': None,
                'message': '更新成功'
            })
            
        except sqlite3.OperationalError:
            # 如果coaches表不存在，返回错误
            return jsonify({
                'code': 500,
                'data': None,
                'message': '教练表不存在'
            }), 500
        
        finally:
            conn.close()
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新失败: {str(e)}'
        }), 500

@app.route('/api/coaches/<int:coach_id>', methods=['DELETE'])
def delete_coach(coach_id):
    """删除教练"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM coaches WHERE id = ?', (coach_id,))
            
            if cursor.rowcount == 0:
                conn.close()
                return jsonify({
                    'code': 404,
                    'data': None,
                    'message': '教练不存在'
                }), 404
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'code': 0,
                'data': None,
                'message': '删除成功'
            })
            
        except sqlite3.OperationalError:
            # 如果coaches表不存在，返回错误
            return jsonify({
                'code': 500,
                'data': None,
                'message': '教练表不存在'
            }), 500
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'删除失败: {str(e)}'
        }), 500

@app.route('/api/coaches/batch-delete', methods=['POST'])
def batch_delete_coaches():
    """批量删除教练"""
    try:
        data = request.get_json()
        ids = data.get('ids', [])
        
        if not ids:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '没有选择要删除的教练'
            }), 400
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            # 构建占位符
            placeholders = ','.join(['?' for _ in ids])
            cursor.execute(f'DELETE FROM coaches WHERE id IN ({placeholders})', ids)
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return jsonify({
                'code': 0,
                'data': {'deleted_count': deleted_count},
                'message': f'成功删除 {deleted_count} 个教练'
            })
            
        except sqlite3.OperationalError:
            # 如果coaches表不存在，返回错误
            return jsonify({
                'code': 500,
                'data': None,
                'message': '教练表不存在'
            }), 500
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'批量删除失败: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("启动体育预约系统API服务...")
    print("访问地址: http://127.0.0.1:5000")
    print("健康检查: http://127.0.0.1:5000/health")
    app.run(host='0.0.0.0', port=5000, debug=False)
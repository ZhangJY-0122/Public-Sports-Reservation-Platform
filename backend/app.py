"""
Flask应用主入口
"""

import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Api

# 导入配置文件
from config import config

# 导入数据库模型
from models import db

# 导入路由蓝图
from routes.auth import auth_bp
from routes.venue import venue_bp
from routes.booking import booking_bp
from routes.user import user_bp
from routes.activity import activity_bp


# 创建Flask应用
def create_app(config_name=None):
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 选择配置
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    init_extensions(app)
    
    # 注册蓝图
    register_blueprints(app)
    
    # 配置路由
    register_routes(app)
    
    # 配置日志
    setup_logging(app)
    
    return app

def init_extensions(app):
    """初始化Flask扩展"""
    # 初始化数据库
    db.init_app(app)
    
    # 配置CORS
    cors = CORS(
        app,
        origins=["*", "http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080", "http://127.0.0.1:8080"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Content-Type", "Authorization", "User-Id", "X-Requested-With", "Accept", "Origin"],
        supports_credentials=True,
        max_age=86400,
        expose_headers=["Content-Length", "Content-Range"]
    )
    
    # 初始化Flask-RESTX（用于Swagger文档）
    api = Api(
        app,
        version='1.0',
        title='体育预约系统API',
        description='基于Flask开发的体育场馆预约系统后端API',
        doc='/api/docs/',
        prefix='/api'
    )
    
    # 将api对象保存到app实例中
    app.extensions['api'] = api

def register_blueprints(app):
    """注册蓝图"""
    # 注册认证蓝图
    app.register_blueprint(auth_bp)
    
    # 注册场馆管理蓝图
    app.register_blueprint(venue_bp)

    # 注册场馆CRUD蓝图
    from routes.venue_crud import venue_crud_bp
    app.register_blueprint(venue_crud_bp)
    

    # 注册预约管理蓝图
    app.register_blueprint(booking_bp)
    
    # 注册用户中心蓝图
    app.register_blueprint(user_bp)
    
    # 注册活动管理蓝图
    app.register_blueprint(activity_bp)

    # 注册教练管理蓝图
    from routes.coaches import coaches_bp
    app.register_blueprint(coaches_bp)
    

    
    # 注册好友管理蓝图
    from routes.friends import friends_bp
    app.register_blueprint(friends_bp)
    
    # 注册赛事管理蓝图
    from routes.events import events_bp
    app.register_blueprint(events_bp)
    
    # 注册费用分摊蓝图
    from routes.booking_share import booking_share_bp
    app.register_blueprint(booking_share_bp)

def register_routes(app):
    """注册路由"""
    
    @app.route('/')
    def index():
        """首页"""
        return jsonify({
            'message': '体育预约系统API服务',
            'version': '1.0',
            'status': 'running',
            'docs': '/api/docs/',
            'endpoints': {
                'auth': '/api/auth/',
                'venue': '/api/venue/',
                'booking': '/api/booking/',
                'user': '/api/user/',
                'activity': '/api/activity/',
                'coach': '/api/coach/',
                'booking-share': '/api/booking-share/'
            }
        })
    
    @app.route('/health')
    def health_check():
        """健康检查"""
        return jsonify({
            'status': 'healthy',
            'message': '服务运行正常',
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })
    
    @app.route('/api/system/info', methods=['GET'])
    def get_system_info():
        """获取系统信息"""
        import platform
        import sys
        
        return jsonify({
            'code': 0,
            'data': {
                'system': {
                    'platform': platform.platform(),
                    'python_version': sys.version,
                    'framework': 'Flask'
                },
                'api': {
                    'version': '1.0',
                    'status': 'running'
                },
                'database': {
                    'type': 'SQLAlchemy',
                    'connected': True
                }
            },
            'message': '获取成功'
        })
    
    @app.route('/api/upload', methods=['POST'])
    def upload_file():
        """文件上传接口"""
        try:
            from werkzeug.utils import secure_filename
            import uuid
            from datetime import datetime
            
            # 检查是否有文件上传
            if 'file' not in request.files:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '没有选择文件'
                }), 400
            
            file = request.files['file']
            
            # 检查文件是否为空
            if file.filename == '':
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '文件不能为空'
                }), 400
            
            # 检查文件类型
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
            if '.' not in file.filename:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': '无效的文件格式'
                }), 400
            
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            if file_extension not in allowed_extensions:
                return jsonify({
                    'code': 400,
                    'data': None,
                    'message': f'不支持的文件格式，支持的格式：{", ".join(allowed_extensions)}'
                }), 400
            
            # 创建上传目录
            upload_folder = os.path.join(app.root_path, 'static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            # 生成唯一文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}.{file_extension}"
            filename = secure_filename(unique_filename)
            
            # 保存文件
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # 生成文件URL
            file_url = f"/static/uploads/{filename}"
            
            # 获取文件信息
            file_size = os.path.getsize(file_path)
            
            return jsonify({
                'code': 0,
                'data': {
                    'filename': filename,
                    'original_name': file.filename,
                    'url': file_url,
                    'size': file_size,
                    'extension': file_extension,
                    'upload_time': datetime.now().isoformat()
                },
                'message': '上传成功'
            }), 200
            
        except Exception as e:
            return jsonify({
                'code': 500,
                'data': None,
                'message': f'文件上传失败: {str(e)}'
            }), 500
    
    @app.route('/api/debug/database_status', methods=['GET'])
    def get_database_status():
        """获取数据库状态信息"""
        try:
            # 导入相关模型
            from models import CoachBooking, Venue
            
            # 检查coach_bookings表结构
            columns = [column.name for column in CoachBooking.__table__.columns]
            has_venue_id = 'venue_id' in columns
            
            # 检查数据统计
            total_bookings = CoachBooking.query.count()
            bookings_with_venue = CoachBooking.query.filter(CoachBooking.venue_id.isnot(None)).count()
            bookings_without_venue = CoachBooking.query.filter(CoachBooking.venue_id.is_(None)).count()
            
            # 最近的预约记录
            recent_bookings = CoachBooking.query.order_by(CoachBooking.created_at.desc()).limit(3).all()
            
            # 获取示例记录
            sample_booking = None
            if total_bookings > 0:
                sample_booking = CoachBooking.query.first()
            
            # 统计各种状态的数据
            status_stats = {}
            for status in ['upcoming', 'confirmed', 'completed', 'cancelled']:
                count = CoachBooking.query.filter_by(status=status).count()
                status_stats[status] = count
            
            # 场馆数据统计
            total_venues = Venue.query.count()
            venues_with_price = Venue.query.filter(Venue.price_per_hour.isnot(None)).count()
            
            return jsonify({
                'code': 0,
                'message': '数据库状态检查成功',
                'data': {
                    # 表结构信息
                    'table_structure': {
                        'has_venue_id_column': has_venue_id,
                        'all_columns': columns,
                        'coach_bookings_columns_count': len(columns)
                    },
                    
                    # 数据统计
                    'data_statistics': {
                        'total_bookings': total_bookings,
                        'bookings_with_venue_id': bookings_with_venue,
                        'bookings_without_venue_id': bookings_without_venue,
                        'venue_id_coverage_rate': f"{(bookings_with_venue/total_bookings*100):.1f}%" if total_bookings > 0 else "0%"
                    },
                    
                    # 状态统计
                    'status_statistics': status_stats,
                    
                    # 场馆统计
                    'venue_statistics': {
                        'total_venues': total_venues,
                        'venues_with_price': venues_with_price
                    },
                    
                    # 示例数据
                    'sample_data': {
                        'first_booking': sample_booking.to_dict() if sample_booking else None,
                        'recent_bookings_count': len(recent_bookings),
                        'recent_bookings': [booking.to_dict() for booking in recent_bookings]
                    }
                }
            })
            
        except Exception as e:
            return jsonify({
                'code': -1,
                'message': f'数据库检查失败: {str(e)}',
                'data': None
            }), 500
    
    # 错误处理
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'code': 400,
            'data': None,
            'message': '请求参数错误'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'code': 401,
            'data': None,
            'message': '未授权访问'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'code': 403,
            'data': None,
            'message': '禁止访问'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'code': 404,
            'data': None,
            'message': '资源不存在'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'code': 405,
            'data': None,
            'message': '请求方法不允许'
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'code': 500,
            'data': None,
            'message': '服务器内部错误'
        }), 500

def setup_logging(app):
    """配置日志"""
    if not app.debug and not app.testing:
        # 生产环境日志配置
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = logging.FileHandler('logs/app.log', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('体育预约系统启动')

# 创建Flask应用实例
app = create_app()

if __name__ == '__main__':
    # 开发环境运行
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=False,
        use_reloader=False
    )
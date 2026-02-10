"""
配置文件 - 支持MySQL和SQLite切换
"""

import os
from datetime import timedelta


class BaseConfig:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'

    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # 分页配置
    PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    # 跨域配置
    CORS_ORIGINS = ["*"]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS = [
        "Content-Type",
        "Authorization",
        "X-User-ID",
        "X-User-Role",
        "Accept",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers"
    ]

    # 请求头用户ID字段
    USER_ID_HEADER = 'X-User-ID'
    USER_ROLE_HEADER = 'X-User-Role'


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    DEBUG = True

    # 数据库配置 - 切换到MySQL
    DATABASE_TYPE = 'mysql'

    if DATABASE_TYPE == 'mysql':
        # MySQL配置
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/sports_booking'

        # MySQL连接池配置 - 解决连接频繁中断问题
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_recycle': 300,  # 4分40秒，小于常见的300秒超时
            'pool_pre_ping': True,  # 启用连接检测
            'pool_size': 10,  # 根据并发量调整
            'max_overflow': 20,  # 最大溢出连接数
            'pool_timeout': 30,  # 获取连接超时时间
            'connect_args': {
                "charset": "utf8mb4",
                "collation": "utf8mb4_unicode_ci",
                "autocommit": True
            }
        }
    else:
        # SQLite配置
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                                  'sqlite:///instance//sports_booking.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    """生产环境配置"""
    DEBUG = False

    # MySQL数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # MySQL连接池配置 - 生产环境优化
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,  # 5分钟回收
        'pool_pre_ping': True,  # 启用连接检测
        'pool_size': 20,  # 生产环境连接池更大
        'max_overflow': 30,  # 最大溢出连接数
        'pool_timeout': 60,  # 获取连接超时时间
        'connect_args': {
            "charset": "utf8mb4",
            "collation": "utf8mb4_unicode_ci",
            "autocommit": True
        }
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
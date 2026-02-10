#!/usr/bin/env python3
"""
测试MySQL连接池配置是否生效
"""

from app import create_app
from models import db

def test_pool_config():
    """测试连接池配置"""
    app = create_app()
    
    with app.app_context():
        # 检查连接池配置
        engine = db.engine
        
        print("=" * 50)
        print("MySQL连接池配置验证")
        print("=" * 50)
        
        # 获取连接池配置信息
        pool = engine.pool
        print(f"连接池类: {type(pool).__name__}")
        print(f"基础连接数: {pool.size()}")
        print(f"空闲连接数: {pool.checkedin()}")
        print(f"正在使用连接数: {pool.checkedout()}")
        print(f"溢出连接数: {pool.overflow()}")
        print(f"是否启用pre_ping: {hasattr(engine, 'pool') and hasattr(pool, '_pre_ping')}")
        
        # 测试数据库连接
        try:
            with engine.connect() as conn:
                result = conn.execute(db.text("SELECT 1"))
                print("✅ 数据库连接测试: 成功")
        except Exception as e:
            print(f"❌ 数据库连接测试失败: {e}")
        
        print("=" * 50)

if __name__ == "__main__":
    test_pool_config()
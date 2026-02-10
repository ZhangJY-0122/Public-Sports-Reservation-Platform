"""
Flask应用启动脚本
用于开发和生产环境快速启动服务
"""

import os
import sys
import click
from flask.cli import FlaskGroup

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from migrate import init_database, reset_database

# 创建应用组
cli = FlaskGroup(create_app=create_app)

@cli.command("run")
@click.option("--host", "-h", default="0.0.0.0", help="服务器主机地址")
@click.option("--port", "-p", default=5000, help="服务器端口")
@click.option("--debug", "-d", is_flag=True, help="开启调试模式")
@click.option("--env", "-e", default="development", help="运行环境 (development/production)")
def run(host, port, debug, env):
    """启动开发服务器"""
    click.echo("🚀 启动体育预约系统API服务...")
    click.echo(f"🌐 环境: {env}")
    click.echo(f"🔗 地址: http://{host}:{port}")
    click.echo(f"📚 文档: http://{host}:{port}/api/docs/")
    click.echo(f"💡 健康检查: http://{host}:{port}/health")
    click.echo("-" * 50)
    
    # 设置环境变量
    os.environ['FLASK_ENV'] = env
    os.environ['FLASK_DEBUG'] = str(int(debug))
    
    app = create_app(env)
    
    if debug:
        click.echo("🐛 调试模式: 开启")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug,
        threaded=True
    )

@cli.command("init-db")
@click.option("--with-sample", "-s", is_flag=True, help="包含示例数据")
def init_db(with_sample):
    """初始化数据库"""
    click.echo("🗄️  初始化数据库...")
    
    app = create_app()
    with app.app_context():
        try:
            from migrate import create_tables
            create_tables(app)
            init_database(app)
            
            if with_sample:
                click.echo("📊 注意: 当前版本暂不支持示例数据...")
            
            click.echo("✅ 数据库初始化完成")
            
        except Exception as e:
            click.echo(f"❌ 数据库初始化失败: {str(e)}")
            sys.exit(1)

@cli.command("reset-db")
@click.confirmation_option(prompt="确定要重置数据库吗？这将删除所有数据！")
def reset_db():
    """重置数据库"""
    click.echo("🔄 重置数据库...")
    
    app = create_app()
    with app.app_context():
        try:
            reset_database(app)
            click.echo("✅ 数据库重置完成")
            
        except Exception as e:
            click.echo(f"❌ 数据库重置失败: {str(e)}")
            sys.exit(1)

@cli.command("db-status")
def db_status():
    """查看数据库状态"""
    app = create_app()
    with app.app_context():
        try:
            # 检查数据库连接
            result = db.session.execute("SELECT 1").fetchone()
            if result:
                click.echo("✅ 数据库连接正常")
                
                # 获取表信息
                from sqlalchemy import inspect
                inspector = inspect(db.engine)
                tables = inspector.get_table_names()
                click.echo(f"📋 数据库表数量: {len(tables)}")
                
                for table in tables:
                    click.echo(f"  - {table}")
                    
                # 获取用户数量
                from models import User
                user_count = User.query.count()
                click.echo(f"👥 用户总数: {user_count}")
                
            else:
                click.echo("❌ 数据库连接失败")
                
        except Exception as e:
            click.echo(f"❌ 数据库检查失败: {str(e)}")

@cli.command("test")
@click.option("--verbose", "-v", is_flag=True, help="详细输出")
def test(verbose):
    """运行测试"""
    click.echo("🧪 运行测试...")
    
    # 导入测试模块
    try:
        from test_api import main as test_main
    except ImportError as e:
        click.echo(f"❌ 无法导入测试模块: {e}")
        click.echo("💡 请确保 test_api.py 文件存在且在正确位置")
        sys.exit(1)
    
    if verbose:
        # 运行详细测试
        click.echo("📋 运行详细测试...")
    else:
        # 运行基础测试
        click.echo("📋 运行基础测试...")
    
    try:
        # 直接调用测试函数
        test_main()
        click.echo("✅ 所有测试通过")
    except Exception as e:
        click.echo(f"❌ 测试失败: {str(e)}")
        sys.exit(1)

@cli.command("config-check")
def config_check():
    """检查配置"""
    click.echo("⚙️  检查应用配置...")
    
    app = create_app()
    with app.app_context():
        config_obj = app.config
        
        click.echo(f"🔑 SECRET_KEY: {'已设置' if config_obj.get('SECRET_KEY') else '未设置'}")
        click.echo(f"🗄️  数据库类型: {config_obj.get('DATABASE_TYPE', 'sqlite')}")
        click.echo(f"🔗 数据库URI: {config_obj.get('SQLALCHEMY_DATABASE_URI')}")
        click.echo(f"🐛 调试模式: {config_obj.get('DEBUG', False)}")
        click.echo(f"🌐 CORS配置: {config_obj.get('CORS_ORIGINS')}")
        click.echo(f"📄 分页大小: {config_obj.get('PAGE_SIZE')}")

if __name__ == '__main__':
    cli()
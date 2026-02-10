#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库调试和修复脚本
"""

import sys
import os
import traceback

# 添加当前目录到Python路径
sys.path.append('.')

def debug_database():
    """调试数据库问题"""
    print("🔍 开始调试数据库问题...")
    
    try:
        from app import create_app
        from models import db
        import sqlalchemy as sa
        
        # 创建Flask应用
        app = create_app('development')
        
        print("✅ Flask应用创建成功")
        print(f"📋 数据库URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        with app.app_context():
            print("📝 尝试创建所有数据库表...")
            
            # 创建所有表
            db.create_all()
            print("✅ 数据库表创建成功")
            
            # 检查表是否存在
            inspector = sa.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 检查数据库表: {tables}")
            
            # 尝试手动测试每个模型
            from models import User, VenueCategory, Venue
            
            print("📋 测试模型导入...")
            print(f"  User模型: {User}")
            print(f"  VenueCategory模型: {VenueCategory}")  
            print(f"  Venue模型: {Venue}")
            
            # 测试数据查询
            print("🔍 测试数据查询...")
            
            # 查询分类数量
            categories_count = db.session.query(VenueCategory).count()
            print(f"  场馆分类数量: {categories_count}")
            
            # 查询场馆数量
            venues_count = db.session.query(Venue).count()
            print(f"  场馆数量: {venues_count}")
            
            # 查询用户数量
            users_count = db.session.query(User).count()
            print(f"  用户数量: {users_count}")
            
            if categories_count == 0:
                print("⚠️  数据库中没有分类数据，需要填充数据")
                
                # 手动创建分类数据
                test_categories = ['篮球场', '羽毛球场', '网球场', '游泳池', '乒乓球室', '健身房', '排球场', '足球场']
                for cat_name in test_categories:
                    category = VenueCategory(name=cat_name)
                    db.session.add(category)
                db.session.commit()
                print("✅ 已创建默认分类数据")
                
            print("🎉 数据库调试完成！")
            
    except Exception as e:
        print(f"❌ 数据库调试失败: {e}")
        print("📋 详细错误信息:")
        traceback.print_exc()

if __name__ == '__main__':
    debug_database()
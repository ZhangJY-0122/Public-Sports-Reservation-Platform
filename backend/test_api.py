#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
体育预约系统API测试脚本
测试各个API接口的功能和响应
"""

import requests
import json
from datetime import datetime

# API基础地址
BASE_URL = "http://127.0.0.1:5000"

def test_api(endpoint, method="GET", data=None, description=""):
    """测试API接口"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*60}")
    print(f"🔍 测试: {description}")
    print(f"📡 URL: {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        print(f"📊 状态码: {response.status_code}")
        print(f"📝 响应内容:")
        
        try:
            result = response.json()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except:
            print(response.text)
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🏃 体育预约系统API接口测试")
    print("="*60)
    
    # 测试健康检查
    test_api("/health", description="健康检查API")
    
    # 测试首页
    test_api("/", description="首页API")
    
    # 测试API接口
    test_api("/api/test", description="API测试接口")
    
    print(f"\n{'='*60}")
    print("🎉 测试完成!")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 提示：这是简化版测试服务，只包含基本的健康检查接口")
    print("💡 完整的体育预约系统功能需要启动 app_simple.py 服务")

if __name__ == "__main__":
    main()
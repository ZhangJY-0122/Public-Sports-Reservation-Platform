#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度测试赛事API接口
"""

import requests
import json

def test_events_advanced():
    """测试高级赛事API功能"""
    base_url = "http://127.0.0.1:5000"
    
    print("🏟️  高级赛事API测试")
    print("=" * 60)
    
    # 测试我的报名记录
    print("\n1. 测试我的报名记录 (GET /api/events/my-registrations)")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/events/my-registrations", timeout=5)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('message', '获取成功')}")
        else:
            print(f"❌ {response.text[:100]}")
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    # 测试赛事报名（模拟）
    print("\n2. 测试赛事报名接口 (POST /api/events/7/register)")
    print("-" * 40)
    try:
        # 尝试报名第7个赛事
        payload = {
            "user_name": "测试用户",
            "contact": "test@example.com"
        }
        response = requests.post(f"{base_url}/api/events/7/register", 
                               json=payload, timeout=5)
        print(f"报名状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('message', '报名成功')}")
        else:
            print(f"❌ 报名失败: {response.text[:100]}")
    except Exception as e:
        print(f"❌ 报名异常: {e}")
    
    # 测试赛事报名管理（需要管理员权限）
    print("\n3. 测试报名管理接口 (GET /api/events/7/registrations)")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/events/7/registrations", timeout=5)
        print(f"管理接口状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('message', '获取成功')}")
        else:
            print(f"❌ {response.text[:100]}")
    except Exception as e:
        print(f"❌ 异常: {e}")

    print("\n" + "=" * 60)
    print("🏁 高级赛事API测试完成")

if __name__ == "__main__":
    test_events_advanced()
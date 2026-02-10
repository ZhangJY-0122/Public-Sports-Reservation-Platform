#!/usr/bin/env python3
"""
前端联调测试脚本
"""
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_register():
    """测试用户注册"""
    print("\n=== 测试用户注册 ===")
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "123456",
        "phone": "13800138000",
        "city": "北京市",
        "real_name": "测试用户"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return True
    except Exception as e:
        print(f"注册测试失败: {e}")
        return False

def test_login():
    """测试用户登录"""
    print("\n=== 测试用户登录 ===")
    data = {
        "username": "testuser",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        if response.status_code == 200:
            return response.json().get('data')
        return None
    except Exception as e:
        print(f"登录测试失败: {e}")
        return None

def test_categories(user_data=None):
    """测试获取场馆分类"""
    print("\n=== 测试获取场馆分类 ===")
    
    headers = {}
    if user_data:
        token = user_data.get('token')
        if token:
            headers['Authorization'] = f'Bearer {token}'
    
    try:
        response = requests.get(f"{BASE_URL}/api/venue/categories", headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"分类测试失败: {e}")
        return False

def test_venues(user_data=None):
    """测试获取场馆列表"""
    print("\n=== 测试获取场馆列表 ===")
    
    headers = {}
    if user_data:
        token = user_data.get('token')
        if token:
            headers['Authorization'] = f'Bearer {token}'
    
    try:
        response = requests.get(f"{BASE_URL}/api/venue/list", headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"场馆列表测试失败: {e}")
        return False

def test_booking_create(user_data=None):
    """测试创建预约"""
    print("\n=== 测试创建预约 ===")
    
    headers = {}
    if user_data:
        token = user_data.get('token')
        if token:
            headers['Authorization'] = f'Bearer {token}'
    
    data = {
        "venue_id": 1,
        "booking_date": "2025-11-17",
        "start_time": "14:00",
        "end_time": "16:00"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/booking/create", json=data, headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"预约测试失败: {e}")
        return False

def main():
    """主测试流程"""
    print("🚀 开始前后端联调测试...")
    
    # 1. 测试注册
    test_register()
    
    # 2. 测试登录
    user_data = test_login()
    
    # 3. 测试分类
    test_categories(user_data)
    
    # 4. 测试场馆列表
    test_venues(user_data)
    
    # 5. 测试预约创建
    test_booking_create(user_data)
    
    print("\n✅ 前后端联调测试完成!")

if __name__ == "__main__":
    main()
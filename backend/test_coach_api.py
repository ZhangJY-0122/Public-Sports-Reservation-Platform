#!/usr/bin/env python3
"""
测试教练API的功能
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def test_create_coach():
    """测试创建教练"""
    print("🧪 测试创建教练接口...")
    
    url = f"{BASE_URL}/api/coaches/"
    
    data = {
        "name": "张伟教练",
        "specialization": "健身指导", 
        "hourly_rate": 200.0,
        "experience_years": 8,
        "introduction": "具有8年健身指导经验，擅长力量训练和体能提升",
        "phone": "13800138001"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📄 响应内容:")
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def test_update_coach(coach_id):
    """测试更新教练"""
    print(f"\n🧪 测试更新教练接口 (ID: {coach_id})...")
    
    url = f"{BASE_URL}/api/coaches/{coach_id}"
    
    data = {
        "name": "张伟教练（已更新）",
        "hourly_rate": 250.0,
        "experience_years": 10,
        "rating": 4.8
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.put(url, json=data, headers=headers)
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📄 响应内容:")
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def test_get_coach_list():
    """测试获取教练列表"""
    print(f"\n🧪 测试获取教练列表接口...")
    
    url = f"{BASE_URL}/api/coaches/list"
    
    try:
        response = requests.get(url)
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📄 响应内容:")
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def test_get_coach_detail(coach_id):
    """测试获取教练详情"""
    print(f"\n🧪 测试获取教练详情接口 (ID: {coach_id})...")
    
    url = f"{BASE_URL}/api/coaches/{coach_id}"
    
    try:
        response = requests.get(url)
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📄 响应内容:")
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def main():
    """主测试函数"""
    print("🚀 开始测试教练API功能...")
    print(f"📍 服务器地址: {BASE_URL}")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 测试获取列表（先看看数据库中是否已有教练）
    coaches_list = test_get_coach_list()
    
    if coaches_list and coaches_list.get('code') == 0:
        existing_coaches = coaches_list.get('data', {}).get('coaches', [])
        print(f"📊 数据库中已有 {len(existing_coaches)} 个教练")
        
        if existing_coaches:
            # 获取第一个教练ID用于测试
            test_coach_id = existing_coaches[0]['id']
            print(f"🎯 使用现有教练ID进行测试: {test_coach_id}")
            
            # 测试更新
            test_update_coach(test_coach_id)
            
            # 测试详情
            test_get_coach_detail(test_coach_id)
    
    # 测试创建新教练
    new_coach = test_create_coach()
    
    if new_coach and new_coach.get('code') == 0:
        coach_id = new_coach['data']['coach']['id']
        print(f"🎉 成功创建教练，ID: {coach_id}")
        
        # 测试更新新创建的教练
        test_update_coach(coach_id)
        
        # 测试详情
        test_get_coach_detail(coach_id)
        
        # 再次获取列表确认创建成功
        test_get_coach_list()
    
    print("\n" + "=" * 60)
    print("✅ 教练API测试完成！")

if __name__ == "__main__":
    main()
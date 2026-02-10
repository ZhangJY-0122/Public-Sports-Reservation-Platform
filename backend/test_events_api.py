#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试赛事API接口
"""

import requests
import json
from datetime import datetime

def test_events_api():
    """测试赛事相关API"""
    base_url = "http://127.0.0.1:5000"
    
    print("🏟️  赛事API测试报告")
    print("=" * 60)
    
    # 测试1: 赛事列表
    print("\n1. 测试赛事列表接口 (GET /api/events/list)")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/events/list", timeout=5)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"API状态: {'✅ 成功' if data.get('code') == 0 else '❌ 失败'}")
            
            if 'data' in data and 'events' in data['data']:
                events = data['data']['events']
                print(f"赛事总数: {len(events)} 个")
                
                if events:
                    print("\n📋 赛事详细信息:")
                    for i, event in enumerate(events, 1):
                        print(f"\n  [{i}] 赛事信息:")
                        print(f"      类型: {event.get('event_type', '未知')}")
                        print(f"      时间: {event.get('event_date', '未设置')}")
                        print(f"      描述: {event.get('description', '无描述')}")
                        print(f"      当前参与人数: {event.get('current_participants', 0)}")
                        print(f"      创建时间: {event.get('created_at', '')}")
                        
                        # 如果有event_id，显示详情链接
                        if 'id' in event:
                            print(f"      详情ID: {event['id']}")
                else:
                    print("📝 当前没有赛事数据")
            else:
                print("❌ 响应格式异常")
                print(f"原始响应: {data}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    # 测试2: 尝试获取单个赛事详情（如果有赛事的话）
    print("\n\n2. 测试赛事详情接口 (GET /api/events/<id>)")
    print("-" * 40)
    
    try:
        # 先获取赛事列表，获取第一个ID
        response = requests.get(f"{base_url}/api/events/list", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'events' in data['data'] and data['data']['events']:
                first_event_id = data['data']['events'][0].get('id')
                if first_event_id:
                    detail_response = requests.get(f"{base_url}/api/events/{first_event_id}", timeout=5)
                    print(f"赛事 {first_event_id} 详情状态码: {detail_response.status_code}")
                    
                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()
                        print("✅ 赛事详情获取成功")
                    else:
                        print(f"❌ 赛事详情获取失败: {detail_response.text}")
            else:
                print("📝 没有可用的赛事ID进行详情测试")
    except Exception as e:
        print(f"❌ 详情测试异常: {e}")

    print("\n" + "=" * 60)
    print("🏁 赛事API测试完成")

if __name__ == "__main__":
    test_events_api()
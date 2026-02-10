import requests
import json

print('=== 测试API接口 ===')

# 测试健康检查
try:
    response = requests.get('http://127.0.0.1:5000/health')
    print('\n1. 健康检查:', response.status_code)
    print('Response:', response.json())
except Exception as e:
    print(f'错误: {e}')

# 测试活动列表
try:
    response = requests.get('http://127.0.0.1:5000/api/activity/list')
    print('\n2. 活动列表:', response.status_code)
    if response.status_code == 200:
        data = response.json()
        total = data['data']['pagination']['total']
        print(f'活动数量: {total}')
    else:
        print('Response:', response.json())
except Exception as e:
    print(f'错误: {e}')

# 测试创建活动
try:
    activity_data = {
        'title': '测试活动',
        'description': '这是一个测试活动',
        'activity_type': 'training',
        'start_date': '2024-01-15',
        'end_date': '2024-01-15',
        'start_time': '14:00',
        'end_time': '16:00',
        'location': '测试场地',
        'max_participants': 20
    }
    response = requests.post('http://127.0.0.1:5000/api/activity', json=activity_data)
    print('\n3. 创建活动:', response.status_code)
    print('Response:', response.json())
except Exception as e:
    print(f'错误: {e}')

# 再次测试活动列表，查看是否添加成功
try:
    response = requests.get('http://127.0.0.1:5000/api/activity/list')
    print('\n4. 再次测试活动列表:', response.status_code)
    if response.status_code == 200:
        data = response.json()
        total = data['data']['pagination']['total']
        print(f'活动数量: {total}')
    else:
        print('Response:', response.json())
except Exception as e:
    print(f'错误: {e}')
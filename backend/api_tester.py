#!/usr/bin/env python
"""
API全面测试脚本
自动测试体育预约系统所有API接口
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# API基础URL
BASE_URL = "http://127.0.0.1:5000"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.test_user_id = None
        self.test_user_token = None
        self.admin_user_id = None
        self.test_results = []
    
    def log_test(self, test_name, status, message, response_data=None):
        """记录测试结果"""
        result = {
            'test': test_name,
            'status': status,  # 'PASS', 'FAIL', 'SKIP'
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'response_data': response_data
        }
        self.test_results.append(result)
        
        status_symbol = "✅" if status == 'PASS' else "❌" if status == 'FAIL' else "⏭️"
        print(f"{status_symbol} {test_name}: {message}")
        
        if response_data and status == 'FAIL':
            print(f"   响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
    
    def test_base_endpoints(self):
        """测试基础接口"""
        print("\n🔍 测试基础接口...")
        
        # 测试健康检查
        try:
            response = self.session.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_test("健康检查", 'PASS', "服务运行正常")
                else:
                    self.log_test("健康检查", 'FAIL', "健康状态异常", data)
            else:
                self.log_test("健康检查", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("健康检查", 'FAIL', f"连接失败: {str(e)}")
        
        # 测试首页
        try:
            response = self.session.get(f"{BASE_URL}/")
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'API服务' in data['message']:
                    self.log_test("首页接口", 'PASS', "API服务信息获取成功", data)
                else:
                    self.log_test("首页接口", 'FAIL', "响应格式异常", data)
            else:
                self.log_test("首页接口", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("首页接口", 'FAIL', f"连接失败: {str(e)}")
        
        # 测试系统信息
        try:
            response = self.session.get(f"{BASE_URL}/api/system/info")
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and 'system' in data.get('data', {}):
                    self.log_test("系统信息", 'PASS', "系统信息获取成功", data)
                else:
                    self.log_test("系统信息", 'FAIL', "响应格式异常", data)
            else:
                self.log_test("系统信息", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("系统信息", 'FAIL', f"连接失败: {str(e)}")
    
    def test_auth_endpoints(self):
        """测试认证接口"""
        print("\n🔐 测试认证接口...")
        
        # 测试用户注册
        try:
            user_data = {
                'username': f'test_user_{int(datetime.now().timestamp())}',
                'email': f'test{int(datetime.now().timestamp())}@example.com',
                'password': '123456',
                'phone': f'138{int(datetime.now().timestamp()) % 100000000:08d}',
                'city': '北京市',
                'real_name': '测试用户'
            }
            
            response = self.session.post(f"{BASE_URL}/api/auth/register", json=user_data)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and 'user_id' in data.get('data', {}):
                    self.test_user_id = data['data']['user_id']
                    self.log_test("用户注册", 'PASS', f"注册成功，用户ID: {self.test_user_id}")
                else:
                    self.log_test("用户注册", 'FAIL', "响应格式异常", data)
            else:
                self.log_test("用户注册", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("用户注册", 'FAIL', f"注册失败: {str(e)}")
        
        # 测试重复注册
        try:
            response = self.session.post(f"{BASE_URL}/api/auth/register", json=user_data)
            if response.status_code == 409:
                self.log_test("重复注册检查", 'PASS', "正确阻止重复注册")
            else:
                self.log_test("重复注册检查", 'FAIL', f"应该返回409状态码，实际: {response.status_code}")
        except Exception as e:
            self.log_test("重复注册检查", 'FAIL', f"测试失败: {str(e)}")
        
        # 测试用户登录
        try:
            login_data = {
                'username': user_data['username'],
                'password': user_data['password']
            }
            
            response = self.session.post(f"{BASE_URL}/api/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and 'user_id' in data.get('data', {}):
                    self.log_test("用户登录", 'PASS', f"登录成功")
                    
                    # 设置用户ID到请求头（模拟登录状态）
                    self.session.headers.update({'User-Id': str(data['data']['user_id'])})
                else:
                    self.log_test("用户登录", 'FAIL', "响应格式异常", data)
            else:
                self.log_test("用户登录", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("用户登录", 'FAIL', f"登录失败: {str(e)}")
        
        # 测试管理员登录
        try:
            admin_login_data = {
                'username': 'admin',
                'password': 'admin123'
            }
            
            response = self.session.post(f"{BASE_URL}/api/auth/login", json=admin_login_data)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    self.admin_user_id = data['data']['user_id']
                    self.log_test("管理员登录", 'PASS', f"管理员登录成功，ID: {self.admin_user_id}")
                else:
                    self.log_test("管理员登录", 'FAIL', "响应格式异常", data)
            else:
                self.log_test("管理员登录", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("管理员登录", 'FAIL', f"管理员登录失败: {str(e)}")
    
    def test_venue_endpoints(self):
        """测试场馆接口"""
        print("\n🏟️ 测试场馆接口...")
        
        # 获取场馆分类
        try:
            response = self.session.get(f"{BASE_URL}/api/venue/categories")
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and isinstance(data.get('data'), list):
                    self.log_test("获取场馆分类", 'PASS', f"获取到 {len(data['data'])} 个分类")
                else:
                    self.log_test("获取场馆分类", 'FAIL', "响应格式异常", data)
            else:
                self.log_test("获取场馆分类", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("获取场馆分类", 'FAIL', f"获取失败: {str(e)}")
        
        # 获取场馆列表
        try:
            response = self.session.get(f"{BASE_URL}/api/venue/list")
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and 'venues' in data.get('data', {}):
                    venue_count = len(data['data']['venues'])
                    self.log_test("获取场馆列表", 'PASS', f"获取到 {venue_count} 个场馆")
                else:
                    self.log_test("获取场馆列表", 'FAIL', "响应格式异常", data)
            else:
                self.log_test("获取场馆列表", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("获取场馆列表", 'FAIL', f"获取失败: {str(e)}")
        
        # 测试场馆搜索
        try:
            response = self.session.get(f"{BASE_URL}/api/venue/list?keyword=篮球")
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    self.log_test("场馆搜索", 'PASS', "搜索功能正常")
                else:
                    self.log_test("场馆搜索", 'FAIL', "响应格式异常", data)
            else:
                self.log_test("场馆搜索", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("场馆搜索", 'FAIL', f"搜索失败: {str(e)}")
    
    def test_user_endpoints(self):
        """测试用户接口"""
        print("\n👤 测试用户接口...")
        
        # 获取用户信息
        if self.test_user_id:
            try:
                response = self.session.get(f"{BASE_URL}/api/user/profile")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == 0 and isinstance(data.get('data'), dict):
                        self.log_test("获取用户信息", 'PASS', "用户信息获取成功")
                    else:
                        self.log_test("获取用户信息", 'FAIL', "响应格式异常", data)
                else:
                    self.log_test("获取用户信息", 'FAIL', f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_test("获取用户信息", 'FAIL', f"获取失败: {str(e)}")
        else:
            self.log_test("获取用户信息", 'SKIP', "无测试用户")
        
        # 获取用户仪表板
        if self.test_user_id:
            try:
                response = self.session.get(f"{BASE_URL}/api/user/dashboard")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == 0:
                        self.log_test("获取用户仪表板", 'PASS', "仪表板数据获取成功")
                    else:
                        self.log_test("获取用户仪表板", 'FAIL', "响应格式异常", data)
                else:
                    self.log_test("获取用户仪表板", 'FAIL', f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_test("获取用户仪表板", 'FAIL', f"获取失败: {str(e)}")
        else:
            self.log_test("获取用户仪表板", 'SKIP', "无测试用户")
        
        # 获取用户预约记录
        if self.test_user_id:
            try:
                response = self.session.get(f"{BASE_URL}/api/user/bookings")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == 0:
                        self.log_test("获取用户预约", 'PASS', "预约记录获取成功")
                    else:
                        self.log_test("获取用户预约", 'FAIL', "响应格式异常", data)
                else:
                    self.log_test("获取用户预约", 'FAIL', f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_test("获取用户预约", 'FAIL', f"获取失败: {str(e)}")
        else:
            self.log_test("获取用户预约", 'SKIP', "无测试用户")
    
    def test_booking_endpoints(self):
        """测试预约接口"""
        print("\n📅 测试预约接口...")
        
        if not self.test_user_id:
            self.log_test("创建预约", 'SKIP', "无测试用户")
            self.log_test("获取预约列表", 'SKIP', "无测试用户")
            return
        
        # 创建预约
        try:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            booking_data = {
                'venue_id': 1,
                'booking_date': tomorrow,
                'start_time': '14:00',
                'end_time': '16:00'
            }
            
            response = self.session.post(f"{BASE_URL}/api/booking/create", json=booking_data)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and isinstance(data.get('data'), dict):
                    self.log_test("创建预约", 'PASS', "预约创建成功")
                else:
                    self.log_test("创建预约", 'FAIL', "响应格式异常", data)
            else:
                self.log_test("创建预约", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("创建预约", 'FAIL', f"创建失败: {str(e)}")
        
        # 获取预约列表
        try:
            response = self.session.get(f"{BASE_URL}/api/booking/list")
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    self.log_test("获取预约列表", 'PASS', "预约列表获取成功")
                else:
                    self.log_test("获取预约列表", 'FAIL', "响应格式异常", data)
            else:
                self.log_test("获取预约列表", 'FAIL', f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("获取预约列表", 'FAIL', f"获取失败: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始API全面测试...")
        print(f"📍 测试地址: {BASE_URL}")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 依次测试各个模块
        self.test_base_endpoints()
        self.test_auth_endpoints()
        self.test_venue_endpoints()
        self.test_user_endpoints()
        self.test_booking_endpoints()
        
        # 统计结果
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        skipped = sum(1 for r in self.test_results if r['status'] == 'SKIP')
        total = len(self.test_results)
        
        print("\n" + "=" * 60)
        print("📊 测试结果统计:")
        print(f"   总计: {total}")
        print(f"   ✅ 通过: {passed}")
        print(f"   ❌ 失败: {failed}")
        print(f"   ⏭️  跳过: {skipped}")
        print(f"   成功率: {passed/total*100:.1f}%")
        
        # 保存详细结果
        with open('api_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        print(f"📄 详细结果已保存到: api_test_results.json")
        
        return failed == 0

if __name__ == '__main__':
    tester = APITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
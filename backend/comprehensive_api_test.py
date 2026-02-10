#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
体育预约系统 - 全面API接口测试脚本
测试所有可用的API端点
"""

import requests
import json
import time
from datetime import datetime

# API基础配置
BASE_URL = "http://127.0.0.1:5000"
API_PREFIX = f"{BASE_URL}/api"

# 测试配置
TEST_TIMEOUT = 10
SUCCESS_STATUS_CODES = [200, 201]

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.api_prefix = API_PREFIX
        self.session = requests.Session()
        self.session.timeout = TEST_TIMEOUT
        self.test_results = []
        self.auth_token = None
        self.user_id = None
        
    def log_test(self, endpoint, method, status_code, response_time, success, details=""):
        """记录测试结果"""
        result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'endpoint': endpoint,
            'method': method,
            'status_code': status_code,
            'response_time_ms': round(response_time * 1000, 2),
            'success': success,
            'details': details
        }
        self.test_results.append(result)
        
        # 控制台输出
        status_symbol = "✅" if success else "❌"
        print(f"{status_symbol} {method} {endpoint} - {status_code} ({response_time:.3f}s)")
        if details:
            print(f"   详情: {details}")
        print()
    
    def make_request(self, method, endpoint, **kwargs):
        """发起HTTP请求"""
        url = f"{self.api_prefix}{endpoint}"
        if method.upper() == 'GET':
            response = self.session.get(url, **kwargs)
        elif method.upper() == 'POST':
            response = self.session.post(url, **kwargs)
        elif method.upper() == 'PUT':
            response = self.session.put(url, **kwargs)
        elif method.upper() == 'DELETE':
            response = self.session.delete(url, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return response
    
    def test_basic_endpoints(self):
        """测试基础端点"""
        print("🔍 测试基础端点...")
        
        # 根路径
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/")
            response_time = time.time() - start_time
            success = response.status_code in SUCCESS_STATUS_CODES
            details = response.json().get('message', '') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
            self.log_test('/', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/', 'GET', None, 0, False, f"请求异常: {str(e)}")
        
        # 健康检查
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/health")
            response_time = time.time() - start_time
            success = response.status_code in SUCCESS_STATUS_CODES
            details = response.json().get('message', '') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
            self.log_test('/health', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/health', 'GET', None, 0, False, f"请求异常: {str(e)}")
        
        # 系统信息
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/system/info")
            response_time = time.time() - start_time
            success = response.status_code in SUCCESS_STATUS_CODES
            data = response.json().get('data', {}) if response.headers.get('content-type', '').startswith('application/json') else {}
            details = f"API版本: {data.get('api', {}).get('version', 'N/A')}"
            self.log_test('/api/system/info', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/api/system/info', 'GET', None, 0, False, f"请求异常: {str(e)}")
    
    def test_auth_endpoints(self):
        """测试认证端点"""
        print("🔐 测试认证端点...")
        
        # 用户注册
        register_data = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test{int(time.time())}@example.com",
            "password": "123456",
            "phone": f"138{int(time.time()) % 100000000:08d}",
            "city": "北京市",
            "real_name": "测试用户"
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.api_prefix}/auth/register",
                json=register_data,
                headers={'Content-Type': 'application/json'}
            )
            response_time = time.time() - start_time
            
            if response.status_code in SUCCESS_STATUS_CODES:
                self.user_id = response.json().get('data', {}).get('user_id')
                details = f"用户ID: {self.user_id}"
            else:
                details = response.json().get('message', '未知错误') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
            
            success = response.status_code in SUCCESS_STATUS_CODES
            self.log_test('/auth/register', 'POST', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/auth/register', 'POST', None, 0, False, f"请求异常: {str(e)}")
        
        # 用户登录
        if self.user_id:  # 只有注册成功才测试登录
            login_data = {
                "username": register_data["username"],
                "password": register_data["password"]
            }
            
            try:
                start_time = time.time()
                response = self.session.post(
                    f"{self.api_prefix}/auth/login",
                    json=login_data,
                    headers={'Content-Type': 'application/json'}
                )
                response_time = time.time() - start_time
                
                if response.status_code in SUCCESS_STATUS_CODES:
                    login_result = response.json().get('data', {})
                    self.auth_token = login_result.get('token')
                    details = "登录成功，获取token"
                else:
                    details = response.json().get('message', '未知错误') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
                
                success = response.status_code in SUCCESS_STATUS_CODES
                self.log_test('/auth/login', 'POST', response.status_code, response_time, success, details)
            except Exception as e:
                self.log_test('/auth/login', 'POST', None, 0, False, f"请求异常: {str(e)}")
    
    def test_venue_endpoints(self):
        """测试场馆管理端点"""
        print("🏟️ 测试场馆管理端点...")
        
        # 场馆分类
        try:
            start_time = time.time()
            response = self.session.get(f"{self.api_prefix}/venue/categories")
            response_time = time.time() - start_time
            
            if response.status_code in SUCCESS_STATUS_CODES:
                categories = response.json().get('data', [])
                details = f"获取到 {len(categories)} 个分类"
            else:
                details = response.json().get('message', '未知错误') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
            
            success = response.status_code in SUCCESS_STATUS_CODES
            self.log_test('/venue/categories', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/venue/categories', 'GET', None, 0, False, f"请求异常: {str(e)}")
        
        # 场馆列表
        try:
            start_time = time.time()
            response = self.session.get(f"{self.api_prefix}/venue/list?page=1&page_size=10")
            response_time = time.time() - start_time
            
            if response.status_code in SUCCESS_STATUS_CODES:
                venues = response.json().get('data', {}).get('venues', [])
                details = f"获取到 {len(venues)} 个场馆"
            else:
                details = response.json().get('message', '未知错误') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
            
            success = response.status_code in SUCCESS_STATUS_CODES
            self.log_test('/venue/list', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/venue/list', 'GET', None, 0, False, f"请求异常: {str(e)}")
        
        # 场馆搜索
        try:
            start_time = time.time()
            response = self.session.get(f"{self.api_prefix}/venue/search?keyword=篮球")
            response_time = time.time() - start_time
            
            if response.status_code in SUCCESS_STATUS_CODES:
                venues = response.json().get('data', [])
                details = f"搜索到 {len(venues)} 个相关场馆"
            else:
                details = response.json().get('message', '未知错误') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
            
            success = response.status_code in SUCCESS_STATUS_CODES
            self.log_test('/venue/search?keyword=篮球', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/venue/search?keyword=篮球', 'GET', None, 0, False, f"请求异常: {str(e)}")
    
    def test_booking_endpoints(self):
        """测试预约管理端点"""
        print("📅 测试预约管理端点...")
        
        # 创建预约（需要用户认证）
        headers = {'Content-Type': 'application/json'}
        if self.user_id:
            headers['User-Id'] = str(self.user_id)
        
        booking_data = {
            "venue_id": 1,
            "booking_date": (datetime.now().date().isoformat()),
            "start_time": "10:00",
            "end_time": "12:00"
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.api_prefix}/booking/create",
                json=booking_data,
                headers=headers
            )
            response_time = time.time() - start_time
            
            if response.status_code in SUCCESS_STATUS_CODES:
                booking_id = response.json().get('data', {}).get('id')
                details = f"预约ID: {booking_id}"
            else:
                details = response.json().get('message', '未知错误') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
            
            success = response.status_code in SUCCESS_STATUS_CODES
            self.log_test('/booking/create', 'POST', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/booking/create', 'POST', None, 0, False, f"请求异常: {str(e)}")
        
        # 获取预约列表
        try:
            start_time = time.time()
            response = self.session.get(
                f"{self.api_prefix}/booking/list",
                headers=headers
            )
            response_time = time.time() - start_time
            
            if response.status_code in SUCCESS_STATUS_CODES:
                bookings = response.json().get('data', {})
                details = "获取预约列表"
            else:
                details = response.json().get('message', '未知错误') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
            
            success = response.status_code in SUCCESS_STATUS_CODES
            self.log_test('/booking/list', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/booking/list', 'GET', None, 0, False, f"请求异常: {str(e)}")
    
    def test_user_endpoints(self):
        """测试用户中心端点"""
        print("👤 测试用户中心端点...")
        
        headers = {'Content-Type': 'application/json'}
        if self.user_id:
            headers['User-Id'] = str(self.user_id)
        
        # 获取用户资料
        try:
            start_time = time.time()
            response = self.session.get(
                f"{self.api_prefix}/user/profile",
                headers=headers
            )
            response_time = time.time() - start_time
            
            if response.status_code in SUCCESS_STATUS_CODES:
                user_data = response.json().get('data', {})
                details = f"用户名: {user_data.get('username', 'N/A')}"
            else:
                details = response.json().get('message', '未知错误') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
            
            success = response.status_code in SUCCESS_STATUS_CODES
            self.log_test('/user/profile', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/user/profile', 'GET', None, 0, False, f"请求异常: {str(e)}")
        
        # 获取用户仪表板
        try:
            start_time = time.time()
            response = self.session.get(
                f"{self.api_prefix}/user/dashboard",
                headers=headers
            )
            response_time = time.time() - start_time
            
            if response.status_code in SUCCESS_STATUS_CODES:
                details = "获取用户仪表板数据"
            else:
                details = response.json().get('message', '未知错误') if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]
            
            success = response.status_code in SUCCESS_STATUS_CODES
            self.log_test('/user/dashboard', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/user/dashboard', 'GET', None, 0, False, f"请求异常: {str(e)}")
    
    def test_swagger_docs(self):
        """测试API文档"""
        print("📚 测试API文档...")
        
        # Swagger JSON
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/swagger.json")
            response_time = time.time() - start_time
            
            if response.status_code in SUCCESS_STATUS_CODES:
                swagger_data = response.json()
                paths = swagger_data.get('paths', {})
                details = f"API文档，包含 {len(paths)} 个接口"
            else:
                details = response.text[:100]
            
            success = response.status_code in SUCCESS_STATUS_CODES
            self.log_test('/api/swagger.json', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/api/swagger.json', 'GET', None, 0, False, f"请求异常: {str(e)}")
        
        # Swagger UI
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/docs/")
            response_time = time.time() - start_time
            
            if response.status_code in SUCCESS_STATUS_CODES:
                details = "Swagger UI 页面可访问"
            else:
                details = f"状态码: {response.status_code}"
            
            success = response.status_code in SUCCESS_STATUS_CODES
            self.log_test('/api/docs/', 'GET', response.status_code, response_time, success, details)
        except Exception as e:
            self.log_test('/api/docs/', 'GET', None, 0, False, f"请求异常: {str(e)}")
    
    def run_comprehensive_test(self):
        """运行全面测试"""
        print("🚀 开始全面API接口测试...")
        print(f"测试地址: {self.base_url}")
        print("=" * 60)
        
        # 等待服务启动
        print("⏳ 检查服务状态...")
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ 服务运行正常")
            else:
                print("⚠️  服务状态异常")
        except Exception as e:
            print(f"❌ 无法连接到服务: {str(e)}")
            return
        
        print("=" * 60)
        
        # 执行各项测试
        self.test_basic_endpoints()
        self.test_auth_endpoints()
        self.test_venue_endpoints()
        self.test_booking_endpoints()
        self.test_user_endpoints()
        self.test_swagger_docs()
        
        # 生成测试报告
        self.generate_test_report()
    
    def generate_test_report(self):
        """生成测试报告"""
        print("=" * 60)
        print("📊 测试报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - successful_tests
        
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"总测试数: {total_tests}")
        print(f"成功: {successful_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"成功率: {success_rate:.1f}%")
        print()
        
        # 平均响应时间
        response_times = [result['response_time_ms'] for result in self.test_results if result['success']]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"平均响应时间: {avg_response_time:.2f}ms")
        print()
        
        # 失败的测试
        if failed_tests > 0:
            print("❌ 失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['method']} {result['endpoint']} - {result['status_code']}")
                    print(f"    {result['details']}")
            print()
        
        # 保存详细报告
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"api_test_report_{timestamp}.json"
        
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2)
            print(f"📁 详细测试报告已保存到: {report_filename}")
        except Exception as e:
            print(f"❌ 保存报告失败: {str(e)}")

if __name__ == "__main__":
    tester = APITester()
    tester.run_comprehensive_test()
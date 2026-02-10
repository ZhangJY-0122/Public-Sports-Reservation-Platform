#!/usr/bin/env python3
"""
体育预约系统API综合测试脚本
测试所有核心API接口的功能
"""

import requests
import json
import time
from datetime import datetime

# API基础URL
BASE_URL = "http://127.0.0.1:5000"

# 测试用的认证Token（登录后获取）
auth_token = None

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.results = []
    
    def log_test(self, test_name, success, response=None, error=None):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'response': response,
            'error': str(error) if error else None
        }
        self.results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if error:
            print(f"    错误: {error}")
        if response and not success:
            print(f"    响应: {response}")
    
    def make_request(self, method, endpoint, data=None, headers=None):
        """发起HTTP请求"""
        url = f"{BASE_URL}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            # 尝试解析JSON响应
            try:
                json_response = response.json()
                return response.status_code, json_response
            except json.JSONDecodeError:
                return response.status_code, response.text
                
        except Exception as e:
            return None, str(e)
    
    def test_health_check(self):
        """测试健康检查接口"""
        status_code, response = self.make_request('GET', '/health')
        
        success = (
            status_code == 200 and 
            isinstance(response, dict) and 
            response.get('status') == 'healthy'
        )
        
        self.log_test("健康检查", success, response)
        return success
    
    def test_system_info(self):
        """测试系统信息接口"""
        status_code, response = self.make_request('GET', '/api/system/info')
        
        success = (
            status_code == 200 and 
            isinstance(response, dict) and 
            response.get('code') == 0
        )
        
        self.log_test("系统信息", success, response)
        return success
    
    def test_index(self):
        """测试首页接口"""
        status_code, response = self.make_request('GET', '/')
        
        success = (
            status_code == 200 and 
            isinstance(response, dict) and 
            'message' in response
        )
        
        self.log_test("首页接口", success, response)
        return success
    
    def test_user_login(self):
        """测试用户登录"""
        # 使用预置的管理员账户
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        status_code, response = self.make_request('POST', '/api/auth/login', data=login_data)
        
        global auth_token
        success = (
            status_code == 200 and 
            isinstance(response, dict) and 
            response.get('code') == 0 and
            'token' in response.get('data', {})
        )
        
        if success:
            auth_token = response['data']['token']
            self.session.headers.update({
                'Authorization': f'Bearer {auth_token}'
            })
        
        self.log_test("用户登录", success, response)
        return success
    
    def test_user_profile(self):
        """测试获取用户信息"""
        if not auth_token:
            self.log_test("用户信息", False, None, "未获取到认证令牌")
            return False
        
        status_code, response = self.make_request('GET', '/api/user/profile')
        
        success = (
            status_code == 200 and 
            isinstance(response, dict) and 
            response.get('code') == 0
        )
        
        self.log_test("用户信息", success, response)
        return success
    
    def test_venue_list(self):
        """测试获取场馆列表"""
        status_code, response = self.make_request('GET', '/api/venue/list')
        
        success = (
            status_code == 200 and 
            isinstance(response, dict) and 
            response.get('code') == 0
        )
        
        self.log_test("场馆列表", success, response)
        return success
    
    def test_venue_categories(self):
        """测试获取场馆分类"""
        status_code, response = self.make_request('GET', '/api/venue/categories')
        
        success = (
            status_code == 200 and 
            isinstance(response, dict) and 
            response.get('code') == 0
        )
        
        self.log_test("场馆分类", success, response)
        return success
    
    def test_activity_list(self):
        """测试获取活动列表"""
        status_code, response = self.make_request('GET', '/api/activity/list')
        
        success = (
            status_code == 200 and 
            isinstance(response, dict) and 
            response.get('code') == 0
        )
        
        self.log_test("活动列表", success, response)
        return success
    
    def test_coach_list(self):
        """测试获取教练列表"""
        status_code, response = self.make_request('GET', '/api/coach/list')
        
        success = (
            status_code == 200 and 
            isinstance(response, dict) and 
            response.get('code') == 0
        )
        
        self.log_test("教练列表", success, response)
        return success
    
    def test_api_docs(self):
        """测试API文档访问"""
        status_code, response = self.make_request('GET', '/api/docs/')
        
        success = status_code == 200
        
        self.log_test("API文档", success, response)
        return success
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始体育预约系统API综合测试")
        print("=" * 50)
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"API地址: {BASE_URL}")
        print("=" * 50)
        
        # 基础接口测试
        print("\n📋 基础接口测试:")
        self.test_health_check()
        self.test_system_info()
        self.test_index()
        self.test_api_docs()
        
        # 认证接口测试
        print("\n🔐 认证接口测试:")
        login_success = self.test_user_login()
        
        if login_success:
            print("\n👤 用户相关测试:")
            self.test_user_profile()
        
        # 数据接口测试
        print("\n📊 数据接口测试:")
        self.test_venue_categories()
        self.test_venue_list()
        self.test_activity_list()
        self.test_coach_list()
        
        # 输出测试结果统计
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 50)
        print("📊 测试结果摘要")
        print("=" * 50)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"成功率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ 失败的测试:")
            for result in self.results:
                if not result['success']:
                    print(f"  - {result['test_name']}: {result['error']}")
        
        # 保存详细结果到文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'api_test_report_{timestamp}.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细报告已保存到: {report_file}")

def main():
    """主函数"""
    try:
        tester = APITester()
        tester.run_all_tests()
        
        print("\n🎉 API测试完成！")
        
    except KeyboardInterrupt:
        print("\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n💥 测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
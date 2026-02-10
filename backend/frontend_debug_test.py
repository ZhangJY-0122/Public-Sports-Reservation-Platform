#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前后端联调测试脚本
测试uni-app登录页面与后端API的连接
"""

import requests
import json
import time
from datetime import datetime

class BackendTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_connection(self):
        """测试后端服务连接"""
        try:
            self.log("🔗 测试后端连接...")
            response = requests.get(f"{self.base_url}/", timeout=5)
            self.log(f"✅ 后端连接成功 (状态码: {response.status_code})")
            return True
        except requests.exceptions.RequestException as e:
            self.log(f"❌ 后端连接失败: {e}", "ERROR")
            return False
    
    def test_login_api(self, username="testuser", password="123456"):
        """测试登录API"""
        try:
            self.log(f"🔐 测试用户登录: {username}")
            
            # 准备请求数据
            login_data = {
                "username": username,
                "password": password
            }
            
            # 发送请求
            self.log("📤 发送登录请求...")
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                headers=self.headers,
                json=login_data,
                timeout=10
            )
            
            self.log(f"📊 响应状态码: {response.status_code}")
            
            # 解析响应
            try:
                data = response.json()
                self.log(f"📦 响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
                
                if response.status_code == 200:
                    if data.get('code') == 0:
                        self.log("✅ 登录成功!", "SUCCESS")
                        token = data.get('data', {}).get('token')
                        user = data.get('data', {}).get('user')
                        if token:
                            self.log(f"🎫 Token: {token[:20]}...")
                        if user:
                            self.log(f"👤 用户信息: {user}")
                        return True, data
                    else:
                        self.log(f"❌ 登录失败: {data.get('message', '未知错误')}", "ERROR")
                        return False, data
                else:
                    self.log(f"❌ HTTP错误: {response.status_code}", "ERROR")
                    return False, data
                    
            except json.JSONDecodeError:
                self.log(f"❌ 响应格式错误: {response.text}", "ERROR")
                return False, None
                
        except requests.exceptions.RequestException as e:
            self.log(f"❌ 请求失败: {e}", "ERROR")
            return False, None
    
    def test_venue_categories(self):
        """测试场馆分类API"""
        try:
            self.log("🏢 测试场馆分类API...")
            response = requests.get(f"{self.base_url}/api/venue/categories", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"📦 场馆分类数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
                self.log("✅ 场馆分类API测试成功", "SUCCESS")
                return True
            else:
                self.log(f"❌ 场馆分类API失败: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ 场馆分类API异常: {e}", "ERROR")
            return False
    
    def test_venue_list(self):
        """测试场馆列表API"""
        try:
            self.log("📋 测试场馆列表API...")
            response = requests.get(f"{self.base_url}/api/venue/list", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"📦 场馆列表数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
                self.log("✅ 场馆列表API测试成功", "SUCCESS")
                return True
            else:
                self.log(f"❌ 场馆列表API失败: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ 场馆列表API异常: {e}", "ERROR")
            return False
    
    def run_full_test(self):
        """运行完整测试"""
        self.log("🚀 开始前后端联调测试", "HEADER")
        print("=" * 60)
        
        # 测试连接
        if not self.test_connection():
            self.log("❌ 无法连接到后端服务，测试终止", "ERROR")
            return False
        
        # 测试登录
        print("\n" + "=" * 40)
        login_success, login_data = self.test_login_api()
        
        # 测试场馆API
        print("\n" + "=" * 40)
        venue_cat_success = self.test_venue_categories()
        
        print("\n" + "=" * 40)
        venue_list_success = self.test_venue_list()
        
        # 总结
        print("\n" + "=" * 60)
        self.log("📊 测试总结", "SUMMARY")
        self.log(f"后端连接: {'✅ 成功' if True else '❌ 失败'}")
        self.log(f"用户登录: {'✅ 成功' if login_success else '❌ 失败'}")
        self.log(f"场馆分类: {'✅ 成功' if venue_cat_success else '❌ 失败'}")
        self.log(f"场馆列表: {'✅ 成功' if venue_list_success else '❌ 失败'}")
        
        overall_success = login_success and venue_cat_success and venue_list_success
        self.log(f"🎯 整体测试结果: {'✅ 成功' if overall_success else '❌ 失败'}", "RESULT")
        
        if overall_success:
            self.log("🎉 前后端联调测试通过！现在可以在浏览器中测试uni-app登录页面", "SUCCESS")
            self.log("🌐 浏览器访问地址: http://localhost:8080/uni_login_test.html")
        else:
            self.log("❌ 部分测试失败，请检查后端服务或API实现", "ERROR")
        
        return overall_success

def main():
    print("🎯 前后端联调测试工具")
    print("测试环境: uni-app登录页面 vs Flask后端API")
    print("=" * 60)
    
    tester = BackendTester()
    tester.run_full_test()

if __name__ == "__main__":
    main()
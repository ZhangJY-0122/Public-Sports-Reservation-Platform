#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的测试服务器
"""

from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'code': 0,
        'message': '体育预约系统API服务',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': '服务正常运行'
    })

@app.route('/api/test')
def test():
    return jsonify({
        'code': 0,
        'data': {
            'message': 'API测试成功',
            'time': '2025-11-16 18:05:00'
        },
        'message': '测试成功'
    })

if __name__ == '__main__':
    print("🏃 简化测试服务器启动")
    print("📡 访问地址: http://127.0.0.1:5000")
    print("🔗 健康检查: http://127.0.0.1:5000/health")
    print("🧪 API测试: http://127.0.0.1:5000/api/test")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False
    )
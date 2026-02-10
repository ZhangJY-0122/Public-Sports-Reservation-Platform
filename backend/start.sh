#!/bin/bash

# 体育预约系统启动脚本
# 适用于Linux/macOS系统

echo "🏃 体育预约系统 - 快速启动脚本"
echo "================================"

# 检查Python版本
python_version=$(python3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "✅ Python版本: $python_version"
else
    echo "❌ 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到pip3，请先安装pip"
    exit 1
fi
echo "✅ pip可用"

# 进入后端目录
cd "$(dirname "$0")"
backend_dir=$(pwd)
echo "📁 后端目录: $backend_dir"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "🔧 创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖包..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖包安装失败"
    exit 1
fi
echo "✅ 依赖包安装完成"

# 初始化数据库
echo "🗄️  初始化数据库..."
python run.py init-db --with-sample

if [ $? -ne 0 ]; then
    echo "❌ 数据库初始化失败"
    exit 1
fi

# 检查配置
echo "⚙️  检查配置..."
python run.py config-check

echo ""
echo "🚀 启动服务..."
echo "📚 API文档: http://localhost:5000/api/docs/"
echo "💡 健康检查: http://localhost:5000/health"
echo "================================"
echo "按 Ctrl+C 停止服务"
echo ""

# 启动服务
python run.py run --host=0.0.0.0 --port=5000 --debug
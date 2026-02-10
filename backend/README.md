# 体育预约系统 - 后端API

基于Flask框架开发的体育场馆预约系统后端API，支持MySQL/SQLite数据库切换。

## 项目结构

```
backend/
├── app.py                 # Flask应用主入口
├── config.py              # 配置文件
├── models.py              # 数据模型
├── migrate.py             # 数据库迁移模块
├── run.py                 # 启动脚本
├── requirements.txt       # Python依赖
├── .env.example          # 环境变量示例
├── start.sh              # 快速启动脚本（Linux/macOS）
├── routes/               # API路由模块
│   ├── auth.py           # 用户认证
│   ├── venue.py          # 场馆管理
│   ├── booking.py        # 预约管理
│   └── user.py           # 用户中心
└── tests/                # 测试文件
    └── test_api.py       # API测试
```

## 功能特性

### 🔐 用户认证
- 用户注册
- 用户登录
- 用户信息管理
- 基于请求头的身份识别

### 🏟️ 场馆管理
- 场馆分类管理
- 场馆列表查询（支持分页、筛选）
- 场馆详情获取
- 热门场馆推荐
- 场馆可用时间检查

### 📅 预约管理
- 创建预约
- 预约列表查询
- 预约状态管理
- 预约统计信息

### 👤 用户中心
- 用户资料管理
- 用户仪表板
- 我的赛事活动
- 用户统计数据

## 技术架构

- **框架**: Flask 2.3.3
- **数据库**: SQLAlchemy ORM + MySQL/SQLite
- **API文档**: Flask-RESTX (Swagger)
- **跨域**: Flask-CORS
- **认证**: 基于请求头的身份识别（无JWT）
- **分页**: 统一分页处理
- **联表查询**: SQLAlchemy关系查询

## 快速开始

### 1. 环境要求
- Python 3.7+
- MySQL 5.7+ 或 SQLite

### 2. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境
```bash
# 复制环境变量文件
cp .env.example .env

# 编辑配置文件
# DATABASE_TYPE=sqlite  # 或 mysql
# DATABASE_URL=sqlite:///sports_booking.db
```

### 4. 初始化数据库
```bash
# 初始化数据库（包含示例数据）
python run.py init-db --with-sample

# 或者重置数据库
python run.py reset-db
```

### 5. 启动服务
```bash
# 开发环境启动
python run.py run --debug

# 使用启动脚本（Linux/macOS）
./start.sh

# 或直接运行
python run.py run --host=0.0.0.0 --port=5000 --debug
```

### 6. 访问服务
- **API服务**: http://localhost:5000/
- **API文档**: http://localhost:5000/api/docs/
- **健康检查**: http://localhost:5000/health

## API使用说明

### 统一返回格式
```json
{
  "code": 0,
  "data": [...],
  "message": "操作成功"
}
```

### 身份识别
所有API通过请求头识别用户身份：
```
X-User-ID: 用户ID
X-User-Role: 用户角色
```

### 错误码说明
- `200`: 成功
- `400`: 请求参数错误
- `401`: 未授权访问
- `403`: 禁止访问
- `404`: 资源不存在
- `409`: 资源已存在（冲突）
- `500`: 服务器内部错误

## 常用命令

```bash
# 查看数据库状态
python run.py db-status

# 检查配置
python run.py config-check

# 运行测试
python run.py test --verbose

# 启动服务（自定义配置）
python run.py run --host=127.0.0.1 --port=8080 --debug --env=development
```

## 数据库设计

### 主要数据表
- `users`: 用户信息
- `venue_categories`: 场馆分类
- `venues`: 场馆信息
- `bookings`: 预约记录
- `activities`: 活动信息
- `friendships`: 好友关系
- `events`: 赛事信息
- `coaches`: 教练信息
- `coach_bookings`: 教练预约

### 数据关系
- 用户 ←→ 预约（一对多）
- 场馆分类 ←→ 场馆（一对多）
- 场馆 ←→ 预约（一对多）
- 用户 ←→ 好友关系（多对多）

## 开发指南

### 添加新的API接口
1. 在 `routes/` 目录下创建或编辑路由文件
2. 使用蓝图注册路由
3. 添加Swagger文档注释
4. 遵循统一返回格式

### 数据库变更
1. 修改 `models.py` 中的模型定义
2. 运行 `python run.py reset-db` 重新创建数据库
3. 或使用SQLite浏览器手动编辑数据库

### 环境配置
- 开发环境: `FLASK_ENV=development`
- 生产环境: `FLASK_ENV=production`
- 数据库切换: `DATABASE_TYPE=mysql` 或 `sqlite`

## 部署说明

### 开发环境
```bash
python run.py run --debug
```

### 生产环境
```bash
# 设置生产环境变量
export FLASK_ENV=production
export DATABASE_TYPE=mysql
export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/sports_booking"

# 使用Gunicorn部署
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker部署（可选）
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py", "run", "--host=0.0.0.0"]
```

## 注意事项

1. **安全**: 生产环境请修改默认密钥和数据库密码
2. **备份**: 定期备份数据库数据
3. **监控**: 建议添加日志监控和性能监控
4. **扩展**: 可根据需要添加Redis缓存、消息队列等

## 技术支持

如有问题，请检查：
1. Python版本是否符合要求
2. 依赖包是否正确安装
3. 数据库连接配置是否正确
4. 防火墙是否允许端口访问

---

**版本**: 1.0.0  
**更新时间**: 2025年1月  
**开发者**: AI Assistant
# CoachBooking 功能和API修改说明

## 修改概述

根据需求，对 CoachBooking 模型和相关的 API 接口进行了重要更新，主要包括添加场馆支持和改进预约流程。

## 主要修改

### 1. 数据库模型修改 (`backend/models.py`)

#### CoachBooking 模型更新
- **添加外键**: 新增 `venue_id` 字段，关联到 `venues` 表
- **添加关系**: 新增与 `Venue` 模型的关系定义
- **更新 to_dict**: 在返回数据中包含场馆信息 (`venue_id`, `venue_name`)

#### 具体修改
```python
# 新增外键字段
venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False, comment='场馆ID')

# 新增关系
venue = db.relationship('Venue', backref='coach_bookings')

# 更新 to_dict 方法
'venue_id': self.venue_id,
'venue_name': self.venue.name if self.venue else '',
```

### 2. API 接口修改 (`backend/routes/coaches.py`)

#### book_coach 方法重写
- **新增必填参数**: `venue_id` 成为预约的必需参数
- **场馆验证**: 添加场馆存在性验证
- **双重冲突检查**: 
  - 检查场馆在指定时段是否可用
  - 检查教练在指定时段是否可用
- **价格计算优化**: 包含场馆费用（教练基础价格 + 场馆每小时费用）
- **预约编号改进**: 在编号中包含场馆ID信息

#### 主要功能改进
1. **参数验证**: 要求 `venue_id` 为正整数且对应场馆存在
2. **价格策略**: `总价格 = (教练基础价格 + 场馆价格) × 预约时长`
3. **简化流程**: **移除了时间段冲突检查** - 允许多人同时预约同一时段
4. **错误处理**: 更精确的错误信息，区分场馆和教练冲突

#### 请求示例
```json
{
  "venue_id": 1,
  "date": "2025-12-01",
  "start_time": "09:00",
  "end_time": "10:00",
  "description": "篮球训练"
}
```

#### 响应数据
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "booking_no": "CB202511181430001001001",
    "coach_name": "张三",
    "venue_name": "体育馆A",
    "venue_id": 1,
    "date": "2025-12-01",
    "time": "09:00-10:00",
    "duration": "1.0小时",
    "price": "200.00",
    "status": "upcoming",
    "description": "篮球训练"
  },
  "message": "教练预约成功"
}
```

## 重要变更说明

### ⚡ 简化预约流程
- **移除冲突检查**: 预约不再检查时间段冲突，允许：
  - 多个用户同时预约同一教练的同一时段
  - 多个用户同时使用同一场馆的同一时段
- **优先下单**: 只要参数正确就能成功下单，无需考虑资源冲突
- **适合场景**: 适合演示、教学或低并发场景使用

## 向后兼容性

⚠️ **重要**: 此修改为破坏性更新，原有 API 需要 `venue_id` 参数才能正常工作。

## 数据库迁移

由于添加了新的外键约束，可能需要执行数据库迁移：

```bash
# 如果使用 Flask-Migrate
flask db upgrade

# 或手动执行 SQL
ALTER TABLE coach_bookings ADD COLUMN venue_id INT NOT NULL REFERENCES venues(id);
```

## 测试建议

1. **正常预约流程测试**: 验证包含 venue_id 的预约
2. **冲突检测测试**: 测试场馆和教练的时间冲突
3. **价格计算测试**: 验证场馆费用是否正确计算
4. **错误处理测试**: 测试无效 venue_id 的处理

## 修改文件清单

- ✅ `backend/models.py` - CoachBooking 模型和关系
- ✅ `backend/routes/coaches.py` - book_coach API 方法重写
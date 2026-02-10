# 体育预约系统 - 完整API接口文档

## 概述

本文档描述了体育预约系统后端API接口的详细信息。所有接口的基地址为：`http://127.0.0.1:5000/api`

## 系统功能特点

✅ **用户管理** - 用户注册、登录、个人信息管理  
✅ **场馆管理** - 场馆分类、搜索、详情、评价系统  
✅ **教练管理** - 教练信息、预约服务、专业领域  
✅ **预约系统** - 场地预约、分享预约、费用分摊  
✅ **赛事系统** - 赛事列表、报名、管理、统计  
✅ **活动管理** - 活动创建、参与、社交功能  
✅ **好友系统** - 用户社交、好友管理  

## 通用响应格式

所有API响应均采用以下统一格式：

```json
{
    "code": 0,
    "data": {},
    "message": "success"
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| code | integer | 状态码，0表示成功，其他值表示错误 |
| data | object | 响应数据 |
| message | string | 响应消息 |

### HTTP状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权，需要登录 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 409 | 资源冲突（如用户名已存在） |
| 500 | 服务器内部错误 |

## 认证说明

需要认证的接口需要在请求头中携带用户ID：
```
User-Id: <用户ID>
```

---

## 1. 用户认证模块 (/api/auth)

### 1.1 用户注册
- **接口地址**：`POST /api/auth/register`
- **功能描述**：创建新的用户账号
- **请求参数**：
  ```json
  {
      "username": "zhangsan",
      "email": "zhangsan@example.com",
      "password": "123456",
      "phone": "13800138000",
      "city": "北京市",
      "real_name": "张三"
  }
  ```
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": {
          "user_id": 1,
          "username": "zhangsan"
      },
      "message": "注册成功"
  }
  ```

### 1.2 用户登录
- **接口地址**：`POST /api/auth/login`
- **功能描述**：用户登录获取访问权限
- **请求参数**：
  ```json
  {
      "username": "zhangsan",
      "password": "123456"
  }
  ```
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": {
          "user_id": 1,
          "username": "zhangsan"
      },
      "message": "登录成功"
  }
  ```

### 1.3 获取用户信息
- **接口地址**：`GET /api/auth/profile`
- **功能描述**：获取当前登录用户的信息
- **认证要求**：需要

### 1.4 更新用户信息
- **接口地址**：`PUT /api/auth/profile`
- **功能描述**：更新当前登录用户的信息
- **认证要求**：需要
- **请求参数**：
  ```json
  {
      "nickname": "新昵称",
      "avatar": "头像URL",
      "phone": "手机号",
      "city": "城市",
      "bio": "个人简介"
  }
  ```

---

## 2. 用户中心模块 (/api/user)

### 2.1 获取用户列表
- **接口地址**：`GET /api/user/list`
- **功能描述**：获取用户列表（管理员用）
- **认证要求**：需要
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": {
          "users": [
              {
                  "id": 1,
                  "username": "user1",
                  "nickname": "用户1",
                  "email": "user1@example.com",
                  "phone": "13800138000",
                  "city": "北京市",
                  "real_name": "张三",
                  "created_at": "2024-01-01T00:00:00"
              }
          ],
          "pagination": {
              "page": 1,
              "page_size": 20,
              "total": 100,
              "total_pages": 5
          }
      },
      "message": "获取成功"
  }
  ```

### 2.2 获取用户基本信息
- **接口地址**：`GET /api/user/profile`
- **功能描述**：获取当前用户的个人信息
- **认证要求**：需要

### 2.3 更新用户基本信息
- **接口地址**：`PUT /api/user/profile`
- **功能描述**：更新当前用户的个人信息
- **认证要求**：需要
- **请求参数**：
  ```json
  {
      "nickname": "新昵称",
      "avatar": "头像URL",
      "phone": "手机号",
      "city": "城市",
      "bio": "个人简介"
  }
  ```

### 2.4 获取用户仪表板数据
- **接口地址**：`GET /api/user/dashboard`
- **功能描述**：获取用户在个人中心的统计和推荐数据
- **认证要求**：需要

### 2.5 获取我的活动列表
- **接口地址**：`GET /api/user/my-activities`
- **功能描述**：获取用户参与的活动列表
- **认证要求**：需要

### 2.6 获取我的赛事列表
- **接口地址**：`GET /api/user/my-events`
- **功能描述**：获取用户参与的赛事列表
- **认证要求**：需要

### 2.7 获取用户统计信息
- **接口地址**：`GET /api/user/statistics`
- **功能描述**：获取用户的各种统计数据
- **认证要求**：需要

### 2.8 获取用户预约列表
- **接口地址**：`GET /api/user/bookings`
- **功能描述**：获取当前用户的预约记录
- **认证要求**：需要

---

## 3. 场馆管理模块 (/api/venue)

### 3.1 获取场馆分类列表
- **接口地址**：`GET /api/venue/categories`
- **功能描述**：获取所有启用的场馆分类信息
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": [
          {
              "id": 1,
              "name": "篮球场",
              "description": "室内篮球场地",
              "is_active": true
          },
          {
              "id": 2,
              "name": "羽毛球场",
              "description": "专业羽毛球场地",
              "is_active": true
          }
      ],
      "message": "获取成功"
  }
  ```

### 3.2 获取场馆列表
- **接口地址**：`GET /api/venue/list`
- **功能描述**：支持分页、搜索、分类筛选的场馆列表
- **查询参数**：
  - `page`: 页码（默认1）
  - `page_size`: 每页数量（默认20）
  - `keyword`: 搜索关键词（场馆名称、类型、地址）
  - `category_id`: 分类ID
  - `is_hot`: 是否热门（1:热门 0:全部，默认0）
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": {
          "venues": [
              {
                  "id": 1,
                  "name": "体育中心篮球场",
                  "category": "篮球场",
                  "location": "市中心体育中心",
                  "price_per_hour": 100.0,
                  "rating": 4.8,
                  "is_hot": true,
                  "images": ["http://example.com/image1.jpg"],
                  "facilities": ["空调", "停车位", "更衣室"],
                  "description": "专业篮球场地，设施齐全"
              }
          ],
          "pagination": {
              "page": 1,
              "page_size": 20,
              "total": 50,
              "total_pages": 3
          }
      },
      "message": "获取成功"
  }
  ```

### 3.3 获取热门场馆
- **接口地址**：`GET /api/venue/hot`
- **功能描述**：获取热门推荐的场馆列表

### 3.4 获取场馆详情
- **接口地址**：`GET /api/venue/{venue_id}`
- **功能描述**：获取指定场馆的详细信息
- **路径参数**：
  - `venue_id`: 场馆ID

### 3.5 获取场馆可用时间
- **接口地址**：`GET /api/venue/{venue_id}/availability`
- **功能描述**：获取指定场馆的可用时间段
- **路径参数**：
  - `venue_id`: 场馆ID

### 3.6 获取轮播图
- **接口地址**：`GET /api/venue/banners`
- **功能描述**：获取首页轮播图列表

### 3.7 搜索场馆
- **接口地址**：`GET /api/venue/search`
- **功能描述**：根据关键词搜索场馆
- **查询参数**：
  - `keyword`: 搜索关键词
  - `page`: 页码
  - `page_size`: 每页数量

### 3.8 添加场馆评价
- **接口地址**：`POST /api/venue/{venue_id}/reviews`
- **功能描述**：为指定场馆添加评价
- **路径参数**：
  - `venue_id`: 场馆ID
- **认证要求**：需要
- **请求参数**：
  ```json
  {
      "rating": 5,
      "content": "场地很好，设施齐全",
      "images": ["图片URL1", "图片URL2"]
  }
  ```

### 3.9 获取场馆评价列表
- **接口地址**：`GET /api/venue/{venue_id}/reviews`
- **功能描述**：获取指定场馆的评价列表
- **路径参数**：
  - `venue_id`: 场馆ID
- **查询参数**：
  - `page`: 页码
  - `page_size`: 每页数量
  - `sort`: 排序方式（newest:最新，oldest:最早，rating_high:评分高，rating_low:评分低）

### 3.10 标记评价有用
- **接口地址**：`POST /api/venue/reviews/{review_id}/helpful`
- **功能描述**：标记某条评价为有用
- **路径参数**：
  - `review_id`: 评价ID
- **认证要求**：需要

### 3.11 删除评价
- **接口地址**：`DELETE /api/venue/reviews/{review_id}`
- **功能描述**：删除指定的评价（只能删除自己的评价）
- **路径参数**：
  - `review_id`: 评价ID
- **认证要求**：需要

---

## 4. 教练管理模块 (/api/coaches)

### 4.1 获取教练列表
- **接口地址**：`GET /api/coaches`
- **功能描述**：获取教练列表，支持筛选
- **查询参数**：
  - `page`: 页码
  - `page_size`: 每页数量
  - `specialization`: 专业领域
  - `keyword`: 搜索关键词
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": {
          "coaches": [
              {
                  "id": 1,
                  "name": "王教练",
                  "specialization": "篮球",
                  "experience_years": 5,
                  "rating": 4.9,
                  "hourly_rate": 150.0,
                  "description": "专业篮球教练，擅长基础训练",
                  "certification": "国家级篮球教练员",
                  "avatar": "http://example.com/avatar.jpg"
              }
          ],
          "pagination": {
              "page": 1,
              "page_size": 20,
              "total": 15,
              "total_pages": 1
          }
      },
      "message": "获取成功"
  }
  ```

### 4.2 创建教练
- **接口地址**：`POST /api/coaches`
- **功能描述**：创建新的教练信息
- **认证要求**：需要（管理员）
- **请求参数**：
  ```json
  {
      "name": "李教练",
      "specialization": "游泳",
      "experience_years": 8,
      "hourly_rate": 200.0,
      "description": "专业游泳教练",
      "certification": "游泳教练证书",
      "contact_phone": "13900139000",
      "email": "coach@example.com"
  }
  ```

### 4.3 更新教练信息
- **接口地址**：`PUT /api/coaches/{coach_id}`
- **功能描述**：更新指定教练的信息
- **路径参数**：
  - `coach_id`: 教练ID
- **认证要求**：需要（管理员）

### 4.4 删除教练
- **接口地址**：`DELETE /api/coaches/{coach_id}`
- **功能描述**：删除指定的教练
- **路径参数**：
  - `coach_id`: 教练ID
- **认证要求**：需要（管理员）

### 4.5 批量删除教练
- **接口地址**：`POST /api/coaches/batch-delete`
- **功能描述**：批量删除教练
- **认证要求**：需要（管理员）
- **请求参数**：
  ```json
  {
      "coach_ids": [1, 2, 3]
  }
  ```

### 4.6 获取教练详情
- **接口地址**：`GET /api/coaches/{coach_id}`
- **功能描述**：获取指定教练的详细信息
- **路径参数**：
  - `coach_id`: 教练ID

### 4.7 获取专业领域列表
- **接口地址**：`GET /api/coaches/specializations`
- **功能描述**：获取所有教练专业领域列表

---

## 5. 预约管理模块 (/api/booking)

### 5.1 创建预约
- **接口地址**：`POST /api/booking/create`
- **功能描述**：创建新的场馆预约
- **认证要求**：需要
- **请求参数**：
  ```json
  {
      "venue_id": 1,
      "date": "2024-01-15",
      "start_time": "14:00",
      "duration": 2,
      "total_price": 200.0,
      "notes": "希望安排在靠窗位置"
  }
  ```

### 5.2 获取我的预约列表
- **接口地址**：`GET /api/booking/my-bookings`
- **功能描述**：获取当前用户的预约列表
- **认证要求**：需要

### 5.3 创建分享预约
- **接口地址**：`POST /api/booking/create-with-share`
- **功能描述**：创建支持多人分摊费用的预约
- **认证要求**：需要

### 5.4 获取预约分享信息
- **接口地址**：`GET /api/booking/{booking_id}/shares`
- **功能描述**：获取指定预约的分享信息
- **路径参数**：
  - `booking_id`: 预约ID
- **认证要求**：需要

### 5.5 支付分享费用
- **接口地址**：`POST /api/booking/{booking_id}/shares/{share_id}/pay`
- **功能描述**：支付自己的分享费用
- **路径参数**：
  - `booking_id`: 预约ID
  - `share_id`: 分享ID
- **认证要求**：需要

### 5.6 获取预约详情
- **接口地址**：`GET /api/booking/{booking_id}`
- **功能描述**：获取指定预约的详细信息
- **路径参数**：
  - `booking_id`: 预约ID
- **认证要求**：需要

### 5.7 取消预约
- **接口地址**：`POST /api/booking/{booking_id}/cancel`
- **功能描述**：取消指定的预约
- **路径参数**：
  - `booking_id`: 预约ID
- **认证要求**：需要

### 5.8 完成预约
- **接口地址**：`POST /api/booking/{booking_id}/complete`
- **功能描述**：标记预约为已完成
- **路径参数**：
  - `booking_id`: 预约ID
- **认证要求**：需要

### 5.9 获取预约统计
- **接口地址**：`GET /api/booking/statistics`
- **功能描述**：获取预约相关的统计信息
- **认证要求**：需要

### 5.10 获取预约列表
- **接口地址**：`GET /api/booking/list`
- **功能描述**：获取所有预约列表（管理员用）
- **响应示例**：
  ```json
  {
      "code": 200,
      "data": {
          "bookings": [],
          "pagination": {
              "page": 1,
              "page_size": 20,
              "total": 0,
              "total_pages": 0
          }
      },
      "message": "获取成功"
  }
  ```

---

## 6. 赛事管理模块 (/api/events)

### 6.1 获取赛事列表
- **接口地址**：`GET /api/events/list`
- **功能描述**：获取可报名的赛事列表，支持分页和搜索
- **查询参数**：
  - `page`: 页码（默认1）
  - `page_size`: 每页数量（默认20）
  - `keyword`: 搜索关键词
  - `status`: 赛事状态筛选
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": {
          "events": [
              {
                  "id": 1,
                  "event_type": "马拉松",
                  "event_date": "2024-10-20",
                  "description": "年度大型城市马拉松赛事，途经天安门、故宫等著名地标",
                  "current_participants": 12500,
                  "created_at": "2025-11-17T10:30:27"
              },
              {
                  "id": 2,
                  "event_type": "篮球对抗赛",
                  "event_date": "2024-12-15",
                  "description": "高校间篮球对抗赛",
                  "current_participants": 28,
                  "created_at": "2025-11-17T10:30:27"
              },
              {
                  "id": 3,
                  "event_type": "游泳比赛",
                  "event_date": "2024-11-30",
                  "description": "市级游泳锦标赛",
                  "current_participants": 320,
                  "created_at": "2025-11-17T10:30:27"
              },
              {
                  "id": 4,
                  "event_type": "半程马拉松",
                  "event_date": "2024-09-15",
                  "description": "面向业余跑者的半程马拉松比赛",
                  "current_participants": 8200,
                  "created_at": "2025-11-17T10:30:27"
              },
              {
                  "id": 5,
                  "event_type": "自行车赛",
                  "event_date": "2024-09-30",
                  "description": "沿海环岛自行车竞赛",
                  "current_participants": 650,
                  "created_at": "2025-11-17T10:30:27"
              },
              {
                  "id": 6,
                  "event_type": "羽毛球",
                  "event_date": "2024-08-25",
                  "description": "业余羽毛球爱好者比赛",
                  "current_participants": 189,
                  "created_at": "2025-11-17T10:30:27"
              },
              {
                  "id": 7,
                  "event_type": "越野跑",
                  "event_date": "2024-07-20",
                  "description": "山地越野跑，体验自然风光",
                  "current_participants": 1500,
                  "created_at": "2025-11-17T10:30:27"
              },
              {
                  "id": 8,
                  "event_type": "欢乐跑",
                  "event_date": "2024-06-01",
                  "description": "5公里欢乐跑，适合家庭参与",
                  "current_participants": 3800,
                  "created_at": "2025-11-17T10:30:27"
              }
          ],
          "pagination": {
              "page": 1,
              "page_size": 20,
              "total": 8,
              "total_pages": 1
          }
      },
      "message": "获取成功"
  }
  ```

### 6.2 获取赛事详情
- **接口地址**：`GET /api/events/{event_id}`
- **功能描述**：获取指定赛事的详细信息
- **路径参数**：
  - `event_id`: 赛事ID
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": {
          "event": {
              "id": 7,
              "event_type": "越野跑",
              "event_date": "2024-07-20",
              "description": "山地越野跑，体验自然风光",
              "current_participants": 1500,
              "created_at": "2025-11-17T10:30:27",
              "registration_deadline": "2024-07-15",
              "max_participants": 2000,
              "entry_fee": 50.0,
              "organizer": "户外运动协会",
              "contact_info": "organizer@outdoor.com",
              "event_rules": "1. 需自备装备 2. 注意安全 3. 遵守路线",
              "prizes": "前10名获得奖牌和奖品",
              "location": "山地森林公园",
              "difficulty_level": "中等"
          }
      },
      "message": "获取成功"
  }
  ```

### 6.3 报名赛事
- **接口地址**：`POST /api/events/{event_id}/register`
- **功能描述**：报名参加指定的赛事
- **路径参数**：
  - `event_id`: 赛事ID
- **认证要求**：需要
- **请求参数**：
  ```json
  {
      "user_name": "张三",
      "contact": "13800138000",
      "notes": "我是业余爱好者，希望参与体验"
  }
  ```
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": {
          "registration_id": 1001,
          "event_id": 7,
          "status": "pending",
          "registration_time": "2024-12-20T10:30:00"
      },
      "message": "报名成功，请等待审核"
  }
  ```

### 6.4 获取我的赛事报名
- **接口地址**：`GET /api/events/my-registrations`
- **功能描述**：获取当前用户的赛事报名记录
- **认证要求**：需要
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": {
          "registrations": [
              {
                  "id": 1001,
                  "event": {
                      "id": 7,
                      "event_type": "越野跑",
                      "event_date": "2024-07-20"
                  },
                  "status": "pending",
                  "registration_time": "2024-12-20T10:30:00",
                  "approval_time": null
              }
          ]
      },
      "message": "获取成功"
  }
  ```

### 6.5 获取赛事报名列表
- **接口地址**：`GET /api/events/{event_id}/registrations`
- **功能描述**：获取指定赛事的报名列表（组织者用）
- **路径参数**：
  - `event_id`: 赛事ID
- **认证要求**：需要
- **查询参数**：
  - `page`: 页码
  - `page_size`: 每页数量
  - `status`: 报名状态筛选（pending, approved, rejected）

### 6.6 批准报名
- **接口地址**：`POST /api/events/registrations/{registration_id}/approve`
- **功能描述**：批准指定的用户报名
- **路径参数**：
  - `registration_id`: 报名ID
- **认证要求**：需要（管理员）

### 6.7 拒绝报名
- **接口地址**：`POST /api/events/registrations/{registration_id}/reject`
- **功能描述**：拒绝指定的用户报名
- **路径参数**：
  - `registration_id`: 报名ID
- **认证要求**：需要（管理员）

### 6.8 取消报名
- **接口地址**：`POST /api/events/{event_id}/unregister`
- **功能描述**：取消已报的赛事
- **路径参数**：
  - `event_id`: 赛事ID
- **认证要求**：需要

### 6.9 获取赛事统计
- **接口地址**：`GET /api/events/statistics`
- **功能描述**：获取赛事相关统计信息
- **认证要求**：需要（管理员）

---

## 7. 活动管理模块 (/api/activity)

### 7.1 创建活动
- **接口地址**：`POST /api/activity/create`
- **功能描述**：创建新的活动
- **认证要求**：需要
- **请求参数**：
  ```json
  {
      "title": "周末篮球活动",
      "description": "一起打篮球，强身健体",
      "activity_date": "2024-01-20",
      "start_time": "09:00",
      "end_time": "12:00",
      "max_participants": 20,
      "location": "体育中心篮球场",
      "tags": ["篮球", "周末", "运动"]
  }
  ```

### 7.2 获取活动列表
- **接口地址**：`GET /api/activity/list`
- **功能描述**：获取活动列表，支持筛选
- **查询参数**：
  - `page`: 页码
  - `page_size`: 每页数量
  - `keyword`: 搜索关键词
  - `activity_date`: 活动日期筛选
- **响应示例**：
  ```json
  {
      "code": 0,
      "data": {
          "activities": [
              {
                  "id": 1,
                  "title": "周末篮球活动",
                  "description": "一起打篮球，强身健体",
                  "activity_date": "2024-01-20",
                  "start_time": "09:00",
                  "end_time": "12:00",
                  "location": "体育中心篮球场",
                  "current_participants": 15,
                  "max_participants": 20,
                  "creator": {
                      "id": 1,
                      "username": "organizer"
                  },
                  "tags": ["篮球", "周末"],
                  "created_at": "2024-01-15T10:00:00"
              }
          ],
          "pagination": {
              "page": 1,
              "page_size": 20,
              "total": 25,
              "total_pages": 2
          }
      },
      "message": "获取成功"
  }
  ```

### 7.3 获取我的活动
- **接口地址**：`GET /api/activity/my-activities`
- **功能描述**：获取当前用户创建和参与的活动
- **认证要求**：需要

### 7.4 获取活动详情
- **接口地址**：`GET /api/activity/{activity_id}`
- **功能描述**：获取指定活动的详细信息
- **路径参数**：
  - `activity_id`: 活动ID

### 7.5 参加活动
- **接口地址**：`POST /api/activity/{activity_id}/join`
- **功能描述**：参加指定的活动
- **路径参数**：
  - `activity_id`: 活动ID
- **认证要求**：需要

### 7.6 退出活动
- **接口地址**：`POST /api/activity/{activity_id}/leave`
- **功能描述**：退出已参加的活动
- **路径参数**：
  - `activity_id`: 活动ID
- **认证要求**：需要

### 7.7 更新活动
- **接口地址**：`PUT /api/activity/{activity_id}/update`
- **功能描述**：更新活动信息（只能更新自己创建的活动）
- **路径参数**：
  - `activity_id`: 活动ID
- **认证要求**：需要

### 7.8 删除活动
- **接口地址**：`DELETE /api/activity/{activity_id}`
- **功能描述**：删除活动（只能删除自己创建的活动）
- **路径参数**：
  - `activity_id`: 活动ID
- **认证要求**：需要

### 7.9 获取活动类型
- **接口地址**：`GET /api/activity/types`
- **功能描述**：获取所有活动类型列表

---

## 8. 好友系统模块 (/api/friends)

### 8.1 获取好友列表
- **接口地址**：`GET /api/friends/list`
- **功能描述**：获取当前用户的好友列表
- **认证要求**：需要

### 8.2 添加好友
- **接口地址**：`POST /api/friends/add`
- **功能描述**：向其他用户发送好友申请
- **认证要求**：需要
- **请求参数**：
  ```json
  {
      "target_user_id": 123,
      "message": "我是通过活动认识你的，可以加个好友吗？"
  }
  ```

### 8.3 获取好友申请列表
- **接口地址**：`GET /api/friends/requests`
- **功能描述**：获取当前用户收到的好友申请列表
- **认证要求**：需要

### 8.4 接受好友申请
- **接口地址**：`POST /api/friends/{request_id}/accept`
- **功能描述**：接受指定的好友申请
- **路径参数**：
  - `request_id`: 好友申请ID
- **认证要求**：需要

### 8.5 拒绝好友申请
- **接口地址**：`POST /api/friends/{request_id}/reject`
- **功能描述**：拒绝指定的好友申请
- **路径参数**：
  - `request_id`: 好友申请ID
- **认证要求**：需要

### 8.6 删除好友
- **接口地址**：`DELETE /api/friends/{friend_id}/remove`
- **功能描述**：删除指定的好友关系
- **路径参数**：
  - `friend_id`: 好友ID
- **认证要求**：需要

### 8.7 搜索用户
- **接口地址**：`GET /api/friends/search`
- **功能描述**：根据用户名或昵称搜索用户
- **认证要求**：需要
- **查询参数**：
  - `keyword`: 搜索关键词

---

## 9. 系统管理模块 (/api/admin)

### 9.1 获取系统统计
- **接口地址**：`GET /api/admin/statistics`
- **功能描述**：获取系统整体统计数据
- **认证要求**：需要（管理员）

### 9.2 获取用户管理
- **接口地址**：`GET /api/admin/users`
- **功能描述**：管理用户信息
- **认证要求**：需要（管理员）

### 9.3 系统配置
- **接口地址**：`GET /api/admin/config`
- **功能描述**：获取系统配置信息
- **认证要求**：需要（管理员）

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 401 | 用户未登录或登录已过期 |
| 403 | 没有权限访问该资源 |
| 404 | 资源不存在 |
| 409 | 资源冲突（如用户名已存在、重复预约等） |
| 500 | 服务器内部错误 |

## 常用状态码

### 预约状态
- `pending` - 待审核
- `confirmed` - 已确认
- `cancelled` - 已取消
- `completed` - 已完成

### 赛事状态
- `open` - 开放报名
- `closed` - 报名截止
- `in_progress` - 进行中
- `finished` - 已结束

### 活动状态
- `upcoming` - 即将开始
- `ongoing` - 进行中
- `ended` - 已结束
- `cancelled` - 已取消

## 注意事项

1. **认证要求**
   - 所有需要认证的接口都需要在请求头中携带 `User-Id` 参数
   - 部分管理员接口需要额外的权限验证

2. **日期时间格式**
   - 日期：`YYYY-MM-DD`
   - 时间：`HH:MM`
   - 日期时间：`YYYY-MM-DD HH:MM:SS`

3. **价格和数值**
   - 价格相关字段单位为元（CNY）
   - 参与人数为整数
   - 评分范围1-5分

4. **分页规则**
   - `page` 从1开始
   - `page_size` 最大值为100
   - 默认每页20条记录

5. **图片上传**
   - 支持格式：JPG, PNG, GIF
   - 单张图片大小限制：5MB
   - 使用 multipart/form-data 格式上传

6. **搜索和筛选**
   - 关键词搜索支持模糊匹配
   - 分类筛选使用对应的ID
   - 时间筛选格式：YYYY-MM-DD

7. **缓存说明**
   - 列表接口支持客户端缓存
   - 详情接口实时获取最新数据
   - 缓存失效时间：5分钟

---

## 测试用例

### curl 示例

```bash
# 获取赛事列表
curl -X GET "http://127.0.0.1:5000/api/events/list" \
  -H "Content-Type: application/json"

# 获取场馆分类
curl -X GET "http://127.0.0.1:5000/api/venue/categories" \
  -H "Content-Type: application/json"

# 获取用户列表（需要管理员权限）
curl -X GET "http://127.0.0.1:5000/api/user/list" \
  -H "Content-Type: application/json" \
  -H "User-Id: 1"
```

### JavaScript 示例

```javascript
// 获取赛事列表
async function getEvents() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/events/list');
        const data = await response.json();
        console.log('赛事列表:', data);
    } catch (error) {
        console.error('获取赛事失败:', error);
    }
}

// 赛事报名
async function registerEvent(eventId, userInfo) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/events/${eventId}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'User-Id': '1' // 需要用户ID
            },
            body: JSON.stringify(userInfo)
        });
        const data = await response.json();
        console.log('报名结果:', data);
    } catch (error) {
        console.error('报名失败:', error);
    }
}
```

---

**文档生成时间**: 2025年11月20日  
**API版本**: v1.0  
**服务器地址**: http://127.0.0.1:5000  
**文档状态**: 完整版 - 包含所有已实现的API接口

> 📝 **更新日志**
> - 2025-11-20: 完善赛事管理模块，添加所有赛事相关接口
> - 2025-11-20: 更新教练管理模块，添加CRUD操作
> - 2025-11-20: 优化响应格式和示例代码
> - 2025-11-20: 添加测试用例和注意事项
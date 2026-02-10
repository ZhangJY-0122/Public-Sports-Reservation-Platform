// API服务统一管理
import { http } from '@/utils/http.js'

// 认证相关API
export const authAPI = {
  // 用户登录
  login(data) {
    return http.post('auth/login', data)
  },
  
  // 用户注册
  register(data) {
    return http.post('/api/auth/register', data)
  },
  
  // 获取用户信息
  getUserInfo() {
    return http.get('/api/auth/me')
  },
  
  // 登出
  logout() {
    return http.post('/api/auth/logout')
  }
}

// 场馆相关API
export const venueAPI = {
  // 获取所有场馆
  getVenues() {
    return http.get('/api/venue/list')
  },
  
  // 获取单个场馆详情
  getVenueDetail(id) {
    return http.get(`/api/venue/${id}`)
  },
  
  // 搜索场馆
  searchVenues(params) {
    return http.get('/api/venue/search', params)
  },
  
  // 获取场馆分类
  getCategories() {
    return http.get('/api/venue/categories')
  }
}

// 预约相关API
export const bookingAPI = {
  // 获取用户预约列表
  getBookings() {
    return http.get('/api/booking/list')
  },
  
  // 创建预约
  createBooking(data) {
    return http.post('/api/booking/create', data)
  },
  
  // 获取预约详情
  getBookingDetail(id) {
    return http.get(`/api/booking/${id}`)
  },
  
  // 取消预约
  cancelBooking(id) {
    return http.delete(`/api/booking/cancel/${id}`)
  }
}

// 统计数据API
export const statsAPI = {
  // 获取仪表盘数据
  getDashboard() {
    return http.get('/api/stats/dashboard')
  },
  
  // 获取用户统计
  getUserStats() {
    return http.get('/api/stats/user')
  }
}
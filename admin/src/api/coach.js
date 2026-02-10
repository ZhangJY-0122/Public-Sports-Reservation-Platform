import request from '@/utils/request'

// 教练相关API
export const coachApi = {
  // ====== 教练相关API ======
  // 获取教练列表
  getCoachList(params = {}) {
    return request.get('/api/coaches/list', params)
  },
  
  // 获取教练详情
  getCoachDetail(id) {
    return request.get(`/api/coaches/${id}`)
  },
  
  // 创建教练
  createCoach(data) {
    return request.post('/api/coaches/', data)
  },
  
  // 更新教练
  updateCoach(id, data) {
    return request.put(`/api/coaches/${id}`, data)
  },
  
  // 删除教练
  deleteCoach(id) {
    return request.post(`/api/coaches/${id}/delete`)
  },
  
  // 切换教练状态
  toggleCoachStatus(id, is_active) {
    return request.post(`/api/coaches/${id}/toggle-status`, { is_active })
  },
  
  // 获取教练可用时间段
  getCoachAvailability(id, params = {}) {
    return request.get(`/api/coaches/${id}/availability`, params)
  },
  
  // 预约教练
  bookCoach(data) {
    return request.post('/api/coaches/book', data)
  },
  
  // 获取我的教练预约
  getMyBookings(params = {}) {
    return request.get('/api/coaches/my-bookings', params)
  },
  
  // 获取所有教练预约（管理员接口）
  getAllBookings(params = {}) {
    return request.get('/api/coaches/admin/bookings', params)
  },
  
  // 获取预约详情
  getBookingDetail(id) {
    return request.get(`/api/coaches/bookings/${id}`)
  },
  
  // 取消预约
  cancelBooking(id) {
    return request.post(`/api/coaches/bookings/${id}/cancel`)
  }
}

// 图片上传API
export const uploadImage = (formData) => {
  return request.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 导出别名，保持与其他页面的一致性
export const getCoachesList = coachApi.getCoachList
export const getCoachDetail = coachApi.getCoachDetail
export const createCoach = coachApi.createCoach
export const updateCoach = coachApi.updateCoach
export const deleteCoach = coachApi.deleteCoach
export const getAllCoachBookings = coachApi.getAllBookings
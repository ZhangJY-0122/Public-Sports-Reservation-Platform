import request from '@/utils/request'

/**
 * 赛事管理API
 */

// 赛事相关API对象
export const eventApi = {
  // ====== 赛事相关API ======
  // 获取赛事列表
  getEventsList(params = {}) {
    return request.get('/api/events/list', params)
  },
  
  // 获取赛事详情
  getEventDetail(id) {
    return request.get(`/api/events/${id}`)
  },
  
  // 创建赛事
  createEvent(data) {
    return request.post('/api/events', data)
  },
  
  // 更新赛事
  updateEvent(id, data) {
    return request.put(`/api/events/${id}`, data)
  },
  
  // 删除赛事
  deleteEvent(id) {
    return request.delete(`/api/events/${id}`)
  },
  
  // 赛事报名
  registerEvent(id, data) {
    return request.post(`/api/events/${id}/register`, data)
  },
  
  // 获取我的赛事申请
  getMyEventRegistrations() {
    return request.get('/api/events/my-registrations')
  },
  
  // 获取赛事报名列表
  getEventRegistrations(id) {
    return request.get(`/api/events/${id}/registrations`)
  },
  
  // 审核赛事报名 - 批准
  approveEventRegistration(registrationId) {
    return request.post(`/api/events/registrations/${registrationId}/approve`)
  },
  
  // 审核赛事报名 - 拒绝
  rejectEventRegistration(registrationId) {
    return request.post(`/api/events/registrations/${registrationId}/reject`)
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
export const getEventsList = eventApi.getEventsList
export const getEventDetail = eventApi.getEventDetail
export const createEvent = eventApi.createEvent
export const updateEvent = eventApi.updateEvent
export const deleteEvent = eventApi.deleteEvent
export const registerEvent = eventApi.registerEvent
export const getMyEventRegistrations = eventApi.getMyEventRegistrations
export const getEventRegistrations = eventApi.getEventRegistrations
export const approveEventRegistration = eventApi.approveEventRegistration
export const rejectEventRegistration = eventApi.rejectEventRegistration
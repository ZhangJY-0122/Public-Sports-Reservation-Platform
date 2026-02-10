import request from '@/utils/request'

// 活动相关API
export const activityApi = {
  // 获取活动列表
  getActivityList(params = {}) {
    return request.get('/api/activity/list', params)
  },
  
  // 创建活动
  createActivity(data) {
    return request.post('/api/activity/create', data)
  },
  
  // 更新活动
  updateActivity(data) {
    return request.post('/api/activity/update', data)
  },
  
  // 删除活动
  deleteActivity(id) {
    return request.post('/api/activity/delete', { id })
  },
  
  // 批量删除活动
  batchDeleteActivity(ids) {
    return request.post('/api/activity/batchDelete', { ids })
  }
}
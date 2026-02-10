import request from '@/utils/request'

// 场馆相关API
export const venueApi = {
  // ====== 场馆相关API ======
  // 获取场馆列表
  getVenueList(params = {}) {
    return request.get('/api/venue/list', params)
  },
  
  // 创建场馆
  createVenue(data) {
    return request.post('/api/venue/create', data)
  },
  
  // 更新场馆
  updateVenue(data) {
    return request.post('/api/venue/update', data)
  },
  
  // 删除场馆
  deleteVenue(id) {
    return request.post('/api/venue/delete', { id })
  },
  
  // 批量删除场馆
  batchDeleteVenue(ids) {
    return request.post('/api/venue/batchDelete', { ids })
  },
  
  // ====== 场馆评价相关API ======
  
  // 获取场馆评价列表
  getVenueReviews(venueId, params = {}) {
    return request.get(`/api/venues/${venueId}/reviews`, params)
  },
  
  // 创建场馆评价
  createVenueReview(venueId, data) {
    return request.post(`/api/venues/${venueId}/reviews`, data)
  },
  
  // 标记评价为有用
  markReviewHelpful(reviewId) {
    return request.post(`/api/reviews/${reviewId}/helpful`)
  },
  
  // 删除评价
  deleteReview(reviewId) {
    return request.delete(`/api/reviews/${reviewId}`)
  },
  
  // ====== 场馆分类相关API ======
  // 获取场馆分类列表
  getVenueCategories(params = {}) {
    return request.get('/api/venue/categories', params)
  },
  
  // 创建场馆分类
  createCategory(data) {
    return request.post('/api/venue/categories', data)
  },
  
  // 更新场馆分类
  updateCategory(id, data) {
    return request.put(`/api/venue/categories/${id}`, data)
  },
  
  // 删除场馆分类
  deleteCategory(id) {
    return request.delete(`/api/venue/categories/${id}`)
  }
}
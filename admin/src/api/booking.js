import request from '../utils/request'

/**
 * 预约相关API接口
 */
export default {
  /**
   * 获取场馆营业分析数据
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回Promise对象
   */
  getBusinessAnalysis(params = {}) {
    return request.get('/api/booking/business-analysis', params)
  },

  /**
   * 获取预约列表
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回Promise对象
   */
  getBookingList(params = {}) {
    return request.get('/api/booking/list', params)
  }
}
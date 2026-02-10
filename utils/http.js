// 基础配置
const BASE_URL = 'http://127.0.0.1:5000/api/'  // 后端API地址
const TIMEOUT  = 15000                  // 15s

// 取 token
const getToken = () => uni.getStorageSync('token') || ''

// 统一错误提示
const showError = (msg) => {
  uni.showToast({ title: String(msg), icon: 'none', duration: 3000 })
}

/**
 * 核心请求
 */
function request(options) {
  const {
    url,
    method = 'GET',
    data = {},
    headers = {},
    hideErrorToast = false,
    timeout = TIMEOUT
  } = options

  return new Promise((resolve, reject) => {
	  
	 let user=uni.getStorageSync("user")
	 let user_id=user.user_id
	  
    uni.request({
      url: /^https?:\/\//.test(url) ? url : BASE_URL + url,
      method,
      timeout,
      data,
      header: {
        'content-type': 'application/json',
        Authorization: getToken() ? `Bearer ${getToken()}` : '',
		"User-Id":user_id,
        ...headers
      },
      success: (res) => {
        const { statusCode, data: resData } = res
        if (statusCode >= 200 && statusCode < 300) {
          // 约定 code == 0 为成功
          const { code, msg, data } = resData
          if (code === 0) {
            resolve(data)
          } else {
            !hideErrorToast && showError(msg || '业务异常')
            reject({ code, msg, data })
          }
        } else {
          !hideErrorToast && showError(`请求异常(${statusCode})`)
          reject({ code: statusCode, msg: `HTTP ${statusCode}` })
        }
      },
      fail: (err) => {
        !hideErrorToast && showError('网络错误，请检查网络')
        reject(err)
      }
    })
  })
}

/* 快捷方法 */
export const http = {
  get(url, params, opt) {
    return request({ ...opt, url, method: 'GET', data: params })
  },
  post(url, data, opt) {
    return request({ ...opt, url, method: 'POST', data })
  },
  put(url, data, opt) {
    return request({ ...opt, url, method: 'PUT', data })
  },
  delete(url, params, opt) {
    return request({ ...opt, url, method: 'DELETE', data: params })
  }
}

export const BaseUrl = BASE_URL

/*
import { http } from '@/utils/http.js'

登录 
export function apiLogin(data) {
  return http.post('/user/login', data)
}

获取用户信息 
export function apiGetUserInfo() {
  return http.get('/user/info')
}



import {onShow,onLoad,onReady} from '@dcloudio/uni-app'

import { ref, reactive } from 'vue'
import { http } from '@/utils/http.js'
import {onShow,	onLoad,	onReady} from '@dcloudio/uni-app'



*/

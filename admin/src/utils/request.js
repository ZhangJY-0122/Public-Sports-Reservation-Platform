import axios from 'axios'
import { ElMessage } from 'element-plus'

// 环境配置
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000'

// 开发环境下打印环境信息
if (import.meta.env.DEV) {
  console.log('🚀 当前运行环境:', import.meta.env.MODE)
  console.log('📡 API 地址:', baseURL)
}



class Request {
  constructor() {
    this.instance = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    this.setupInterceptors()
  }

  setupInterceptors() {
    // 请求拦截器
    this.instance.interceptors.request.use(
      (config) => {
        // 动态获取 userStore，避免循环依赖
        const userStore = this.getUserStore()
        
        if (userStore?.token) {
          config.headers.Authorization = `Bearer ${userStore.token}`
   
        }

          // 新增 User-Id 头部
      if (userStore?.userInfo?.id) {
        config.headers['User-Id'] = userStore.userInfo.id
      }


        // 开发环境下打印请求信息
        if (import.meta.env.DEV) {
          console.log(`➡️ ${config.method?.toUpperCase()} ${config.url}`, config.params || config.data)
        }

        // 合并自定义 headers
        if (config.customHeaders) {
          config.headers = {
            ...config.headers,
            ...config.customHeaders
          }
        }

        return config
      },
      (error) => {
        console.error('请求配置错误:', error)
        return Promise.reject(error)
      }
    )

    // 响应拦截器
    this.instance.interceptors.response.use(
      (response) => {
        const { data, status, config } = response
        
        // 开发环境下打印响应信息
        if (import.meta.env.DEV) {
          console.log(`⬅️ ${config.method?.toUpperCase()} ${config.url}`, data)
        }

        if (status >= 200 && status < 300) {
          if (data && typeof data === 'object') {
            // 业务错误处理
            if (data.code !== undefined && data.code !== 200 && data.code !== 0) {
        
              this.handleBusinessError(data, config.showError)
              return Promise.reject(data)
            }
            return data
          }
          return data
        }
        
        if (config.showError !== false) {
          ElMessage.error(`请求失败，状态码: ${status}`)
        }
        return Promise.reject(new Error(`请求失败，状态码: ${status}`))
      },
      (error) => {
        // 开发环境下打印错误信息
        if (import.meta.env.DEV) {
          console.error('❌ 请求错误:', error)
        }
        
        this.handleHttpError(error, error.config?.showError)
        return Promise.reject(error)
      }
    )
  }

  // 动态获取 userStore 的方法
  getUserStore() {
    try {
      // 动态导入，避免循环依赖
      const { useUserStore } = require('@/stores/modules/user')
      return useUserStore?.()
    } catch (error) {
      console.warn('UserStore 未找到，可能是循环依赖问题')
      return null
    }
  }

  handleBusinessError(data, showError = true) {
    const { code, message } = data
    
    if (showError) {
      switch (code) {
        case 401:
          this.handleUnauthorized()
          break
        case 403:
          ElMessage.error('权限不足')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(message || '业务处理失败')
      }
    }
  }

  handleHttpError(error, showError = true) {
    if (!showError) return
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          this.handleUnauthorized()
          break
        case 403:
          ElMessage.error('权限不足，禁止访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(data?.message || `网络错误: ${status}`)
      }
    } else if (error.request) {
      ElMessage.error('网络连接异常，请检查网络设置')
    } else {
      ElMessage.error('请求配置错误')
    }
  }

  handleUnauthorized() {
    // 使用动态导入避免循环依赖
    import('@/router').then((routerModule) => {
      const router = routerModule.default
      const userStore = this.getUserStore()
      
      if (userStore && typeof userStore.clearUserInfo === 'function') {
        userStore.clearUserInfo()
      }
      
      ElMessage.warning('登录已过期，请重新登录')
      
      if (router && typeof router.push === 'function') {
        router.push('/login')
      } else {
        // 备用方案
        window.location.href = '/login'
      }
    }).catch(error => {
      console.error('路由导入失败:', error)
      // 备用方案：直接跳转
      window.location.href = '/login'
    })
  }

  request(config) {
    return this.instance.request(config)
  }

  get(url, params, config) {
    return this.request({
      url,
      method: 'GET',
      params,
      ...config
    })
  }

  post(url, data, config) {
    return this.request({
      url,
      method: 'POST',
      data,
      ...config
    })
  }

  put(url, data, config) {
    return this.request({
      url,
      method: 'PUT',
      data,
      ...config
    })
  }

  delete(url, params, config) {
    return this.request({
      url,
      method: 'DELETE',
      params,
      ...config
    })
  }

  getInstance() {
    return this.instance
  }
}

const http = new Request()

export default http
export { baseURL }

/*
// 基本使用
http.get('/users', { page: 1 })
http.post('/users', { name: 'John' })

// 自定义 headers
http.get('/data', null, {
  headers: {
    'X-Custom-Header': 'value',
    'Authorization': 'Custom-Token' // 会覆盖拦截器中的设置
  }
})

// 禁用错误提示
http.get('/data', null, {
  showError: false
})

*/
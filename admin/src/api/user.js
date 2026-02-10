import request from '@/utils/request';

// 用户注册
export const userRegisterService = ({ username, password, email, phone, city, real_name }) => {
  return request.post('/api/auth/register', { username, password, email, phone, city, real_name })
}

// 用户登录
export const userLoginService = ({ mobile, password }) => {
  // 后端需要 username 字段，这里将 mobile 当作 username 使用
  return request.post('/api/auth/login', { username: mobile, password })
}

// 获取用户信息
export const getUserProfile = () => {
  return request.get('/api/user/profile')
}

// 更新用户信息
export const updateUserProfile = (data) => {
  return request.put('/api/user/profile', data)
}

// 用户管理API
export const userApi = {
  // 获取用户列表
  getUserList(params = {}) {
    return request.get('/api/user/list', params)
  },
  
  // 创建用户
  createUser(data) {
    return request.post('/api/user/create', data)
  },
  
  // 更新用户
  updateUser(data) {
    return request.post('/api/user/update', data)
  },
  
  // 删除用户
  deleteUser(id) {
    return request.post('/api/user/delete', { id })
  }
}

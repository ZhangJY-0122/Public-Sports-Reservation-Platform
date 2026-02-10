<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="header">
      <view class="back-btn" @click="handleBack">
        <text class="back-icon">←</text>
      </view>
      <text class="header-title">用户注册</text>
      <view class="placeholder"></view>
    </view>

    <!-- 注册表单 -->
    <view class="register-form">
      <!-- Logo区域 -->
      <view class="logo-section">
        <view class="logo-circle">
          <text class="logo-text">🏟️</text>
        </view>
        <text class="app-name">体育预约</text>
        <text class="app-slogan">加入我们，开启运动之旅</text>
      </view>

      <!-- 表单输入区 -->
      <view class="form-section">
        <!-- 用户名 -->
        <view class="input-group">
          <text class="input-label">用户名</text>
          <view class="input-container">
            <text class="input-icon">👤</text>
            <input 
              type="text" 
              placeholder="请输入用户名"
              class="input-field"
              v-model="formData.username"
              @blur="validateField('username')"
            />
          </view>
          <text class="error-text" v-if="errors.username">{{ errors.username }}</text>
        </view>

        <!-- 邮箱 -->
        <view class="input-group">
          <text class="input-label">邮箱</text>
          <view class="input-container">
            <text class="input-icon">📧</text>
            <input 
              type="text" 
              placeholder="请输入邮箱地址"
              class="input-field"
              v-model="formData.email"
              @blur="validateField('email')"
            />
          </view>
          <text class="error-text" v-if="errors.email">{{ errors.email }}</text>
        </view>

        <!-- 手机号 -->
        <view class="input-group">
          <text class="input-label">手机号</text>
          <view class="input-container">
            <text class="input-icon">📱</text>
            <input 
              type="text" 
              placeholder="请输入手机号"
              class="input-field"
              v-model="formData.phone"
              @blur="validateField('phone')"
            />
          </view>
          <text class="error-text" v-if="errors.phone">{{ errors.phone }}</text>
        </view>

        <!-- 城市 -->
        <view class="input-group">
          <text class="input-label">所在城市</text>
          <view class="input-container">
            <text class="input-icon">🌆</text>
            <picker mode="selector" :range="cityList" @change="onCityChange">
              <view class="picker-field" :class="{ placeholder: !formData.city }">
                {{ formData.city || '请选择所在城市' }}
              </view>
            </picker>
          </view>
          <text class="error-text" v-if="errors.city">{{ errors.city }}</text>
        </view>

        <!-- 密码 -->
        <view class="input-group">
          <text class="input-label">密码</text>
          <view class="input-container">
            <text class="input-icon">🔒</text>
            <input 
              :type="showPassword ? 'text' : 'password'" 
              placeholder="请输入密码（6-20位）"
              class="input-field"
              v-model="formData.password"
              @blur="validateField('password')"
            />
            <text class="toggle-password" @click="togglePassword">
              {{ showPassword ? '👁️' : '👁️‍🗨️' }}
            </text>
          </view>
          <text class="error-text" v-if="errors.password">{{ errors.password }}</text>
        </view>

        <!-- 确认密码 -->
        <view class="input-group">
          <text class="input-label">确认密码</text>
          <view class="input-container">
            <text class="input-icon">🔐</text>
            <input 
              :type="showConfirmPassword ? 'text' : 'password'" 
              placeholder="请再次输入密码"
              class="input-field"
              v-model="formData.confirmPassword"
              @blur="validateField('confirmPassword')"
            />
            <text class="toggle-password" @click="toggleConfirmPassword">
              {{ showConfirmPassword ? '👁️' : '👁️‍🗨️' }}
            </text>
          </view>
          <text class="error-text" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</text>
        </view>

        <!-- 协议同意 -->
        <view class="agreement-section">
          <checkbox-group @change="onAgreementChange">
            <label class="agreement-label">
              <checkbox 
                :checked="agreed" 
                color="#4a90e2"
                class="agreement-checkbox"
              />
              <text class="agreement-text">
                我已阅读并同意 
                <text class="agreement-link">《用户协议》</text> 
                和 
                <text class="agreement-link">《隐私政策》</text>
              </text>
            </label>
          </checkbox-group>
          <text class="error-text" v-if="errors.agreement">{{ errors.agreement }}</text>
        </view>

        <!-- 注册按钮 -->
        <button 
          class="register-btn" 
          :class="{ active: canRegister }"
          :disabled="!canRegister"
          @click="handleRegister"
        >
          立即注册
        </button>
      </view>

      <!-- 登录链接 -->
      <view class="login-link">
        <text class="login-text">已有账号？</text>
        <text class="login-btn" @click="handleLogin">立即登录</text>
      </view>
    </view>
  </view>
</template>

<script setup>
	
	
import { ref, reactive, computed } from 'vue'
import { http } from '@/utils/http.js'

import {onShow,onLoad,onReady} from '@dcloudio/uni-app'

// 表单数据
const formData = reactive({
  username: '',
  email: '',
  phone: '',
  city: '',
  password: '',
  confirmPassword: ''
})

// 错误信息
const errors = reactive({
  username: '',
  email: '',
  phone: '',
  city: '',
  password: '',
  confirmPassword: '',
  agreement: ''
})

// 显示密码
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const agreed = ref(false)

// 城市列表
const cityList = [
  '北京市', '上海市', '广州市', '深圳市', '杭州市', '南京市', 
  '武汉市', '成都市', '西安市', '重庆市', '天津市', '青岛市',
  '大连市', '厦门市', '苏州市', '无锡市', '宁波市', '长沙市'
]

// 能否注册
const canRegister = computed(() => {
  return (
    formData.username.trim() &&
    formData.email.trim() &&
    formData.phone.trim() &&
    formData.city.trim() &&
    formData.password.trim() &&
    formData.confirmPassword.trim() &&
    agreed.value &&
    !errors.username &&
    !errors.email &&
    !errors.phone &&
    !errors.city &&
    !errors.password &&
    !errors.confirmPassword
  )
})

// 切换密码显示
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

// 城市选择
const onCityChange = (e) => {
  formData.city = cityList[e.detail.value]
}

// 协议同意
const onAgreementChange = (e) => {
  agreed.value = e.detail.value.length > 0
  if (agreed.value) {
    errors.agreement = ''
  }
}

// 字段验证
const validateField = (field) => {
  const value = formData[field]
  
  switch (field) {
    case 'username':
      if (!value.trim()) {
        errors.username = '请输入用户名'
      } else if (value.length < 3) {
        errors.username = '用户名至少3个字符'
      } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
        errors.username = '用户名只能包含字母、数字和下划线'
      } else {
        errors.username = ''
      }
      break
      
    case 'email':
      if (!value.trim()) {
        errors.email = '请输入邮箱地址'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        errors.email = '邮箱格式不正确'
      } else {
        errors.email = ''
      }
      break
      
    case 'phone':
      if (!value.trim()) {
        errors.phone = '请输入手机号'
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        errors.phone = '手机号格式不正确'
      } else {
        errors.phone = ''
      }
      break
      
    case 'city':
      if (!value.trim()) {
        errors.city = '请选择所在城市'
      } else {
        errors.city = ''
      }
      break
      
    case 'password':
      if (!value.trim()) {
        errors.password = '请输入密码'
      } else if (value.length < 6 || value.length > 20) {
        errors.password = '密码长度6-20位'
      } else {
        errors.password = ''
      }
      // 重新验证确认密码
      if (formData.confirmPassword) {
        validateField('confirmPassword')
      }
      break
      
    case 'confirmPassword':
      if (!value.trim()) {
        errors.confirmPassword = '请确认密码'
      } else if (value !== formData.password) {
        errors.confirmPassword = '两次输入的密码不一致'
      } else {
        errors.confirmPassword = ''
      }
      break
  }
}

// 注册处理
const handleRegister = () => {
  if (!canRegister.value) return
  
  // 验证所有字段
  validateField('username')
  validateField('email')
  validateField('phone')
  validateField('city')
  validateField('password')
  validateField('confirmPassword')
  
  if (!agreed.value) {
    errors.agreement = '请同意用户协议和隐私政策'
    return
  }
  
  // 模拟注册请求
  uni.showLoading({ title: '注册中...' })
  
     http.post('auth/register', formData)
    .then((res) => {
      uni.hideLoading()
      
      // 注册成功
      uni.showToast({ title: '注册成功', icon: 'success' })
      
      // 清空表单
      formData.username = ''
      formData.email = ''
      formData.phone = ''
      formData.city = ''
      formData.password = ''
      formData.confirmPassword = ''
      agreed.value = false
      
      // 延迟2秒后跳转到登录页面
    
    // 跳转到登录页面
    setTimeout(() => {
      uni.navigateTo({
        url: '/pages/auth/login'
      })
    }, 1500)
  }, 2000)
}

// 返回按钮
const handleBack = () => {
  uni.navigateBack()
}

// 登录页面
const handleLogin = () => {
  uni.navigateTo({
    url: '/pages/auth/login'
  })
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

// 顶部导航栏
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 60rpx 40rpx 40rpx;
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
  
  .back-btn {
    width: 60rpx;
    height: 60rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    
    .back-icon {
      font-size: 32rpx;
      color: #fff;
    }
  }
  
  .header-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #fff;
  }
  
  .placeholder {
    width: 60rpx;
  }
}

// 注册表单
.register-form {
  padding: 60rpx 40rpx;
  
  // Logo区域
  .logo-section {
    text-align: center;
    margin-bottom: 80rpx;
    
    .logo-circle {
      width: 120rpx;
      height: 120rpx;
      background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 30rpx;
      box-shadow: 0 8rpx 32rpx rgba(74, 144, 226, 0.3);
      
      .logo-text {
        font-size: 60rpx;
      }
    }
    
    .app-name {
      font-size: 40rpx;
      font-weight: bold;
      color: #333;
      margin-bottom: 10rpx;
    }
    
    .app-slogan {
      font-size: 26rpx;
      color: #666;
    }
  }
  
  // 表单区域
  .form-section {
    background: #fff;
    border-radius: 24rpx;
    padding: 40rpx;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
    margin-bottom: 40rpx;
    
    // 输入组
    .input-group {
      margin-bottom: 40rpx;
      
      .input-label {
        display: block;
        font-size: 28rpx;
        font-weight: 500;
        color: #333;
        margin-bottom: 15rpx;
      }
      
      .input-container {
        position: relative;
        display: flex;
        align-items: center;
        border: 2rpx solid #e1e8ed;
        border-radius: 16rpx;
        padding: 0 30rpx;
        transition: all 0.3s ease;
        
        &:focus-within {
          border-color: #4a90e2;
          box-shadow: 0 0 0 6rpx rgba(74, 144, 226, 0.1);
        }
        
        .input-icon {
          font-size: 32rpx;
          margin-right: 20rpx;
          color: #666;
        }
        
        .input-field {
          flex: 1;
          height: 90rpx;
          font-size: 28rpx;
          color: #333;
          border: none;
          outline: none;
          background: transparent;
        }
        
        .toggle-password {
          font-size: 32rpx;
          color: #666;
          padding: 10rpx;
        }
        
        .picker-field {
          flex: 1;
          height: 90rpx;
          display: flex;
          align-items: center;
          font-size: 28rpx;
          color: #333;
          
          &.placeholder {
            color: #999;
          }
        }
      }
      
      .error-text {
        display: block;
        font-size: 24rpx;
        color: #ff4757;
        margin-top: 10rpx;
      }
    }
    
    // 协议区域
    .agreement-section {
      margin-bottom: 50rpx;
      
      .agreement-label {
        display: flex;
        align-items: flex-start;
        
        .agreement-checkbox {
          margin-right: 15rpx;
          margin-top: 5rpx;
        }
        
        .agreement-text {
          font-size: 26rpx;
          color: #666;
          line-height: 1.5;
          
          .agreement-link {
            color: #4a90e2;
            text-decoration: none;
          }
        }
      }
    }
    
    // 注册按钮
    .register-btn {
      width: 100%;
      height: 90rpx;
      background: linear-gradient(135deg, #e1e8ed 0%, #d1d9e0 100%);
      color: #999;
      border: none;
      border-radius: 45rpx;
      font-size: 32rpx;
      font-weight: bold;
      transition: all 0.3s ease;
      
      &.active {
        background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
        color: #fff;
        transform: translateY(0);
        
        &:active {
          transform: translateY(2rpx);
          box-shadow: 0 4rpx 16rpx rgba(74, 144, 226, 0.3);
        }
      }
      
      &:disabled {
        opacity: 0.6;
      }
    }
  }
  
  // 登录链接
  .login-link {
    text-align: center;
    
    .login-text {
      font-size: 26rpx;
      color: #666;
      margin-right: 10rpx;
    }
    
    .login-btn {
      font-size: 26rpx;
      color: #4a90e2;
      font-weight: bold;
    }
  }
}
</style>
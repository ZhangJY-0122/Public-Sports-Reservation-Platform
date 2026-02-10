<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="header">
      <view class="back-btn" @click="handleBack">
        <text class="back-icon">←</text>
      </view>
      <text class="header-title">用户登录</text>
      <view class="placeholder"></view>
    </view>

    <!-- 登录表单 -->
    <view class="login-form">
      <!-- Logo区域 -->
      <view class="logo-section">
        <view class="logo-circle">
          <text class="logo-text">🏟️</text>
        </view>
        <text class="app-name">体育预约</text>
        <text class="app-slogan">欢迎回来，继续您的运动之旅</text>
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
              placeholder="请输入用户名或邮箱"
              class="input-field"
              v-model="formData.username"
              @blur="validateField('username')"
            />
          </view>
          <text class="error-text" v-if="errors.username">{{ errors.username }}</text>
        </view>

        <!-- 密码 -->
        <view class="input-group">
          <text class="input-label">密码</text>
          <view class="input-container">
            <text class="input-icon">🔒</text>
            <input 
              :type="showPassword ? 'text' : 'password'" 
              placeholder="请输入密码"
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

        <!-- 记住密码和忘记密码 -->
        <view class="login-options">
          <view class="remember-section">
            <checkbox-group @change="onRememberChange">
              <label class="remember-label">
                <checkbox 
                  :checked="rememberMe" 
                  color="#4a90e2"
                  class="remember-checkbox"
                />
                <text class="remember-text">记住密码</text>
              </label>
            </checkbox-group>
          </view>
          <text class="forgot-password" @click="handleForgotPassword">忘记密码？</text>
        </view>

        <!-- 登录按钮 -->
        <button 
          class="login-btn" 
          :class="{ active: canLogin }"
          :disabled="!canLogin"
          @click="handleLogin"
        >
          立即登录
        </button>
      </view>

      <!-- 第三方登录 -->
    <!--  <view class="third-party-section">
        <view class="divider">
          <text class="divider-text">或使用以下方式登录</text>
        </view>
        
        <view class="third-party-buttons">
          <view class="third-party-btn wechat-btn" @click="handleWechatLogin">
            <text class="third-party-icon">💬</text>
            <text class="third-party-text">微信登录</text>
          </view>
          
          <view class="third-party-btn qq-btn" @click="handleQqLogin">
            <text class="third-party-icon">🐧</text>
            <text class="third-party-text">QQ登录</text>
          </view>
        </view>
      </view> -->

      <!-- 注册链接 -->
      <view class="register-link">
        <text class="register-text">还没有账号？</text>
        <text class="register-btn" @click="handleRegister">立即注册</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { authAPI } from '@/api/services.js'

import {onShow,onLoad,onReady} from '@dcloudio/uni-app'

// 表单数据
const formData = reactive({
  username: '',
  password: ''
})

// 错误信息
const errors = reactive({
  username: '',
  password: ''
})

// 显示密码
const showPassword = ref(false)
const rememberMe = ref(false)

// 能否登录
const canLogin = computed(() => {
  return (
    formData.username.trim() &&
    formData.password.trim() &&
    !errors.username &&
    !errors.password
  )
})

// 切换密码显示
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

// 记住密码
const onRememberChange = (e) => {
  rememberMe.value = e.detail.value.length > 0
}

// 字段验证
const validateField = (field) => {
  const value = formData[field]
  
  switch (field) {
    case 'username':
      if (!value.trim()) {
        errors.username = '请输入用户名或邮箱'
      } else if (value.includes('@')) {
        // 邮箱验证
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          errors.username = '邮箱格式不正确'
        } else {
          errors.username = ''
        }
      } else {
        // 用户名验证
        if (value.length < 3) {
          errors.username = '用户名至少3个字符'
        } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
          errors.username = '用户名只能包含字母、数字和下划线'
        } else {
          errors.username = ''
        }
      }
      break
      
    case 'password':
      if (!value.trim()) {
        errors.password = '请输入密码'
      } else if (value.length < 6) {
        errors.password = '密码至少6位'
      } else {
        errors.password = ''
      }
      break
  }
}

// 登录处理
const handleLogin = () => {
  if (!canLogin.value) return
  
  // 验证所有字段
  validateField('username')
  validateField('password')
  
  if (errors.username || errors.password) {
    return
  }
  
  // 登录请求
  uni.showLoading({ title: '登录中...' })
  
  authAPI.login(formData).then(res => {
    // 登录成功
    console.log('登录成功:', res)
	
    uni.setStorageSync("user",res)
    // 保存token和用户信息
    if (res.token) {
      uni.setStorageSync('token', res.token)
    }
    if (res.user) {
      uni.setStorageSync('userInfo', res.user)
    }
    
    uni.showToast({
      title: '登录成功！',
      icon: 'success'
    })
    
    // 跳转到首页
    setTimeout(() => {
      uni.switchTab({
        url: '/pages/index/index'
      })
    }, 1500)
  }).catch(err => {
    // 登录失败
    console.error('登录失败:', err)
    uni.showToast({
      title: err.msg || '登录失败，请重试',
      icon: 'none'
    })
  }).finally(() => {
    uni.hideLoading()
  })
  
  
  

}

// 忘记密码
const handleForgotPassword = () => {
  uni.showToast({
    title: '请联系客服重置密码',
    icon: 'none'
  })
}

// 微信登录
const handleWechatLogin = () => {
  uni.showToast({
    title: '微信登录功能开发中',
    icon: 'none'
  })
}

// QQ登录
const handleQqLogin = () => {
  uni.showToast({
    title: 'QQ登录功能开发中',
    icon: 'none'
  })
}

// 返回按钮
const handleBack = () => {
  uni.navigateBack()
}

// 注册页面
const handleRegister = () => {
  uni.navigateTo({
    url: '/pages/auth/register'
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

// 登录表单
.login-form {
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
      }
      
      .error-text {
        display: block;
        font-size: 24rpx;
        color: #ff4757;
        margin-top: 10rpx;
      }
    }
    
    // 登录选项
    .login-options {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 50rpx;
      
      .remember-section {
        .remember-label {
          display: flex;
          align-items: center;
          
          .remember-checkbox {
            margin-right: 10rpx;
          }
          
          .remember-text {
            font-size: 26rpx;
            color: #666;
          }
        }
      }
      
      .forgot-password {
        font-size: 26rpx;
        color: #4a90e2;
      }
    }
    
    // 登录按钮
    .login-btn {
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
  
  // 第三方登录
  .third-party-section {
    margin-bottom: 40rpx;
    
    .divider {
      position: relative;
      text-align: center;
      margin-bottom: 40rpx;
      
      &::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 2rpx;
        background: #e1e8ed;
      }
      
      .divider-text {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 0 30rpx;
        font-size: 26rpx;
        color: #999;
      }
    }
    
    .third-party-buttons {
      display: flex;
      gap: 30rpx;
      
      .third-party-btn {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 30rpx;
        background: #fff;
        border-radius: 16rpx;
        border: 2rpx solid #e1e8ed;
        transition: all 0.3s ease;
        
        &:active {
          transform: translateY(2rpx);
          border-color: #4a90e2;
        }
        
        .third-party-icon {
          font-size: 48rpx;
          margin-bottom: 15rpx;
        }
        
        .third-party-text {
          font-size: 26rpx;
          color: #666;
        }
        
        &.wechat-btn {
          &:active {
            border-color: #09bb07;
          }
        }
        
        &.qq-btn {
          &:active {
            border-color: #12b7f5;
          }
        }
      }
    }
  }
  
  // 注册链接
  .register-link {
    text-align: center;
    
    .register-text {
      font-size: 26rpx;
      color: #666;
      margin-right: 10rpx;
    }
    
    .register-btn {
      font-size: 26rpx;
      color: #4a90e2;
      font-weight: bold;
    }
  }
}
</style>
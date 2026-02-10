<template>
  <view class="event-page">
    <!-- 页面标题 -->
    <view class="header">
      <text class="title">赛事详情</text>
      <text class="subtitle">查看赛事信息并参与比赛</text>
    </view>
    
    <!-- 赛事基本信息 -->
    <view class="section">
      <text class="section-title">赛事信息</text>
      <view class="event-card">
        <!-- 赛事图片 -->
        <view class="event-image-container">
          <image 
            :src="eventDetail.image || '/static/banner/1.jpg'" 
            mode="aspectFill"
            class="event-image"
            @click="previewImage(eventDetail.image)"
          />
          <view class="event-type-badge">{{ eventDetail.event_type }}</view>
          <view class="status-badge" :class="eventDetail.status">
            {{ getStatusText(eventDetail.status) }}
          </view>
        </view>
        
        <!-- 赛事基本信息 -->
        <view class="event-basic-info">
          <view class="event-header">
            <text class="event-name">{{ eventDetail.name }}</text>
            <view class="event-price">
              <text class="price-label">报名费:</text>
              <text class="price-value">¥{{ eventDetail.registration_fee || 0 }}</text>
            </view>
          </view>
          
          <view class="event-description">
            <text>{{ eventDetail.description || '暂无描述' }}</text>
          </view>
          
          <!-- 赛事详情信息 -->
          <view class="event-details">
            <view class="detail-item">
              <text class="detail-icon">📅</text>
              <text class="detail-label">赛事日期:</text>
              <text class="detail-value">{{ formatDate(eventDetail.event_date) }}</text>
            </view>
            
            <view class="detail-item">
              <text class="detail-icon">⏰</text>
              <text class="detail-label">报名截止:</text>
              <text class="detail-value">{{ formatDate(eventDetail.registration_deadline) }}</text>
            </view>
            
            <view class="detail-item">
              <text class="detail-icon">📍</text>
              <text class="detail-label">比赛地点:</text>
              <text class="detail-value">{{ eventDetail.location }}</text>
            </view>
            
            <view class="detail-item">
              <text class="detail-icon">👥</text>
              <text class="detail-label">参赛人数:</text>
              <text class="detail-value">{{ eventDetail.current_participants }}/{{ eventDetail.max_participants }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 报名统计 -->
    <view class="section" v-if="registrationStats">
      <text class="section-title">报名统计</text>
      <view class="stats-card">
        <view class="stats-item">
          <text class="stats-number">{{ registrationStats.total_registrations }}</text>
          <text class="stats-label">总报名</text>
        </view>
        <view class="stats-item">
          <text class="stats-number approved">{{ registrationStats.approved }}</text>
          <text class="stats-label">已通过</text>
        </view>
        <view class="stats-item">
          <text class="stats-number pending">{{ registrationStats.pending }}</text>
          <text class="stats-label">审核中</text>
        </view>
        <view class="stats-item">
          <text class="stats-number rejected">{{ registrationStats.rejected }}</text>
          <text class="stats-label">已拒绝</text>
        </view>
      </view>
    </view>

    <!-- 赛事规则 -->
    <view class="section">
      <text class="section-title">赛事规则</text>
      <view class="rules-card">
        <view class="rule-item" v-for="(rule, index) in eventRules" :key="index">
          <text class="rule-number">{{ index + 1 }}</text>
          <text class="rule-content">{{ rule }}</text>
        </view>
      </view>
    </view>

    <!-- 参与按钮 -->
    <view class="action-section">
      <view class="action-card">
        <view class="participation-info">
          <text class="info-title">参与赛事</text>
          <text class="info-desc">点击下方按钮立即报名参加赛事</text>
        </view>
        
        <button 
          class="participate-btn"
          @click="participateEvent"
        >
          立即报名
        </button>
      </view>
    </view>

    <!-- 参与确认模态框 -->
    <view class="modal-overlay" v-if="showConfirmModal" @click="hideConfirmModal">
      <view class="modal-content" @click.stop>
        <view class="modal-header">
          <text class="modal-title">确认报名</text>
          <text class="modal-close" @click="hideConfirmModal">×</text>
        </view>
        
        <view class="modal-body">
          <view class="confirm-info">
            <text class="confirm-title">{{ eventDetail.name }}</text>
            <view class="confirm-item">
              <text class="confirm-label">赛事日期:</text>
              <text class="confirm-value">{{ formatDate(eventDetail.event_date) }}</text>
            </view>
            <view class="confirm-item">
              <text class="confirm-label">比赛地点:</text>
              <text class="confirm-value">{{ eventDetail.location }}</text>
            </view>
            <view class="confirm-item">
              <text class="confirm-label">报名费用:</text>
              <text class="confirm-value">¥{{ eventDetail.registration_fee || 0 }}</text>
            </view>
            <view class="confirm-item">
              <text class="confirm-label">参赛人数:</text>
              <text class="confirm-value">{{ eventDetail.current_participants }}/{{ eventDetail.max_participants }}</text>
            </view>
          </view>
          
          <!-- 联系方式 -->
          <view class="contact-section">
            <text class="contact-title">联系方式</text>
            <input 
              v-model="registrationForm.contact_info"
              class="contact-input"
              placeholder="请输入联系电话"
            />
            <textarea 
              v-model="registrationForm.additional_info"
              class="contact-textarea"
              placeholder="其他需要说明的信息（可选）"
            ></textarea>
          </view>
        </view>
        
        <view class="modal-actions">
          <view class="modal-button cancel" @click="hideConfirmModal">取消</view>
          <view class="modal-button confirm" @click="confirmRegistration">确认报名</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { http, BaseUrl } from '@/utils/http.js'

export default {
  data() {
    return {
      eventId: null,
      eventDetail: {},
      registrationStats: null,
      showConfirmModal: false,
      loading: false,
      registrationForm: {
        contact_info: '',
        additional_info: ''
      },
      eventRules: [
        '参赛者需身体健康，无重大疾病',
        '比赛期间请遵守现场秩序和规则',
        '提前30分钟到场进行签到和热身',
        '自备运动装备，场馆提供基本器材',
        '如遇特殊情况无法参赛，请提前2天通知',
        '主办方保留最终解释权和调整权'
      ]
    }
  },



  onLoad(options) {
    this.eventId = options.id || options.eventId
    if (this.eventId) {
      this.loadEventDetail()
    }
  },

  methods: {
    // 加载赛事详情
    async loadEventDetail() {
      try {
        this.loading = true
        const response = await http.get(`/events/${this.eventId}`)
        
         this.eventDetail=response.event
      } catch (error) {
        console.error('加载赛事详情失败:', error)
        uni.showToast({
          title: '网络错误，请重试',
          icon: 'none'
        })
      } finally {
        this.loading = false
      }
    },

    // 格式化日期
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}年${month}月${day}日`
    },

    // 获取状态文本
    getStatusText(status) {
      const statusMap = {
        'upcoming': '即将开始',
        'ongoing': '进行中',
        'completed': '已结束',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    },

    // 参与赛事
    participateEvent() {
      this.showConfirmModal = true
    },

    // 隐藏确认模态框
    hideConfirmModal() {
      this.showConfirmModal = false
      this.registrationForm = {
        contact_info: '',
        additional_info: ''
      }
    },

    // 确认报名
    async confirmRegistration() {
      if (!this.registrationForm.contact_info.trim()) {
        uni.showToast({
          title: '请输入联系电话',
          icon: 'none'
        })
        return
      }
	  
	  let user=uni.getStorageSync("user")

      try {
        this.loading = true
        const response = await http.post(`/events/${this.eventId}/register`, {
		 user_name:user.username,
          contact: this.registrationForm.contact_info,
          notes: this.registrationForm.additional_info
        })
   this.hideConfirmModal()
       uni.showToast({
         title: '报名成功！',
         icon: 'success'
       })
    
      } catch (error) {
        this.hideConfirmModal()
            uni.showToast({
              title: '报名失败！',
              icon: 'success'
            })
      } finally {
        this.loading = false
      }
    },

    // 预览图片
    previewImage(imageUrl) {
      if (!imageUrl) return
      uni.previewImage({
        urls: [imageUrl]
      })
    }
  }
}
</script>

<style scoped>
.event-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20rpx;
}

.header {
  text-align: center;
  margin-bottom: 40rpx;
}

.title {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: white;
  margin-bottom: 16rpx;
}

.subtitle {
  display: block;
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
}

.section {
  margin-bottom: 40rpx;
}

.section-title {
  display: block;
  font-size: 32rpx;
  font-weight: 600;
  color: white;
  margin-bottom: 24rpx;
  padding-left: 20rpx;
  border-left: 8rpx solid #ffd700;
}

.event-card {
  background: white;
  border-radius: 24rpx;
  overflow: hidden;
  box-shadow: 0 16rpx 40rpx rgba(0, 0, 0, 0.1);
}

.event-image-container {
  position: relative;
  height: 400rpx;
  overflow: hidden;
}

.event-image {
  width: 100%;
  height: 100%;
}

.event-type-badge {
  position: absolute;
  top: 24rpx;
  left: 24rpx;
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
  padding: 12rpx 24rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
  font-weight: 600;
}

.status-badge {
  position: absolute;
  top: 24rpx;
  right: 24rpx;
  padding: 12rpx 24rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
  font-weight: 600;
  color: white;
}

.status-badge.upcoming {
  background: linear-gradient(45deg, #4facfe, #00f2fe);
}

.status-badge.ongoing {
  background: linear-gradient(45deg, #43e97b, #38f9d7);
}

.status-badge.completed {
  background: linear-gradient(45deg, #667eea, #764ba2);
}

.status-badge.cancelled {
  background: linear-gradient(45deg, #ff6b6b, #ee5a52);
}

.event-basic-info {
  padding: 32rpx;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24rpx;
}

.event-name {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  flex: 1;
  margin-right: 24rpx;
}

.event-price {
  text-align: right;
}

.price-label {
  display: block;
  font-size: 24rpx;
  color: #666;
  margin-bottom: 8rpx;
}

.price-value {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  color: #ff6b6b;
}

.event-description {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 32rpx;
  padding: 24rpx;
  background: #f8f9fa;
  border-radius: 16rpx;
}

.event-details {
  gap: 24rpx;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;
  padding: 20rpx;
  background: #f8f9fa;
  border-radius: 16rpx;
  transition: all 0.3s ease;
}

.detail-item:hover {
  background: #e9ecef;
}

.detail-icon {
  font-size: 32rpx;
  margin-right: 20rpx;
  width: 40rpx;
  text-align: center;
}

.detail-label {
  font-size: 28rpx;
  color: #666;
  margin-right: 16rpx;
  min-width: 120rpx;
}

.detail-value {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
  flex: 1;
}

.stats-card {
  background: white;
  border-radius: 24rpx;
  padding: 40rpx;
  display: flex;
  justify-content: space-around;
  box-shadow: 0 16rpx 40rpx rgba(0, 0, 0, 0.1);
}

.stats-item {
  text-align: center;
}

.stats-number {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 12rpx;
}

.stats-number.approved {
  color: #43e97b;
}

.stats-number.pending {
  color: #ffa726;
}

.stats-number.rejected {
  color: #ff6b6b;
}

.stats-label {
  display: block;
  font-size: 24rpx;
  color: #666;
}

.rules-card {
  background: white;
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: 0 16rpx 40rpx rgba(0, 0, 0, 0.1);
}

.rule-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 24rpx;
  padding: 20rpx;
  background: #f8f9fa;
  border-radius: 16rpx;
}

.rule-number {
  background: #667eea;
  color: white;
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.rule-content {
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
  flex: 1;
}

.action-section {
  margin-top: 60rpx;
}

.action-card {
  background: white;
  border-radius: 24rpx;
  padding: 40rpx;
  box-shadow: 0 16rpx 40rpx rgba(0, 0, 0, 0.1);
}

.participation-info {
  margin-bottom: 32rpx;
}

.info-title {
  display: block;
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 16rpx;
}

.info-desc {
  display: block;
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.info-desc.warning {
  color: #ff6b6b;
}

.participate-btn {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 44rpx;
  font-size: 32rpx;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.3);
}

.participate-btn:active {
  transform: translateY(2rpx);
  box-shadow: 0 4rpx 12rpx rgba(102, 126, 234, 0.3);
}

.participate-btn.disabled {
  background: #ccc;
  box-shadow: none;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 40rpx;
}

.modal-content {
  background: white;
  border-radius: 24rpx;
  width: 100%;
  max-width: 600rpx;
  max-height: 80vh;
  overflow: hidden;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(100rpx);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx 40rpx;
  border-bottom: 2rpx solid #f0f0f0;
}

.modal-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.modal-close {
  font-size: 48rpx;
  color: #999;
  line-height: 1;
}

.modal-body {
  padding: 40rpx;
  max-height: 50vh;
  overflow-y: auto;
}

.confirm-info {
  margin-bottom: 32rpx;
}

.confirm-title {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
}

.confirm-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
  padding: 16rpx 0;
}

.confirm-label {
  font-size: 28rpx;
  color: #666;
}

.confirm-value {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.contact-section {
  margin-top: 32rpx;
}

.contact-title {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
}

.contact-input {
  width: 100%;
  height: 80rpx;
  border: 2rpx solid #e0e0e0;
  border-radius: 16rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
  background: #f8f9fa;
  margin-bottom: 24rpx;
}

.contact-textarea {
  width: 100%;
  height: 120rpx;
  border: 2rpx solid #e0e0e0;
  border-radius: 16rpx;
  padding: 24rpx;
  font-size: 28rpx;
  background: #f8f9fa;
  resize: none;
}

.modal-actions {
  display: flex;
  padding: 32rpx 40rpx;
  border-top: 2rpx solid #f0f0f0;
  gap: 24rpx;
}

.modal-button {
  flex: 1;
  height: 80rpx;
  border-radius: 40rpx;
  font-size: 28rpx;
  font-weight: 600;
  text-align: center;
  line-height: 80rpx;
  transition: all 0.3s ease;
}

.modal-button.cancel {
  background: #f5f5f5;
  color: #666;
}

.modal-button.cancel:active {
  background: #e0e0e0;
}

.modal-button.confirm {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
}

.modal-button.confirm:active {
  transform: translateY(2rpx);
}

@media (max-width: 750rpx) {
  .event-page {
    padding: 16rpx;
  }
  
  .header {
    margin-bottom: 32rpx;
  }
  
  .title {
    font-size: 40rpx;
  }
  
  .event-image-container {
    height: 300rpx;
  }
  
  .event-basic-info {
    padding: 24rpx;
  }
  
  .event-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .event-name {
    margin-right: 0;
    margin-bottom: 16rpx;
  }
  
  .stats-card {
    padding: 24rpx;
  }
  
  .stats-number {
    font-size: 40rpx;
  }
  
  .modal-content {
    margin: 20rpx;
  }
}
</style>
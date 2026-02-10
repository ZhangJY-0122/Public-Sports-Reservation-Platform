<template>
  <view class="coach-detail-page">
    <!-- 顶部导航栏 -->
    <view class="nav-bar">
      <view class="nav-content">
        <view class="back-btn" @click="goBack">
          <text class="back-icon">←</text>
        </view>
        <text class="nav-title">教练详情</text>
        <view class="nav-actions">
          <text class="share-btn" @click="shareCoach">📤</text>
        </view>
      </view>
    </view>

    <scroll-view class="detail-container" scroll-y>
      <!-- 教练基本信息 -->
      <view class="coach-header-section">
        <view class="coach-avatar-section">
          <image 
            :src="coachDetail.avatar || '/static/nav/n1.png'" 
            mode="aspectFill" 
            class="coach-avatar" 
          />
          <view v-if="coachDetail.is_active" class="status-badge available">可预约</view>
          <view v-else class="status-badge unavailable">暂停服务</view>
        </view>
        
        <view class="coach-basic-info">
          <view class="coach-name">{{ coachDetail.name }}</view>
          <view class="coach-specialization">{{ coachDetail.specialization }}</view>
          <view class="coach-rating-section">
            <view class="stars">
              <text 
                v-for="n in 5" 
                :key="n"
                class="star"
                :class="{ filled: n <= Math.floor(coachDetail.rating || 0) }"
              >⭐</text>
            </view>
            <text class="rating-text">{{ coachDetail.rating || 0 }}分</text>
            <text class="rating-count">({{ coachDetail.booking_stats?.total_bookings || 0 }}次预约)</text>
          </view>
          <view class="coach-price">
            <text class="price-label">时薪：</text>
            <text class="price-value">¥{{ coachDetail.hourly_rate || 0 }}</text>
          </view>
        </view>
      </view>

      <!-- 教练介绍 -->
      <view class="info-section" v-if="coachDetail.bio">
        <text class="section-title">教练介绍</text>
        <view class="info-content">
          <text class="bio-text">{{ coachDetail.bio }}</text>
        </view>
      </view>

      <!-- 专业资质 -->
      <view class="info-section" v-if="coachDetail.certifications && coachDetail.certifications.length">
        <text class="section-title">专业资质</text>
        <view class="certifications-list">
          <view 
            v-for="cert in coachDetail.certifications" 
            :key="cert"
            class="cert-item"
          >
            <text class="cert-icon">🏆</text>
            <text class="cert-text">{{ cert }}</text>
          </view>
        </view>
      </view>

      <!-- 教学特色 -->
      <view class="info-section" v-if="coachDetail.tags && coachDetail.length">
        <text class="section-title">教学特色</text>
        <view class="tags-list">
          <view 
            v-for="tag in coachDetail.tags" 
            :key="tag"
            class="tag"
          >{{ tag }}
        </view>
		</view>
      </view>

      <!-- 预约统计 -->
      <view class="info-section">
        <text class="section-title">预约统计</text>
        <view class="stats-grid">
          <view class="stat-item">
            <text class="stat-number">{{ coachDetail.booking_stats?.total_bookings || 0 }}</text>
            <text class="stat-label">总预约</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">{{ coachDetail.booking_stats?.upcoming || 0 }}</text>
            <text class="stat-label">待进行</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">{{ coachDetail.booking_stats?.completed || 0 }}</text>
            <text class="stat-label">已完成</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">{{ coachDetail.booking_stats?.cancelled || 0 }}</text>
            <text class="stat-label">已取消</text>
          </view>
        </view>
      </view>

      <!-- 用户评价 -->
      <view class="info-section">
        <text class="section-title">用户评价</text>
        <view class="reviews-summary">
          <view class="rating-overview">
            <text class="overall-rating">{{ coachDetail.rating || 0 }}</text>
            <text class="rating-unit">分</text>
            <view class="stars">
              <text 
                v-for="n in 5" 
                :key="n"
                class="star"
                :class="{ filled: n <= Math.floor(coachDetail.rating || 0) }"
              >⭐</text>
            </view>
          </view>
          <text class="review-count">{{ coachDetail.booking_stats?.completed || 0 }}条评价</text>
        </view>
      </view>

      <!-- 可预约时间 -->
      <view class="info-section">
        <text class="section-title">可预约时间</text>
        <view class="time-info">
          <view class="time-item">
            <text class="time-label">营业时间：</text>
            <text class="time-value">08:00 - 22:00</text>
          </view>
          <view class="time-item">
            <text class="time-label">预约时长：</text>
            <text class="time-value">60分钟/课时</text>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- 底部预约栏 -->
    <view class="booking-bar">
      <view class="contact-info">
        <text class="contact-label">咨询了解</text>
        <text class="contact-phone">400-123-4567</text>
      </view>
      <view 
        class="booking-btn"
        :class="{ disabled: !coachDetail.is_active }"
        @click="startBooking"
      >
        <text class="btn-text">立即预约</text>
      </view>
    </view>

    <!-- 预约模态框 -->
    <view v-if="showBookingModal" class="modal-overlay" @click="closeBookingModal">
      <view class="booking-modal" @click.stop>
        <view class="modal-header">
          <text class="modal-title">开始预约</text>
          <text class="modal-close" @click="closeBookingModal">×</text>
        </view>
        
        <view class="modal-content">
          <view class="booking-options">
            <view 
              class="booking-option"
              :class="{ active: bookingType === 'single' }"
              @click="selectBookingType('single')"
            >
              <view class="option-icon">⏰</view>
              <view class="option-info">
                <text class="option-title">单次预约</text>
                <text class="option-desc">按小时收费，灵活便捷</text>
              </view>
              <view class="option-price">
                <text class="price">¥{{ coachDetail.hourly_rate }}/小时</text>
              </view>
            </view>
            
            <view 
              class="booking-option"
              :class="{ active: bookingType === 'package' }"
              @click="selectBookingType('package')"
            >
              <view class="option-icon">📅</view>
              <view class="option-info">
                <text class="option-title">套餐预约</text>
                <text class="option-desc">10小时套餐，享受优惠价格</text>
              </view>
              <view class="option-price">
                <text class="price">¥{{ Math.round((coachDetail.hourly_rate || 0) * 10 * 0.9) }}/10小时</text>
              </view>
            </view>
          </view>
          
          <view class="next-step-hint">
            <text class="hint-text">点击"下一步"选择具体时间和地点</text>
          </view>
        </view>
        
        <view class="modal-actions">
          <view class="cancel-btn" @click="closeBookingModal">取消</view>
          <view class="confirm-btn" @click="proceedToBooking">下一步</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
	import { http } from '@/utils/http.js'
export default {
  name: 'CoachDetail',
  data() {
    return {
      coachId: null,
      coachDetail: {},
      loading: false,
      showBookingModal: false,
      bookingType: 'single'
    }
  },
  
  onLoad(options) {
    this.coachId = options.id;
    if (this.coachId) {
      this.loadCoachDetail();
    }
  },
  
  methods: {
    async loadCoachDetail() {
       var  res=await http.get("coaches/"+this.coachId)
	   this.coachDetail=res
    },
    
    selectBookingType(type) {
      this.bookingType = type;
    },
    
    startBooking() {
      // if (!this.coachDetail.is_active) {
      //   uni.showToast({
      //     title: '该教练暂停服务',
      //     icon: 'none'
      //   });
      //   return;
      // }
	  
	  uni.setStorageSync("coacher",this.coachDetail)
	  
      this.showBookingModal = true;
    },
    
    closeBookingModal() {
      this.showBookingModal = false;
    },
    
    proceedToBooking() {
      this.closeBookingModal();
      
      // 跳转到预约页面
      uni.navigateTo({
        url: `/pages/coach/coach_booking?coachId=${this.coachId}&type=${this.bookingType}`
      });
    },
    
    shareCoach() {
      uni.showShareMenu({
        title: `推荐教练：${this.coachDetail.name}`,
        path: `/pages/coach/coach_detail?id=${this.coachId}`,
        imageUrl: this.coachDetail.avatar
      });
    },
    
    goBack() {
      uni.navigateBack();
    }
  }
}
</script>

<style scoped>
.coach-detail-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
}

.nav-bar {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 20px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.back-btn {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
}

.nav-title {
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.share-btn {
  font-size: 20px;
}

.detail-container {
  flex: 1;
  padding: 20px;
}

.coach-header-section {
  background: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.coach-avatar-section {
  position: relative;
}

.coach-avatar {
  width: 80px;
  height: 80px;
  border-radius: 40px;
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.status-badge {
  position: absolute;
  bottom: -5px;
  right: -5px;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.available {
  background: #4CAF50;
  color: white;
}

.status-badge.unavailable {
  background: #FF5722;
  color: white;
}

.coach-basic-info {
  flex: 1;
}

.coach-name {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.coach-specialization {
  font-size: 16px;
  color: #667eea;
  margin-bottom: 12px;
}

.coach-rating-section {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 14px;
  color: #ddd;
}

.star.filled {
  color: #FFD700;
}

.rating-text {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.rating-count {
  font-size: 12px;
  color: #999;
}

.coach-price {
  display: flex;
  align-items: center;
  gap: 5px;
}

.price-label {
  font-size: 14px;
  color: #666;
}

.price-value {
  font-size: 18px;
  font-weight: bold;
  color: #ff6b6b;
}

.info-section {
  background: white;
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
  display: block;
}

.info-content {
  line-height: 1.6;
}

.bio-text {
  font-size: 16px;
  color: #666;
  line-height: 1.8;
}

.certifications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cert-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 12px;
}

.cert-icon {
  font-size: 20px;
}

.cert-text {
  font-size: 14px;
  color: #333;
}

.tags-list {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.stat-item {
  text-align: center;
  padding: 20px 10px;
  background: #f8f9fa;
  border-radius: 15px;
}

.stat-number {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.reviews-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.rating-overview {
  display: flex;
  align-items: center;
  gap: 10px;
}

.overall-rating {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
}

.rating-unit {
  font-size: 16px;
  color: #667eea;
  margin-right: 10px;
}

.review-count {
  font-size: 14px;
  color: #999;
}

.time-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.time-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.time-label {
  font-size: 14px;
  color: #666;
  min-width: 80px;
}

.time-value {
  font-size: 14px;
  color: #333;
}

.booking-bar {
  background: white;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
}

.contact-info {
  flex: 1;
}

.contact-label {
  font-size: 12px;
  color: #999;
  display: block;
  margin-bottom: 4px;
}

.contact-phone {
  font-size: 16px;
  color: #667eea;
  font-weight: bold;
}

.booking-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: bold;
}

.booking-btn.disabled {
  background: #ccc;
  color: #999;
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
}

.booking-modal {
  background: white;
  border-radius: 20px;
  margin: 20px;
  max-width: 400px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.modal-close {
  font-size: 24px;
  color: #999;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  padding: 20px;
}

.booking-options {
  margin-bottom: 20px;
}

.booking-option {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  margin-bottom: 15px;
  transition: all 0.3s;
}

.booking-option.active {
  border-color: #667eea;
  background: #f0f4ff;
}

.option-icon {
  font-size: 24px;
}

.option-info {
  flex: 1;
}

.option-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 4px;
}

.option-desc {
  font-size: 12px;
  color: #999;
}

.option-price {
  text-align: right;
}

.price {
  font-size: 16px;
  font-weight: bold;
  color: #ff6b6b;
}

.next-step-hint {
  text-align: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 10px;
}

.hint-text {
  font-size: 14px;
  color: #666;
}

.modal-actions {
  display: flex;
  padding: 20px;
  border-top: 1px solid #eee;
  gap: 15px;
}

.cancel-btn, .confirm-btn {
  flex: 1;
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  font-size: 16px;
}

.cancel-btn {
  background: #f8f9fa;
  color: #666;
}

.confirm-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
</style>
<template>
  <view class="coach-payment-page">
    <!-- 顶部导航栏 -->
    <view class="nav-bar">
      <view class="nav-content">
        <view class="back-btn" @click="goBack">
          <text class="back-icon">←</text>
        </view>
        <text class="nav-title">确认支付</text>
        <view class="nav-actions"></view>
      </view>
    </view>

    <scroll-view class="payment-container" scroll-y>
      <!-- 订单信息 -->
      <view class="order-section">
        <text class="section-title">预约信息</text>
        <view class="order-info">
          <!-- 教练信息 -->
          <view class="coach-info">
            <image 
              :src="bookingData.coachDetail?.avatar || '/static/nav/n1.png'" 
              mode="aspectFill" 
              class="coach-avatar" 
            />
            <view class="coach-details">
              <view class="coach-name">{{ curr_coacher.name || '教练名称' }}</view>
              <view class="coach-specialization">{{ curr_coacher.introduction || '专业领域' }}</view>
              <view class="booking-type">{{ bookingData.bookingType === 'single' ? '单次预约' : '套餐预约' }}</view>
            </view>
          </view>
          
          <!-- 预约详情 -->
          <!-- <view class="booking-details">
            <view class="detail-item">
              <text class="detail-label">预约场地：</text>
              <text class="detail-value">{{ bookingData.facility?.name || '未选择' }}</text>
            </view>
            <view class="detail-item" v-if="bookingData.date">
              <text class="detail-label">预约日期：</text>
              <text class="detail-value">{{ bookingData.date.date }}</text>
            </view>
            <view class="detail-item" v-if="bookingData.timeSlot">
              <text class="detail-label">预约时间：</text>
              <text class="detail-value">{{ bookingData.timeSlot.time }}</text>
            </view>
            <view class="detail-item" v-if="bookingData.bookingType === 'package' && bookingData.package">
              <text class="detail-label">套餐课时：</text>
              <text class="detail-value">{{ bookingData.package.hours }}小时</text>
            </view>
            <view class="detail-item" v-if="bookingData.note">
              <text class="detail-label">备注信息：</text>
              <text class="detail-value">{{ bookingData.note }}</text>
            </view>
          </view> -->
        </view>
      </view>

      <!-- 优惠券 -->
     <!-- <view class="payment-section">
        <text class="section-title">优惠券</text>
        <view class="coupon-selector" @click="showCouponModal">
          <view class="coupon-info">
            <text class="coupon-text">
              {{ selectedCoupon ? selectedCoupon.name : '选择优惠券' }}
            </text>
            <text class="coupon-discount" v-if="selectedCoupon">
              减¥{{ selectedCoupon.discount }}
            </text>
          </view>
          <text class="arrow-right">›</text>
        </view>
      </view> -->

      <!-- 支付方式 -->
      <view class="payment-section">
        <text class="section-title">支付方式</text>
        <view class="payment-methods">
          <view 
            v-for="method in paymentMethods" 
            :key="method.id"
            class="payment-method"
            :class="{ active: selectedPaymentMethod?.id === method.id }"
            @click="selectPaymentMethod(method)"
          >
            <view class="method-icon">
              <image :src="method.icon" mode="aspectFit" class="icon-image" />
            </view>
            <view class="method-info">
              <text class="method-name">{{ method.name }}</text>
              <text class="method-desc">{{ method.description }}</text>
            </view>
            <view class="method-check">
              <text class="check-icon" v-if="selectedPaymentMethod?.id === method.id">✓</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 费用明细 -->
      <view class="payment-section">
        <text class="section-title">费用明细</text>
        <view class="cost-breakdown">
          <view class="cost-item">
            <text class="cost-label">教练费用</text>
            <text class="cost-value">¥{{ bookingData.total_price }}</text>
          </view>
          <view class="cost-item" v-if="bookingData.facility">
            <text class="cost-label">场地费用</text>
            <text class="cost-value">¥{{ bookingData.facility.price_per_hour }}</text>
          </view>
          <view class="cost-item discount" v-if="selectedCoupon">
            <text class="cost-label">优惠券折扣</text>
            <text class="cost-value">-¥{{ selectedCoupon.discount }}</text>
          </view>
          <view class="cost-item discount" v-if="bookingData.bookingType === 'package' && bookingData.package">
            <text class="cost-label">套餐优惠</text>
            <text class="cost-value">-¥{{ bookingData.package.savings }}</text>
          </view>
          <view class="cost-divider"></view>
          <view class="cost-item total">
            <text class="cost-label">实付金额</text>
            <text class="cost-value total">¥{{ finalAmount }}</text>
          </view>
        </view>
      </view>

      <!-- 协议条款 -->
      <view class="agreement-section">
        <view class="agreement-item" @click="toggleAgreement">
          <text class="check-box" :class="{ checked: agreementAccepted }">
            {{ agreementAccepted ? '✓' : '' }}
          </text>
          <text class="agreement-text">
            我已阅读并同意
            <text class="link" @click.stop="showTerms">《服务条款》</text>
            和
            <text class="link" @click.stop="showPrivacy">《隐私政策》</text>
          </text>
        </view>
      </view>
    </scroll-view>

    <!-- 底部支付栏 -->
    <view class="payment-footer">
      <view class="amount-info">
        <text class="amount-label">实付：</text>
        <text class="amount-value">¥{{ bookingData.total_price  }}</text>
        <text class="original-amount" v-if="originalAmount > finalAmount">¥{{ originalAmount }}</text>
      </view>
      <view 
        class="pay-btn"
        :class="{ disabled: !canPay || processing }"
        @click="processPayment"
      >
        <text class="btn-text">
          {{ processing ? '处理中...' : '立即支付' }}
        </text>
      </view>
    </view>

    <!-- 优惠券选择弹窗 -->
    <view v-if="showCouponModal" class="modal-overlay" @click="closeCouponModal">
      <view class="coupon-modal" @click.stop>
        <view class="modal-header">
          <text class="modal-title">选择优惠券</text>
          <text class="modal-close" @click="closeCouponModal">×</text>
        </view>
        <view class="coupon-list">
          <view 
            class="coupon-item"
            :class="{ active: !selectedCoupon }"
            @click="selectCoupon(null)"
          >
            <view class="coupon-card">
              <view class="coupon-info">
                <text class="coupon-name">不使用优惠券</text>
                <text class="coupon-condition">适用于所有订单</text>
              </view>
            </view>
          </view>
          
          <view 
            v-for="coupon in availableCoupons" 
            :key="coupon.id"
            class="coupon-item"
            :class="{ active: selectedCoupon?.id === coupon.id, disabled: !coupon.usable }"
            @click="coupon.usable ? selectCoupon(coupon) : null"
          >
            <view class="coupon-card">
              <view class="coupon-amount">
                <text class="amount">¥{{ coupon.discount }}</text>
                <text class="condition">{{ coupon.condition }}</text>
              </view>
              <view class="coupon-info">
                <text class="coupon-name">{{ coupon.name }}</text>
                <text class="coupon-validity">有效期至：{{ coupon.expiry_date }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 支付成功弹窗 -->
    <view v-if="showSuccessModal" class="modal-overlay" @click="closeSuccessModal">
      <view class="success-modal" @click.stop>
        <view class="success-icon">
          <text class="success-check">✓</text>
        </view>
        <view class="success-title">支付成功！</view>
        <view class="success-message">您的预约已确认，请按时到达</view>
        <view class="success-actions">
          <view class="success-btn secondary" @click="viewBooking">
            <text>查看预约</text>
          </view>
          <view class="success-btn primary" @click="goHome">
            <text>返回首页</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
	import { http } from '@/utils/http.js'
export default {
  name: 'CoachPayment',
  data() {
    return {
      bookingData: {},
	  curr_coacher:{},
      selectedPaymentMethod: null,
      selectedCoupon: null,
      agreementAccepted: false,
      processing: false,
      showCouponModal: false,
      showSuccessModal: false,
      
      paymentMethods: [
        {
          id: 'wechat',
          name: '微信支付',
          description: '推荐使用，快速安全',
          icon: '/static/icons/wechat-pay.png'
        },
        {
          id: 'alipay',
          name: '支付宝',
          description: '支持花呗分期',
          icon: '/static/icons/alipay.png'
        },
        {
          id: 'unionpay',
          name: '银行卡',
          description: '储蓄卡/信用卡',
          icon: '/static/icons/unionpay.png'
        }
      ],
      
      availableCoupons: [
        {
          id: 1,
          name: '新人专享券',
          discount: 20,
          condition: '满100元可用',
          expiry_date: '2025-12-31',
          usable: true
        },
        {
          id: 2,
          name: '满减券',
          discount: 50,
          condition: '满300元可用',
          expiry_date: '2025-06-30',
          usable: true
        },
        {
          id: 3,
          name: 'VIP专享券',
          discount: 100,
          condition: '满500元可用',
          expiry_date: '2025-05-31',
          usable: true
        },
        {
          id: 4,
          name: '体验券',
          discount: 10,
          condition: '满50元可用',
          expiry_date: '2025-03-15',
          usable: false
        }
      ]
    }
  },
  
  computed: {
    originalCoachCost() {
      if (this.bookingData.bookingType === 'single') {
        return this.bookingData.coachDetail?.hourly_rate || 0;
      } else {
        return this.bookingData.package?.originalPrice || 0;
      }
    },
    
    facilityCost() {
      return this.bookingData.facility?.price_per_hour || 0;
    },
    
    originalAmount() {
      return this.originalCoachCost + this.facilityCost;
    },
    
    finalAmount() {
      let discount = 0;
      
      // 优惠券折扣
      if (this.selectedCoupon) {
        discount += this.selectedCoupon.discount;
      }
      
      // 套餐折扣
      if (this.bookingData.bookingType === 'package' && this.bookingData.package) {
        discount += this.bookingData.package.savings;
      }
      
      return Math.max(0, this.originalAmount - discount);
    },
    
    canPay() {
      return this.selectedPaymentMethod && this.agreementAccepted && !this.processing;
    }
  },
  
  onLoad(options) {
   
      this.bookingData = uni.getStorageSync("cur_order_coacher")
	  this.curr_coacher=uni.getStorageSync("coacher")
      
  
  },
  
  methods: {
    selectPaymentMethod(method) {
      this.selectedPaymentMethod = method;
    },
    
    selectCoupon(coupon) {
      this.selectedCoupon = coupon;
      this.showCouponModal = false;
    },
    
    toggleAgreement() {
      this.agreementAccepted = !this.agreementAccepted;
    },
    
    showCouponModal() {
      this.showCouponModal = true;
    },
    
    closeCouponModal() {
      this.showCouponModal = false;
    },
    
    closeSuccessModal() {
      this.showSuccessModal = false;
    },
    
    async processPayment() {
      if (!this.canPay) return;
      
	  this.bookingData.date=this.bookingData.booking_date
      this.processing = true;
      let res= await http.post(`coaches/${this.curr_coacher.coach.id}/book`,this.bookingData)
	  uni.showToast({
	  	"title":"预约成功"
	  })
    
    },
    
    viewBooking() {
      // 跳转到预约详情页
      uni.navigateTo({
        url: '/pages/coach/coach_bookings'
      });
    },
    
    goHome() {
      // 跳转到首页
      uni.switchTab({
        url: '/pages/index/index'
      });
    },
    
    showTerms() {
      uni.showToast({
        title: '服务条款',
        icon: 'none'
      });
    },
    
    showPrivacy() {
      uni.showToast({
        title: '隐私政策',
        icon: 'none'
      });
    },
    
    goBack() {
      uni.navigateBack();
    }
  }
}
</script>

<style scoped>
.coach-payment-page {
  min-height: 100vh;
  background: #f8f9fa;
  display: flex;
  flex-direction: column;
}

.nav-bar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  font-size: 18px;
  font-weight: bold;
  color: white;
}

.payment-container {
  flex: 1;
  padding: 20px;
  padding-bottom: 120px;
}

.order-section,
.payment-section {
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
  margin-bottom: 20px;
  display: block;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.coach-info {
  display: flex;
  align-items: center;
  gap: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.coach-avatar {
  width: 50px;
  height: 50px;
  border-radius: 25px;
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.coach-details {
  flex: 1;
}

.coach-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.coach-specialization {
  font-size: 12px;
  color: #667eea;
  margin-bottom: 5px;
}

.booking-type {
  font-size: 12px;
  color: #999;
}

.booking-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.detail-label {
  font-size: 14px;
  color: #666;
  min-width: 80px;
}

.detail-value {
  font-size: 14px;
  color: #333;
  flex: 1;
}

.coupon-selector {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  border: 2px solid #eee;
  border-radius: 12px;
}

.coupon-info {
  flex: 1;
}

.coupon-text {
  font-size: 14px;
  color: #333;
  margin-right: 10px;
}

.coupon-discount {
  font-size: 12px;
  color: #ff6b6b;
  background: #ffeaea;
  padding: 2px 6px;
  border-radius: 8px;
}

.arrow-right {
  font-size: 18px;
  color: #ccc;
}

.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.payment-method {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border: 2px solid #eee;
  border-radius: 12px;
  transition: all 0.3s;
}

.payment-method.active {
  border-color: #667eea;
  background: #f0f4ff;
}

.method-icon {
  width: 40px;
  height: 40px;
  background: #f0f0f0;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-image {
  width: 24px;
  height: 24px;
}

.method-info {
  flex: 1;
}

.method-name {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-bottom: 5px;
  display: block;
}

.method-desc {
  font-size: 12px;
  color: #999;
  display: block;
}

.method-check {
  width: 24px;
  height: 24px;
  border: 2px solid #ddd;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.payment-method.active .method-check {
  border-color: #667eea;
  background: #667eea;
}

.check-icon {
  color: white;
  font-size: 14px;
  font-weight: bold;
}

.cost-breakdown {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
}

.cost-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.cost-item.total {
  margin-bottom: 0;
}

.cost-item.discount .cost-value {
  color: #4CAF50;
}

.cost-label {
  font-size: 14px;
  color: #666;
}

.cost-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.cost-value.total {
  font-size: 18px;
  font-weight: bold;
  color: #ff6b6b;
}

.cost-divider {
  height: 1px;
  background: #ddd;
  margin: 15px 0;
}

.agreement-section {
  padding: 20px;
  margin: 20px 0;
}

.agreement-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.check-box {
  width: 18px;
  height: 18px;
  border: 2px solid #ddd;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: white;
  flex-shrink: 0;
  margin-top: 2px;
}

.check-box.checked {
  background: #667eea;
  border-color: #667eea;
}

.agreement-text {
  font-size: 12px;
  color: #666;
  line-height: 1.6;
}

.link {
  color: #667eea;
  text-decoration: none;
}

.payment-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
}

.amount-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.amount-label {
  font-size: 14px;
  color: #666;
}

.amount-value {
  font-size: 24px;
  font-weight: bold;
  color: #ff6b6b;
}

.original-amount {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
}

.pay-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: bold;
}

.pay-btn.disabled {
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

.coupon-modal {
  background: white;
  border-radius: 20px;
  margin: 20px;
  max-width: 400px;
  width: 100%;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
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

.coupon-list {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.coupon-item {
  margin-bottom: 15px;
}

.coupon-item:last-child {
  margin-bottom: 0;
}

.coupon-item.disabled {
  opacity: 0.5;
}

.coupon-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  transition: all 0.3s;
}

.coupon-item.active .coupon-card {
  border-color: #667eea;
  background: #f0f4ff;
}

.coupon-amount {
  text-align: center;
  min-width: 80px;
}

.amount {
  font-size: 24px;
  font-weight: bold;
  color: #ff6b6b;
  display: block;
}

.condition {
  font-size: 10px;
  color: #999;
  display: block;
  margin-top: 5px;
}

.coupon-info {
  flex: 1;
}

.coupon-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
  display: block;
}

.coupon-validity {
  font-size: 12px;
  color: #999;
  display: block;
}

.success-modal {
  background: white;
  border-radius: 20px;
  padding: 40px 30px;
  margin: 20px;
  text-align: center;
  max-width: 350px;
  width: 100%;
}

.success-icon {
  width: 60px;
  height: 60px;
  background: #4CAF50;
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.success-check {
  font-size: 30px;
  color: white;
  font-weight: bold;
}

.success-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.success-message {
  font-size: 14px;
  color: #666;
  margin-bottom: 30px;
}

.success-actions {
  display: flex;
  gap: 15px;
}

.success-btn {
  flex: 1;
  padding: 12px;
  border-radius: 20px;
  font-size: 14px;
  text-align: center;
}

.success-btn.secondary {
  border: 2px solid #667eea;
  color: #667eea;
  background: white;
}

.success-btn.primary {
  background: #667eea;
  color: white;
}
</style>
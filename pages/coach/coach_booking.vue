<template>
  <view class="coach-booking-page">
    <!-- 顶部导航栏 -->
    <view class="nav-bar">
      <view class="nav-content">
        <view class="back-btn" @click="goBack">
          <text class="back-icon">←</text>
        </view>
        <text class="nav-title">预约教练</text>
        <view class="nav-actions">
          <text class="help-btn" @click="showHelp">?</text>
        </view>
      </view>
    </view>

    <scroll-view class="booking-container" scroll-y>
      <!-- 教练信息卡片 -->
      <view class="coach-info-card">
        <view class="coach-header">
          <image 
            :src="coachDetail.avatar || '/static/nav/n1.png'" 
            mode="aspectFill" 
            class="coach-avatar" 
          />
          <view class="coach-details">
            <view class="coach-name">{{ coachDetail.name }}</view>
            <view class="coach-specialization">{{ coachDetail.specialization }}</view>
            <view class="coach-rating">
              <text class="stars">
                <text v-for="n in 5" :key="n" class="star" :class="{ filled: n <= Math.floor(coachDetail.rating || 0) }">⭐</text>
              </text>
              <text class="rating-text">{{ coachDetail.rating || 0 }}分</text>
            </view>
            <view class="coach-price">
              <text class="price-label">时薪：</text>
              <text class="price-value">¥{{ coachDetail.hourly_rate }}/小时</text>
            </view>
          </view>
        </view>
        
        <view class="booking-type-info">
          <view class="type-item">
            <text class="type-label">预约类型：</text>
            <text class="type-value">{{ bookingType === 'single' ? '单次预约' : '套餐预约' }}</text>
          </view>
          <view class="type-item">
            <text class="type-label">课时时长：</text>
            <text class="type-value">60分钟</text>
          </view>
        </view>
      </view>

      <!-- 场地选择 -->
      <view class="booking-section">
        <text class="section-title">选择场地</text>
        <view class="facility-list">
          <view 
            v-for="facility in facilities" 
            :key="facility.id"
            class="facility-item"
            :class="{ active: selectedFacility?.id === facility.id }"
            @click="selectFacility(facility)"
          >
            <image 
              :src="facility.image || '/static/images/场馆1.png'" 
              mode="aspectFill" 
              class="facility-image" 
            />
            <view class="facility-info">
              <view class="facility-name">{{ facility.name }}</view>
              <view class="facility-location">📍 {{ facility.location }}</view>
              <view class="facility-features">
                <text class="feature-tag" v-for="feature in facility.features.slice(0, 2)" :key="feature">{{ feature }}</text>
              </view>
            </view>
            <view class="facility-price">
              <text class="price">¥{{ facility.price_per_hour }}/小时</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 日期选择 -->
      <view class="booking-section">
        <text class="section-title">选择日期</text>
        <view class="date-selector">
          <scroll-view class="date-list" scroll-x>
            <view 
              v-for="date in availableDates" 
              :key="date.value"
              class="date-item"
              :class="{ 
                active: selectedDate?.value === date.value,
                disabled: date.disabled 
              }"
              @click="selectDate(date)"
            >
              <text class="day">{{ date.day }}</text>
              <text class="weekday">{{ date.weekday }}</text>
              <text class="date">{{ date.date }}</text>
            </view>
          </scroll-view>
        </view>
      </view>

      <!-- 时间段选择 -->
      <view class="booking-section" v-if="selectedDate">
        <text class="section-title">选择时间段</text>
        <view class="time-slots">
          <view 
            v-for="slot in timeSlots" 
            :key="slot.time"
            class="time-slot"
            :class="{ 
              active: selectedTimeSlot?.time === slot.time,
              disabled: !slot.available 
            }"
            @click="selectTimeSlot(slot)"
          >
            <text class="time">{{ slot.time }}</text>
            <text class="duration">{{ slot.duration }}</text>
            <text v-if="!slot.available" class="status">已约满</text>
          </view>
        </view>
     <!--   <view v-if="timeSlots.length 0" class="no-slots">
          <text class="no-slots-text">该日期暂无可用时间段</text>
        </view> -->
      </view>

      <!-- 课时数量（套餐） -->
      <view class="booking-section" v-if="bookingType === 'package'">
        <text class="section-title">选择课时数量</text>
        <view class="package-options">
          <view 
            v-for="option in packageOptions" 
            :key="option.hours"
            class="package-item"
            :class="{ active: selectedPackage?.hours === option.hours }"
            @click="selectPackage(option)"
          >
            <view class="package-header">
              <text class="hours">{{ option.hours }}小时</text>
              <text class="original-price">¥{{ option.originalPrice }}</text>
            </view>
            <view class="package-price">
              <text class="discount-price">¥{{ option.discountPrice }}</text>
              <text class="savings">省¥{{ option.savings }}</text>
            </view>
            <view class="package-features">
              <text class="feature">有效期：{{ option.validity }}</text>
              <text class="feature">可转让</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 预约备注 -->
      <view class="booking-section">
        <text class="section-title">备注信息（可选）</text>
        <view class="note-input">
          <textarea 
            v-model="bookingNote"
            placeholder="请输入您的特殊要求或备注信息..."
            class="note-textarea"
            maxlength="200"
          />
          <view class="char-count">
            <text>{{ bookingNote.length }}/200</text>
          </view>
        </view>
      </view>

      <!-- 费用计算 -->
      <view class="booking-section">
        <text class="section-title">费用计算</text>
        <view class="cost-breakdown">
          <view class="cost-item">
            <text class="cost-label">教练费用</text>
            <text class="cost-value">¥{{ coachCost }}</text>
          </view>
          <view class="cost-item" v-if="selectedFacility">
            <text class="cost-label">场地费用</text>
            <text class="cost-value">¥{{ facilityCost }}</text>
          </view>
          <view class="cost-item" v-if="bookingType === 'package' && selectedPackage">
            <text class="cost-label">套餐优惠</text>
            <text class="cost-value discount">-¥{{ selectedPackage.savings }}</text>
          </view>
          <view class="cost-divider"></view>
          <view class="cost-item total">
            <text class="cost-label">总计</text>
            <text class="cost-value total">¥{{ totalCost }}</text>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- 底部预约栏 -->
    <view class="booking-footer">
      <view class="cost-summary">
        <text class="cost-label">合计：</text>
        <text class="cost-value">¥{{ totalCost }}</text>
      </view>
      <view 
        class="booking-btn"
     
        @click="proceedToPayment"
      >
        <text class="btn-text">确认预约</text>
      </view>
    </view>

    <!-- 帮助弹窗 -->
    <view v-if="showHelpModal" class="modal-overlay" @click="closeHelpModal">
      <view class="help-modal" @click.stop>
        <view class="modal-header">
          <text class="modal-title">预约说明</text>
          <text class="modal-close" @click="closeHelpModal">×</text>
        </view>
        <view class="help-content">
          <text class="help-text">
            1. 请选择合适的场地和时间段
            2. 单次预约按小时收费，套餐享受优惠
            3. 预约后请准时到达，如有变化请提前取消
            4. 费用包含教练指导费和场地费
          </text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
	import { http } from '@/utils/http.js'
export default {
  name: 'CoachBooking',
  data() {
    return {
      coachId: null,
      bookingType: 'single',
      coachDetail: {},
      selectedFacility: null,
      selectedDate: null,
      selectedTimeSlot: null,
      selectedPackage: null,
      bookingNote: '',
      showHelpModal: false,
      loading: false,
      
      // 模拟数据
      facilities: [
        {
          id: 1,
          name: '体育中心网球场',
          location: '朝阳区体育中心',
          price_per_hour: 80,
          image: '/static/images/场馆1.png',
          features: ['专业网球场', '免费停车', '器材租借']
        },
        {
          id: 2,
          name: '奥林匹克篮球馆',
          location: '海淀区奥体中心',
          price_per_hour: 60,
          image: '/static/images/场馆2.png',
          features: ['标准篮球场', '空调环境', '储物柜']
        },
        {
          id: 3,
          name: '阳光游泳馆',
          location: '西城区游泳中心',
          price_per_hour: 50,
          image: '/static/images/场馆3.png',
          features: ['恒温泳池', '淋浴设施', '救生员']
        }
      ],
      
      availableDates: [],
      timeSlots: [],
      
      packageOptions: [
        {
          hours: 10,
          originalPrice: 3000,
          discountPrice: 2700,
          savings: 300,
          validity: '3个月'
        },
        {
          hours: 20,
          originalPrice: 6000,
          discountPrice: 5100,
          savings: 900,
          validity: '6个月'
        },
        {
          hours: 50,
          originalPrice: 15000,
          discountPrice: 12000,
          savings: 3000,
          validity: '1年'
        }
      ]
    }
  },
  
  computed: {
    coachCost() {
      if (this.bookingType === 'single') {
        return this.coachDetail.hourly_rate || 0;
      } else {
        return this.selectedPackage ? this.selectedPackage.discountPrice : 0;
      }
    },
    
    facilityCost() {
      return this.selectedFacility ? this.selectedFacility.price_per_hour : 0;
    },
    
    totalCost() {
      return this.coachCost + this.facilityCost;
    },
    
  canProceed() {
    // 套餐：场地+日期+套餐
    if (this.bookingType === 'package') {
      return this.selectedFacility && this.selectedDate && this.selectedPackage;
    }
    // 单次：场地+日期+任意一个可用时段
    return this.selectedFacility && this.selectedDate && this.timeSlots.some(s => s.available);
  }
  },
  
  onLoad(options) {
    
    this.loadCoachDetail();
    this.generateAvailableDates();
  },
  
  methods: {
    async loadCoachDetail() {
		
		
	 this.coachDetail = uni.getStorageSync("coacher")
    },
    
    generateAvailableDates() {
      const dates = [];
      const today = new Date();
      
      for (let i = 1; i <= 14; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        
        const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
        
        dates.push({
          value: date.toISOString().split('T')[0],
          day: date.getDate(),
          weekday: '周' + weekdays[date.getDay()],
          date: (date.getMonth() + 1) + '/' + date.getDate(),
          disabled: false
        });
      }
      
      this.availableDates = dates;
    },
    
    async selectDate(date) {
      if (date.disabled) return;
      
      this.selectedDate = date;
      this.selectedTimeSlot = null;
      await this.loadTimeSlots();
    },
    
  async loadTimeSlots() {
    // 不再请求后台，直接给模拟数据
    this.timeSlots = [
      { time: '08:00-09:00', duration: '60分钟', available: true },
      { time: '09:00-10:00', duration: '60分钟', available: false },
      { time: '10:00-11:00', duration: '60分钟', available: true },
      { time: '14:00-15:00', duration: '60分钟', available: true },
      { time: '15:00-16:00', duration: '60分钟', available: true },
      { time: '16:00-17:00', duration: '60分钟', available: false }
    ];
  },
    
    selectFacility(facility) {
      this.selectedFacility = facility;
    },
    
    selectTimeSlot(slot) {
      if (!slot.available) return;
      this.selectedTimeSlot = slot;
    },
    
    selectPackage(option) {
      this.selectedPackage = option;
    },
    
  proceedToPayment() {
    if (!this.canProceed) return;
  
    // 取当前选中或第一个可用时段
    let slot = this.selectedTimeSlot || this.timeSlots.find(s => s.available);
    if (this.bookingType === 'single' && !slot) {
      uni.showToast({ title: '当天没有可用时段', icon: 'none' });
      return;
    }
  
    // 核心：把 "14:00-15:00" 拆成两段
    const [start_time, end_time] = slot.time.split('-');
  
    const bookingData = {
      coach_id: this.coachDetail.id,
      bookingType: this.bookingType,
      venue_id: this.selectedFacility.id,
      booking_date: this.selectedDate.value,
      start_time,          // "14:00"
      end_time,            // "15:00"
      package: this.selectedPackage || null,
      description: this.bookingNote.trim(),
      total_price: this.totalCost
    };
  
    uni.setStorageSync('cur_order_coacher', bookingData);
    uni.navigateTo({
      url: '/pages/coach/coach_payment?data=' + encodeURIComponent(JSON.stringify(bookingData))
    });
  },
    
    showHelp() {
      this.showHelpModal = true;
    },
    
    closeHelpModal() {
      this.showHelpModal = false;
    },
    
    goBack() {
      uni.navigateBack();
    }
  }
}
</script>

<style scoped>
.coach-booking-page {
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

.help-btn {
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

.booking-container {
  flex: 1;
  padding: 20px;
  padding-bottom: 120px;
}

.coach-info-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.coach-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.coach-avatar {
  width: 60px;
  height: 60px;
  border-radius: 30px;
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.coach-details {
  flex: 1;
}

.coach-name {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.coach-specialization {
  font-size: 14px;
  color: #667eea;
  margin-bottom: 8px;
}

.coach-rating {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 5px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 12px;
  color: #ddd;
}

.star.filled {
  color: #FFD700;
}

.rating-text {
  font-size: 14px;
  color: #333;
}

.coach-price {
  display: flex;
  align-items: center;
  gap: 5px;
}

.price-label {
  font-size: 12px;
  color: #666;
}

.price-value {
  font-size: 16px;
  font-weight: bold;
  color: #ff6b6b;
}

.booking-type-info {
  display: flex;
  gap: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.type-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.type-label {
  font-size: 14px;
  color: #666;
}

.type-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.booking-section {
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

.facility-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.facility-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border: 2px solid #eee;
  border-radius: 15px;
  transition: all 0.3s;
}

.facility-item.active {
  border-color: #667eea;
  background: #f0f4ff;
}

.facility-image {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  background: #f0f0f0;
}

.facility-info {
  flex: 1;
}

.facility-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.facility-location {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.facility-features {
  display: flex;
  gap: 5px;
}

.feature-tag {
  font-size: 10px;
  color: #667eea;
  background: #f0f4ff;
  padding: 2px 6px;
  border-radius: 8px;
}

.facility-price {
  text-align: right;
}

.price {
  font-size: 14px;
  font-weight: bold;
  color: #ff6b6b;
}

.date-list {
  white-space: nowrap;
}

.date-item {
  display: inline-block;
  text-align: center;
  padding: 15px 12px;
  margin-right: 10px;
  border: 2px solid #eee;
  border-radius: 15px;
  min-width: 60px;
  transition: all 0.3s;
}

.date-item.active {
  border-color: #667eea;
  background: #f0f4ff;
}

.date-item.disabled {
  opacity: 0.5;
  background: #f5f5f5;
}

.day {
  display: block;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.weekday {
  display: block;
  font-size: 12px;
  color: #999;
  margin-top: 2px;
}

.date {
  display: block;
  font-size: 10px;
  color: #ccc;
  margin-top: 2px;
}

.time-slots {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}

.time-slot {
  text-align: center;
  padding: 15px 10px;
  border: 2px solid #eee;
  border-radius: 12px;
  transition: all 0.3s;
}

.time-slot.active {
  border-color: #667eea;
  background: #f0f4ff;
}

.time-slot.disabled {
  opacity: 0.5;
  background: #f5f5f5;
}

.time {
  display: block;
  font-size: 14px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.duration {
  display: block;
  font-size: 12px;
  color: #999;
}

.status {
  display: block;
  font-size: 10px;
  color: #ff6b6b;
  margin-top: 5px;
}

.no-slots {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.package-options {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.package-item {
  padding: 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  transition: all 0.3s;
}

.package-item.active {
  border-color: #667eea;
  background: #f0f4ff;
}

.package-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.hours {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.original-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
}

.package-price {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.discount-price {
  font-size: 24px;
  font-weight: bold;
  color: #ff6b6b;
}

.savings {
  font-size: 12px;
  color: #4CAF50;
  background: #e8f5e8;
  padding: 2px 6px;
  border-radius: 8px;
}

.package-features {
  display: flex;
  gap: 15px;
}

.feature {
  font-size: 12px;
  color: #666;
}

.note-input {
  position: relative;
}

.note-textarea {
  width: 100%;
  min-height: 100px;
  padding: 15px;
  border: 2px solid #eee;
  border-radius: 12px;
  font-size: 14px;
  resize: vertical;
}

.char-count {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-size: 12px;
  color: #999;
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

.cost-label {
  font-size: 14px;
  color: #666;
}

.cost-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.cost-value.discount {
  color: #4CAF50;
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

.booking-footer {
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

.cost-summary {
  flex: 1;
}

.cost-summary .cost-label {
  font-size: 14px;
  color: #666;
}

.cost-summary .cost-value {
  font-size: 20px;
  font-weight: bold;
  color: #ff6b6b;
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

.help-modal {
  background: white;
  border-radius: 20px;
  margin: 20px;
  max-width: 400px;
  width: 100%;
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

.help-content {
  padding: 20px;
}

.help-text {
  font-size: 14px;
  color: #666;
  line-height: 1.8;
}
</style>
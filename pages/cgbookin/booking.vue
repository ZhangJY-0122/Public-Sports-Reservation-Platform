<template>
    <view class="booking-container">
        <!-- 顶部导航栏 -->
        <view class="header">
            <view class="back-btn" @click="goBack">←</view>
            <text class="header-title">🏟️ 预约场馆</text>
            <view class="calendar-btn">📅</view>
        </view>

        <!-- 场馆信息卡片 -->
        <view class="venue-info-card">
          <!--  <view class="venue-avatar">
                <text class="venue-icon">{{ venueInfo.icon }}</text>
            </view> -->
            <view class="venue-details">
                <text class="venue-name">{{ venueInfo.name }}</text>
                <text class="venue-type">{{ venueInfo.type }}</text>
                <view class="venue-rating">
                    <text class="rating-stars">⭐⭐⭐⭐⭐</text>
                    <text class="rating-score">{{ venueInfo.rating }}</text>
                    <text class="review-count">({{ venueInfo.reviewCount }}条评价)</text>
                </view>
            </view>
            <view class="venue-price">
                <text class="price-unit">¥</text>
                <text class="price-amount">{{ venueInfo.price }}</text>
                <text class="price-unit">/小时</text>
            </view>
        </view>

        <!-- 时间选择区域 -->
        <view class="time-section">
            <text class="section-title">⏰ 选择时间</text>
            
            <view class="date-selector">
                <text class="selector-label">📅 预约日期</text>
                <picker mode="date" :value="selectedDate" start="2023-01-01" end="2030-12-31" @change="onDateChange">
                    <view class="picker-display">
                        <text class="picker-text">{{ selectedDate || '请选择日期' }}</text>
                        <text class="picker-arrow">▼</text>
                    </view>
                </picker>
            </view>

            <view class="time-selector">
                <text class="selector-label">🕐 开始时间</text>
                <picker mode="time" :value="startTime" start="06:00" end="23:00" @change="onStartTimeChange">
                    <view class="picker-display">
                        <text class="picker-text">{{ startTime || '请选择开始时间' }}</text>
                        <text class="picker-arrow">▼</text>
                    </view>
                </picker>
            </view>

            <view class="time-selector">
                <text class="selector-label">🕐 结束时间</text>
                <picker mode="time" :value="endTime" start="06:00" end="23:00" @change="onEndTimeChange">
                    <view class="picker-display">
                        <text class="picker-text">{{ endTime || '请选择结束时间' }}</text>
                        <text class="picker-arrow">▼</text>
                    </view>
                </picker>
            </view>
        </view>

        <!-- 费用计算区域 -->
        <view class="cost-section">
            <text class="section-title">💰 费用详情</text>
            
            <view class="cost-detail">
                <view class="cost-item">
                    <text class="cost-label">💵 时长费用</text>
                    <text class="cost-value">{{ durationCost }}元</text>
                </view>
                
                <view class="cost-item">
                    <text class="cost-label">📊 分摊人数</text>
                    <view class="sharer-counter">
                        <view class="counter-btn" @click="decreaseSharers">-</view>
                        <text class="counter-value">{{ sharerCount }}</text>
                        <view class="counter-btn" @click="increaseSharers">+</view>
                    </view>
                </view>
                
                <view class="cost-item">
                    <text class="cost-label">💝 优惠折扣</text>
                    <text class="cost-value">-{{ discount }}元</text>
                </view>
                
                <view class="cost-item">
                    <text class="cost-label">💸 每人费用</text>
                    <text class="cost-value highlight">¥{{ perPersonCost }}</text>
                </view>
            </view>
        </view>

        <!-- 费用分摊开关 -->
        <view class="sharing-section">
            <text class="section-title">🤝 费用分摊</text>
            
            <view class="sharing-toggle">
                <text class="toggle-label">� 开启费用分摊</text>
                <switch :checked="isSharing" @change="onSharingChange" color="#007AFF"/>
            </view>
            
            <view class="sharing-tip" v-if="isSharing">
                💡 已开启费用分摊，请选择 {{ sharerCount }} 位朋友
            </view>
        </view>

        <!-- 朋友选择列表 (新增功能) -->
        <view class="friends-section" v-if="isSharing">
            <text class="section-title">👥 选择朋友</text>
            <text class="section-subtitle">已选择 {{ selectedFriends.length }}/{{ sharerCount }} 位朋友</text>
            
            <view class="friends-list">
                <view 
                    v-for="friend in friends" 
                    :key="friend.id"
                    class="friend-item"
                    :class="{ selected: selectedFriends.includes(friend.id) }"
                    @click="toggleFriend(friend.id)"
                >
                  <!--  <view class="friend-avatar">
                        <text class="friend-emoji">{{ friend.friend_avatar }}</text>
                    </view> -->
                    <view class="friend-info">
                        <text class="friend-name">{{ friend.friend_name }}</text>
                        <text class="friend-status">{{ friend.status }}</text>
                    </view>
                    <view class="friend-select" v-if="selectedFriends.includes(friend.id)">
                        <text class="select-icon">✓</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 备注区域 -->
        <view class="notes-section">
            <text class="section-title">📝 预约备注</text>
            <textarea 
                class="notes-input" 
                v-model="bookingNotes" 
                placeholder="请输入备注信息（可选）"
                maxlength="100"
            />
            <view class="notes-counter">
                <text class="counter-text">{{ bookingNotes.length }}/100</text>
            </view>
        </view>

        <!-- 预约确认区域 -->
        <view class="confirm-section">
            <view class="price-summary">
                <text class="summary-label">合计费用</text>
                <text class="summary-amount">¥{{ perPersonCost }}</text>
            </view>
            <button 
                class="confirm-btn" 
                :class="{ disabled: !canConfirm || (isSharing && selectedFriends.length !== sharerCount) }"
                @click="confirmBooking"
                :disabled="!canConfirm || (isSharing && selectedFriends.length !== sharerCount)"
            >
                <text class="btn-text">{{ isLoading ? '提交中...' : '确认预约' }}</text>
            </button>
        </view>

        <!-- 加载状态 -->
        <view class="loading-overlay" v-if="isLoading">
            <view class="loading-spinner"></view>
            <text class="loading-text">正在提交预约...</text>
        </view>

        <!-- 成功弹窗 -->
        <view class="success-modal" v-if="showSuccess">
            <view class="modal-content">
                <text class="success-icon">🎉</text>
                <text class="success-title">预约成功！</text>
                <text class="success-message">您的预约已成功提交<br/>请按时参加活动</text>
                <view class="modal-actions">
                    <button class="modal-btn secondary" @click="closeSuccess">知道了</button>
                    <button class="modal-btn primary" @click="goToMyBookings">查看预约</button>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
	import { http } from '@/utils/http.js'
export default {
    data() {
        return {
            venueId: '',
            selectedDate: '',
            startTime: '',
            endTime: '',
            isSharing: false,
            sharerCount: 2,
            bookingNotes: '',
            isLoading: false,
            showSuccess: false,
            
            // 场馆信息
            venueInfo: {
                name: '🏀 阳光体育中心',
                type: '篮球场 · 室内场地',
                icon: '🏀',
                rating: 4.8,
                reviewCount: 128,
                price: 80
            },
            
            // 朋友列表数据 (新增)
            friends: [
            
            ],
            
            // 已选择的朋友 (新增)
            selectedFriends: [],
			curr_User:""
        }
    },
    
    computed: {
        totalHours() {
            if (!this.startTime || !this.endTime) return 0
            
            const [startHour, startMinute] = this.startTime.split(':').map(Number)
            const [endHour, endMinute] = this.endTime.split(':').map(Number)
            
            const startTotalMinutes = startHour * 60 + startMinute
            const endTotalMinutes = endHour * 60 + endMinute
            
            if (endTotalMinutes <= startTotalMinutes) return 0
            
		console.log("时长",(endTotalMinutes - startTotalMinutes) / 60);
			
			
            return (endTotalMinutes - startTotalMinutes) / 60
        },
        
        durationCost() {
			console.log("费用",Math.round(this.totalHours * this.venueInfo.price * 100) / 100);
            return Math.round(this.totalHours * this.venueInfo.price * 100) / 100
        },
        
        discount() {
            // 简单折扣逻辑
            if (this.totalHours >= 3) {
                return Math.round(this.durationCost * 0.1 * 100) / 100
            }
            return 0
        },
        
        perPersonCost() {
            const totalCost = this.durationCost - this.discount
            if (this.isSharing) {
				var  cu=this.sharerCount+1
                return Math.round((totalCost / cu) * 100) / 100
            }
            return Math.round(totalCost * 100) / 100
        },
        
        canConfirm() {
            return this.selectedDate && this.startTime && this.endTime && this.totalHours > 0 &&
                   (!this.isSharing || this.selectedFriends.length === this.sharerCount)
        }
    },
    
    onLoad(options) {
        this.venueId = options.id || ''
        this.loadVenueInfo(this.venueId)
        this.loadUserInfo()
		this.loadfriend()
    },
    
    methods: {
        goBack() {
            uni.navigateBack()
        },
        
        async loadVenueInfo(id) {
            let res=await http.get("venue/"+id)
			console.log(res,"res");
			this.venueInfo=res
			
			
        },
        
        loadUserInfo() {
            // 从本地存储获取用户信息
            const userInfo = uni.getStorageSync('user')
            if (!userInfo) {
                uni.showToast({
                    title: '请先登录',
                    icon: 'none'
                })
                setTimeout(() => {
                    uni.navigateTo({
                        url: '/pages/auth/login'
                    })
                }, 1500)
            }
			
			this.curr_User=userInfo
        },
		
		loadfriend()
		{
			//获取我的好友
			let  id=this.curr_User.id
			
			http.get("friends/list").then(res=>{
				this.friends=res.friends
				
			})
			
		},
        
        onDateChange(e) {
            this.selectedDate = e.detail.value
        },
        
        onStartTimeChange(e) {
            this.startTime = e.detail.value
            // 如果结束时间早于开始时间，自动调整
            if (this.endTime && this.startTime >= this.endTime) {
                const [hours, minutes] = this.startTime.split(':').map(Number)
                const newEndTime = `${String(hours).padStart(2, '0')}:${String((minutes + 30) % 60).padStart(2, '0')}`
                this.endTime = newEndTime
            }
        },
        
        onEndTimeChange(e) {
            this.endTime = e.detail.value
        },
        
        onSharingChange(e) {
            this.isSharing = e.detail.value
            if (!this.isSharing) {
                // 关闭分摊时清空选择
                this.selectedFriends = []
            }
        },
        
        decreaseSharers() {
            if (this.sharerCount > 2) {
                this.sharerCount--
                // 如果选择的朋友数超过分摊人数，移除多余选择
                if (this.selectedFriends.length > this.sharerCount) {
                    this.selectedFriends = this.selectedFriends.slice(0, this.sharerCount)
                }
            }
        },
        
        increaseSharers() {
            if (this.sharerCount < 10) {
                this.sharerCount++
            }
        },
        
        // 新增：切换朋友选择状态
        toggleFriend(friendId) {
            const index = this.selectedFriends.indexOf(friendId)
            
            if (index > -1) {
                // 取消选择
                this.selectedFriends.splice(index, 1)
            } else {
                // 添加选择，但不超过分摊人数
                if (this.selectedFriends.length < this.sharerCount) {
                    this.selectedFriends.push(friendId)
                } else {
                    uni.showToast({
                        title: `最多只能选择${this.sharerCount}位朋友`,
                        icon: 'none'
                    })
                }
            }
        },
        
        async confirmBooking() {
            if (!this.canConfirm) {
                if (this.isSharing && this.selectedFriends.length !== this.sharerCount) {
                    uni.showToast({
                        title: `请选择${this.sharerCount}位朋友`,
                        icon: 'none'
                    })
                } else {
                    uni.showToast({
                        title: '请完善预约信息',
                        icon: 'none'
                    })
                }
                return
            }
            
            this.isLoading = true
            
            try {
                // 模拟API调用
                await this.submitBooking()
                
                this.showSuccess = true
                
            } catch (error) {
                console.error('预约失败:', error)
                uni.showToast({
                    title: '预约失败，请重试',
                    icon: 'none'
                })
            } finally {
                this.isLoading = false
            }
        },
        
        async submitBooking() {
			
			let params={}
			
			let url=""
			
             if(this.isSharing)
			 {
				 
				 url="booking/create-with-share"
				 
			 }else
			 {
				 
				 
				 url="booking/create"
				 
				 
			 }
			 
			 params={
			 	venue_id: Number(this.venueId),
			 	            booking_date: this.selectedDate,
			 	            start_time: this.startTime,
			 	            end_time: this.endTime,
			 	        
			 	       
			 	            share_users: this.selectedFriends, // 新增
			 	            description: this.bookingNotes
			 }
		
			let  res =await http.post(url,params)
            // 模拟提交预约
            // return new Promise((resolve) => {
            //     setTimeout(() => {
            //         console.log('提交预约数据:', {
            //             venue_id: this.venueId,
            //             date: this.selectedDate,
            //             start_time: this.startTime,
            //             end_time: this.endTime,
            //             is_sharing: this.isSharing,
            //             sharer_count: this.sharerCount,
            //             selected_friends: this.selectedFriends, // 新增
            //             notes: this.bookingNotes
            //         })
            //         resolve()
            //     }, 2000)
            // })
        },
        
        goToMyBookings() {
            uni.navigateTo({
                url: '/pages/my/bookin'
            })
        },
        
        closeSuccess() {
            this.showSuccess = false
            // 重置表单
            this.selectedDate = ''
            this.startTime = ''
            this.endTime = ''
            this.bookingNotes = ''
            this.selectedFriends = []
        }
    }
}
</script>

<style scoped>
.booking-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20rpx;
}

/* 顶部导航栏 */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20rpx 0;
    margin-bottom: 20rpx;
}

.back-btn {
    width: 60rpx;
    height: 60rpx;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 30rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28rpx;
    color: white;
}

.header-title {
    font-size: 32rpx;
    font-weight: bold;
    color: white;
}

.calendar-btn {
    width: 60rpx;
    height: 60rpx;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 30rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24rpx;
}

/* 场馆信息卡片 */
.venue-info-card {
    background: white;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.venue-avatar {
    width: 100rpx;
    height: 100rpx;
    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
    border-radius: 50rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 30rpx;
}

.venue-icon {
    font-size: 40rpx;
}

.venue-details {
    flex: 1;
}

.venue-name {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
}

.venue-type {
    font-size: 24rpx;
    color: #666;
    margin-bottom: 12rpx;
}

.venue-rating {
    display: flex;
    align-items: center;
    gap: 8rpx;
}

.rating-stars {
    font-size: 20rpx;
}

.rating-score {
    font-size: 22rpx;
    font-weight: bold;
    color: #ff9500;
}

.review-count {
    font-size: 20rpx;
    color: #999;
}

.venue-price {
    display: flex;
    align-items: baseline;
    color: #ff6b6b;
}

.price-unit {
    font-size: 24rpx;
}

.price-amount {
    font-size: 36rpx;
    font-weight: bold;
}

/* 区域标题 */
.section-title {
    font-size: 28rpx;
    font-weight: bold;
    color: white;
    margin-bottom: 20rpx;
    display: block;
}

.section-subtitle {
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 16rpx;
    display: block;
}

/* 时间选择区域 */
.time-section {
    background: white;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.date-selector,
.time-selector {
    margin-bottom: 24rpx;
}

.selector-label {
    font-size: 26rpx;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
}

.picker-display {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20rpx;
    background: #f8f9fa;
    border-radius: 12rpx;
    border: 2rpx solid #e9ecef;
}

.picker-text {
    font-size: 28rpx;
    color: #333;
}

.picker-arrow {
    font-size: 20rpx;
    color: #666;
}

/* 费用计算区域 */
.cost-section {
    background: white;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.cost-detail {
    display: flex;
    flex-direction: column;
    gap: 20rpx;
}

.cost-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 16rpx;
    border-bottom: 2rpx solid #f0f0f0;
}

.cost-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.cost-label {
    font-size: 26rpx;
    color: #666;
}

.cost-value {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
}

.cost-value.highlight {
    color: #007AFF;
}

.sharer-counter {
    display: flex;
    align-items: center;
    gap: 20rpx;
}

.counter-btn {
    width: 48rpx;
    height: 48rpx;
    background: #007AFF;
    color: white;
    border-radius: 24rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24rpx;
    font-weight: bold;
}

.counter-value {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    min-width: 60rpx;
    text-align: center;
}

/* 费用分摊开关 */
.sharing-section {
    background: white;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.sharing-toggle {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12rpx;
}

.toggle-label {
    font-size: 26rpx;
    color: #333;
}

.sharing-tip {
    font-size: 22rpx;
    color: #666;
    background: #f8f9fa;
    padding: 16rpx;
    border-radius: 8rpx;
}

/* 朋友选择列表区域 */
.friends-section {
    background: white;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.friends-list {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
}

.friend-item {
    display: flex;
    align-items: center;
    padding: 20rpx;
    background: #f8f9fa;
    border-radius: 12rpx;
    border: 2rpx solid transparent;
    transition: all 0.3s ease;
}

.friend-item.selected {
    background: #e3f2fd;
    border-color: #007AFF;
}

.friend-avatar {
    width: 64rpx;
    height: 64rpx;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 32rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20rpx;
}

.friend-emoji {
    font-size: 28rpx;
}

.friend-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4rpx;
}

.friend-name {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
}

.friend-status {
    font-size: 22rpx;
    color: #666;
}

.friend-select {
    width: 40rpx;
    height: 40rpx;
    background: #007AFF;
    border-radius: 20rpx;
    display: flex;
    align-items: center;
    justify-content: center;
}

.select-icon {
    color: white;
    font-size: 24rpx;
    font-weight: bold;
}

/* 备注区域 */
.notes-section {
    background: white;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 120rpx;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.notes-input {
    width: 100%;
    height: 160rpx;
    background: #f8f9fa;
    border-radius: 12rpx;
    padding: 20rpx;
    font-size: 26rpx;
    color: #333;
    border: 2rpx solid #e9ecef;
}

.notes-counter {
    text-align: right;
    margin-top: 8rpx;
}

.counter-text {
    font-size: 20rpx;
    color: #999;
}

/* 预约确认区域 */
.confirm-section {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    padding: 20rpx;
    border-top: 2rpx solid #f0f0f0;
    display: flex;
    align-items: center;
    gap: 20rpx;
}

.price-summary {
    flex: 1;
}

.summary-label {
    font-size: 26rpx;
    color: #666;
}

.summary-amount {
    font-size: 32rpx;
    font-weight: bold;
    color: #ff6b6b;
}

.confirm-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50rpx;
    padding: 24rpx 48rpx;
    display: flex;
    align-items: center;
    justify-content: center;
}

.confirm-btn.disabled {
    background: #ccc;
}

.btn-text {
    color: white;
    font-size: 28rpx;
    font-weight: bold;
}

/* 加载状态 */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.loading-spinner {
    width: 60rpx;
    height: 60rpx;
    border: 6rpx solid #f3f3f3;
    border-top: 6rpx solid #007AFF;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20rpx;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-text {
    color: white;
    font-size: 26rpx;
}

/* 成功弹窗 */
.success-modal {
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
    border-radius: 20rpx;
    padding: 60rpx 40rpx;
    text-align: center;
    max-width: 500rpx;
}

.success-icon {
    font-size: 80rpx;
    display: block;
    margin-bottom: 20rpx;
}

.success-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
}

.success-message {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
    margin-bottom: 40rpx;
    display: block;
}

.modal-actions {
    display: flex;
    gap: 20rpx;
    justify-content: center;
}

.modal-btn {
    padding: 20rpx 32rpx;
    border-radius: 50rpx;
    font-size: 26rpx;
    font-weight: bold;
}

.modal-btn.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.modal-btn.secondary {
    background: #f8f9fa;
    color: #666;
    border: 2rpx solid #e9ecef;
}
</style>
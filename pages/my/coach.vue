<template>
    <view class="coaches-page">
        <!-- 顶部导航栏 -->
        <view class="nav-bar">
            <view class="nav-content">
                <text class="nav-title">我预约的教练</text>
            </view>
        </view>
        
        <!-- 统计卡片 -->
        <view class="stats-section">
            <view class="stats-grid">
                <view class="stat-card">
                    <view class="stat-icon upcoming">📅</view>
                    <view class="stat-info">
                        <text class="stat-number">{{ upcomingCount }}</text>
                        <text class="stat-label">即将开始</text>
                    </view>
                </view>
                <view class="stat-card">
                    <view class="stat-icon ongoing">⚡</view>
                    <view class="stat-info">
                        <text class="stat-number">{{ ongoingCount }}</text>
                        <text class="stat-label">进行中</text>
                    </view>
                </view>
                <view class="stat-card">
                    <view class="stat-icon completed">✅</view>
                    <view class="stat-info">
                        <text class="stat-number">{{ completedCount }}</text>
                        <text class="stat-label">已完成</text>
                    </view>
                </view>
            </view>
        </view>
        
        <!-- 筛选选项 -->
        <view class="filter-section">
            <view class="filter-tabs">
                <view 
                    v-for="tab in filterTabs" 
                    :key="tab.key"
                    :class="['filter-tab', { active: activeFilter === tab.key }]"
                    @click="changeFilter(tab.key)"
                >
                    <text>{{ tab.label }}</text>
                </view>
            </view>
            
            <view class="filter-actions">
                <picker mode="selector" :range="sportTypes" @change="onSportTypeChange">
                    <view class="filter-picker">
                        <text class="filter-text">{{ selectedSportType || '全部运动' }}</text>
                        <text class="filter-arrow">▼</text>
                    </view>
                </picker>
                
                <picker mode="date" @change="onDateChange">
                    <view class="filter-picker">
                        <text class="filter-text">{{ selectedDate || '全部日期' }}</text>
                        <text class="filter-arrow">▼</text>
                    </view>
                </picker>
            </view>
        </view>
        
        <!-- 教练列表 -->
        <view class="coaches-list">
            <view 
                v-for="booking in filteredBookings" 
                :key="booking.id"
                class="coach-card"
                @click="viewCoachDetail(booking)"
            >
                <view class="coach-header">
                    <view class="coach-avatar">
                        <image :src="booking.coach.avatar" mode="aspectFill" class="avatar-img" />
                        <view class="coach-status" :class="booking.status">{{ getStatusText(booking.status) }}</view>
                    </view>
                    <view class="coach-info">
                        <view class="coach-name">{{ booking.coach.name }}</view>
                        <view class="coach-sport">{{ booking.coach.sport }}</view>
                        <view class="coach-rating">
                            <text class="stars">⭐ {{ booking.coach.rating }}</text>
                            <text class="experience">{{ booking.coach.experience }}年经验</text>
                        </view>
                    </view>
                    <view class="coach-actions">
                        <view 
                            v-if="booking.status === 'upcoming'" 
                            class="action-btn cancel"
                            @click.stop="cancelBooking(booking.id)"
                        >
                            取消预约
                        </view>
                        <view 
                            v-if="booking.status === 'completed'" 
                            class="action-btn review"
                            @click.stop="writeReview(booking.id)"
                        >
                            写评价
                        </view>
                    </view>
                </view>
                
                <view class="booking-details">
                    <view class="detail-item">
                        <text class="detail-label">预约时间</text>
                        <text class="detail-value">{{ booking.datetime }}</text>
                    </view>
                    <view class="detail-item">
                        <text class="detail-label">课程类型</text>
                        <text class="detail-value">{{ booking.courseType }}</text>
                    </view>
                    <view class="detail-item">
                        <text class="detail-label">预约时长</text>
                        <text class="detail-value">{{ booking.duration }}小时</text>
                    </view>
                    <view class="detail-item">
                        <text class="detail-label">费用</text>
                        <text class="detail-value price">¥{{ booking.price }}</text>
                    </view>
                </view>
                
                <view class="booking-notes" v-if="booking.notes">
                    <text class="notes-label">备注：</text>
                    <text class="notes-content">{{ booking.notes }}</text>
                </view>
            </view>
            
            <!-- 空状态 -->
            <view v-if="filteredBookings.length === 0" class="empty-state">
                <text class="empty-icon">🎾</text>
                <text class="empty-text">暂无预约记录</text>
                <text class="empty-subtext">快去预约一位教练开始运动吧！</text>
            </view>
        </view>
        
        <!-- 快速预约按钮 -->
        <view class="fab-button" @click="quickBooking">
            <text class="fab-icon">+</text>
            <text class="fab-text">预约教练</text>
        </view>
        
        <!-- 写评价弹窗 -->
        <view v-if="showReviewModal" class="modal-overlay" @click="closeReviewModal">
            <view class="review-modal" @click.stop>
                <view class="modal-header">
                    <text class="modal-title">写评价</text>
                    <text class="modal-close" @click="closeReviewModal">×</text>
                </view>
                
                <view class="review-form">
                    <view class="rating-section">
                        <text class="rating-label">评分</text>
                        <view class="rating-stars">
                            <text 
                                v-for="star in 5" 
                                :key="star"
                                :class="['star', { active: star <= newReview.rating }]"
                                @click="setRating(star)"
                            >⭐</text>
                        </view>
                    </view>
                    
                    <view class="comment-section">
                        <text class="comment-label">评价内容</text>
                        <textarea 
                            v-model="newReview.comment"
                            placeholder="分享您的课程体验..."
                            class="comment-input"
                            maxlength="200"
                        />
                        <text class="char-count">{{ newReview.comment.length }}/200</text>
                    </view>
                    
                    <view class="review-actions">
                        <view class="cancel-btn" @click="closeReviewModal">取消</view>
                        <view class="submit-btn" @click="submitReview">提交评价</view>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    name: 'MyCoaches',
    data() {
        return {
            activeFilter: 'all',
            selectedSportType: '',
            selectedDate: '',
            showReviewModal: false,
            selectedBookingId: '',
            newReview: {
                rating: 0,
                comment: ''
            },
            filterTabs: [
                { key: 'all', label: '全部' },
                { key: 'upcoming', label: '即将开始' },
                { key: 'ongoing', label: '进行中' },
                { key: 'completed', label: '已完成' },
                { key: 'cancelled', label: '已取消' }
            ],
            sportTypes: ['全部运动', '网球', '篮球', '足球', '羽毛球', '游泳', '健身'],
            bookings: [
                {
                    id: 1,
                    coach: {
                        name: '张教练',
                        sport: '网球',
                        rating: 4.8,
                        experience: 8,
                        avatar: '/static/images/场馆2.png'
                    },
                    datetime: '2024-12-20 14:00',
                    courseType: '一对一教学',
                    duration: 2,
                    price: 300,
                    status: 'upcoming',
                    notes: '请提前10分钟到达'
                },
                {
                    id: 2,
                    coach: {
                        name: '李教练',
                        sport: '篮球',
                        rating: 4.9,
                        experience: 12,
                        avatar: '/static/images/场馆2.png'
                    },
                    datetime: '2024-12-18 16:00',
                    courseType: '技巧训练',
                    duration: 1.5,
                    price: 250,
                    status: 'ongoing',
                    notes: ''
                },
                {
                    id: 3,
                    coach: {
                        name: '王教练',
                        sport: '游泳',
                        rating: 4.7,
                        experience: 6,
                        avatar: '/static/images/场馆2.png'
                    },
                    datetime: '2024-12-15 10:00',
                    courseType: '蛙泳教学',
                    duration: 1,
                    price: 200,
                    status: 'completed',
                    notes: '完成了基本动作学习'
                },
                {
                    id: 4,
                    coach: {
                        name: '刘教练',
                        sport: '羽毛球',
                        rating: 4.6,
                        experience: 5,
                        avatar: '/static/images/场馆2.png'
                    },
                    datetime: '2024-12-10 19:00',
                    courseType: '双打配合',
                    duration: 2,
                    price: 280,
                    status: 'cancelled',
                    notes: '因天气原因取消'
                }
            ]
        }
    },
    computed: {
        filteredBookings() {
            let filtered = this.bookings
            
            // 状态筛选
            if (this.activeFilter !== 'all') {
                filtered = filtered.filter(booking => booking.status === this.activeFilter)
            }
            
            // 运动类型筛选
            if (this.selectedSportType && this.selectedSportType !== '全部运动') {
                filtered = filtered.filter(booking => booking.coach.sport === this.selectedSportType)
            }
            
            // 日期筛选
            if (this.selectedDate) {
                filtered = filtered.filter(booking => booking.datetime.startsWith(this.selectedDate))
            }
            
            return filtered
        },
        upcomingCount() {
            return this.bookings.filter(booking => booking.status === 'upcoming').length
        },
        ongoingCount() {
            return this.bookings.filter(booking => booking.status === 'ongoing').length
        },
        completedCount() {
            return this.bookings.filter(booking => booking.status === 'completed').length
        }
    },
    methods: {
        changeFilter(key) {
            this.activeFilter = key
        },
        onSportTypeChange(e) {
            this.selectedSportType = this.sportTypes[e.detail.value]
        },
        onDateChange(e) {
            this.selectedDate = e.detail.value
        },
        getStatusText(status) {
            const statusMap = {
                'upcoming': '即将开始',
                'ongoing': '进行中',
                'completed': '已完成',
                'cancelled': '已取消'
            }
            return statusMap[status] || status
        },
        viewCoachDetail(booking) {
            uni.showModal({
                title: '教练信息',
                content: `教练：${booking.coach.name}\n运动：${booking.coach.sport}\n评分：${booking.coach.rating}星\n经验：${booking.coach.experience}年`,
                showCancel: false
            })
        },
        cancelBooking(id) {
            uni.showModal({
                title: '取消预约',
                content: '确定要取消这个预约吗？',
                success: (res) => {
                    if (res.confirm) {
                        const booking = this.bookings.find(b => b.id === id)
                        if (booking) {
                            booking.status = 'cancelled'
                            uni.showToast({
                                title: '预约已取消',
                                icon: 'success'
                            })
                        }
                    }
                }
            })
        },
        writeReview(id) {
            this.selectedBookingId = id
            this.showReviewModal = true
            this.newReview = { rating: 0, comment: '' }
        },
        setRating(star) {
            this.newReview.rating = star
        },
        closeReviewModal() {
            this.showReviewModal = false
            this.selectedBookingId = ''
            this.newReview = { rating: 0, comment: '' }
        },
        submitReview() {
            if (this.newReview.rating === 0) {
                uni.showToast({
                    title: '请选择评分',
                    icon: 'none'
                })
                return
            }
            
            if (!this.newReview.comment.trim()) {
                uni.showToast({
                    title: '请输入评价内容',
                    icon: 'none'
                })
                return
            }
            
            uni.showToast({
                title: '评价提交成功',
                icon: 'success'
            })
            
            this.closeReviewModal()
        },
        quickBooking() {
            uni.showModal({
                title: '预约教练',
                content: '正在跳转到教练预约页面...\n\n这是uniapp Vue页面的功能演示。\n在实际应用中，这里会跳转到具体的预约页面。',
                showCancel: false
            })
        }
    }
}
</script>

<style scoped>
.coaches-page {
    min-height: 100vh;
    background-color: #f5f5f5;
    padding-bottom: 100rpx;
}

.nav-bar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 40rpx 30rpx 20rpx;
    color: white;
}

.nav-content {
    display: flex;
    align-items: center;
    justify-content: center;
}

.nav-title {
    font-size: 36rpx;
    font-weight: 600;
}

.stats-section {
    margin: 20rpx;
}

.stats-grid {
    display: flex;
    gap: 20rpx;
}

.stat-card {
    flex: 1;
    background: white;
    border-radius: 20rpx;
    padding: 30rpx 20rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.stat-icon {
    width: 80rpx;
    height: 80rpx;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32rpx;
    margin-right: 20rpx;
}

.stat-icon.upcoming {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.ongoing {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon.completed {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-info {
    flex: 1;
}

.stat-number {
    display: block;
    font-size: 32rpx;
    font-weight: 700;
    color: #333;
    margin-bottom: 8rpx;
}

.stat-label {
    font-size: 24rpx;
    color: #666;
}

.filter-section {
    margin: 0 20rpx 20rpx;
    background: white;
    border-radius: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.filter-tabs {
    display: flex;
    margin-bottom: 30rpx;
    border-bottom: 2rpx solid #f0f0f0;
    padding-bottom: 20rpx;
}

.filter-tab {
    flex: 1;
    text-align: center;
    padding: 15rpx 10rpx;
    font-size: 28rpx;
    color: #666;
    border-radius: 10rpx;
    transition: all 0.3s ease;
}

.filter-tab.active {
    background: #667eea;
    color: white;
}

.filter-actions {
    display: flex;
    gap: 20rpx;
}

.filter-picker {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20rpx;
    background: #f8f9fa;
    border-radius: 10rpx;
    border: 2rpx solid #e9ecef;
}

.filter-text {
    font-size: 28rpx;
    color: #333;
}

.filter-arrow {
    font-size: 20rpx;
    color: #666;
}

.coaches-list {
    margin: 0 20rpx;
}

.coach-card {
    background: white;
    border-radius: 20rpx;
    margin-bottom: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.coach-header {
    display: flex;
    align-items: flex-start;
    margin-bottom: 25rpx;
}

.coach-avatar {
    position: relative;
    margin-right: 25rpx;
}

.avatar-img {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
}

.coach-status {
    position: absolute;
    top: -5rpx;
    right: -5rpx;
    padding: 5rpx 12rpx;
    border-radius: 20rpx;
    font-size: 20rpx;
    color: white;
}

.coach-status.upcoming {
    background: #667eea;
}

.coach-status.ongoing {
    background: #f5576c;
}

.coach-status.completed {
    background: #4facfe;
}

.coach-status.cancelled {
    background: #999;
}

.coach-info {
    flex: 1;
}

.coach-name {
    font-size: 32rpx;
    font-weight: 600;
    color: #333;
    margin-bottom: 8rpx;
}

.coach-sport {
    font-size: 28rpx;
    color: #667eea;
    margin-bottom: 12rpx;
}

.coach-rating {
    display: flex;
    align-items: center;
    gap: 15rpx;
}

.stars {
    font-size: 24rpx;
    color: #ffa726;
}

.experience {
    font-size: 24rpx;
    color: #666;
}

.coach-actions {
    display: flex;
    flex-direction: column;
    gap: 10rpx;
}

.action-btn {
    padding: 12rpx 20rpx;
    border-radius: 25rpx;
    font-size: 24rpx;
    text-align: center;
    min-width: 120rpx;
}

.action-btn.cancel {
    background: #ff6b6b;
    color: white;
}

.action-btn.review {
    background: #667eea;
    color: white;
}

.booking-details {
    margin-bottom: 20rpx;
}

.detail-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15rpx 0;
    border-bottom: 1rpx solid #f0f0f0;
}

.detail-item:last-child {
    border-bottom: none;
}

.detail-label {
    font-size: 28rpx;
    color: #666;
}

.detail-value {
    font-size: 28rpx;
    color: #333;
    font-weight: 500;
}

.detail-value.price {
    color: #ff6b6b;
    font-weight: 600;
}

.booking-notes {
    background: #f8f9fa;
    padding: 20rpx;
    border-radius: 10rpx;
    margin-top: 20rpx;
}

.notes-label {
    font-size: 28rpx;
    color: #666;
    margin-right: 10rpx;
}

.notes-content {
    font-size: 28rpx;
    color: #333;
}

.empty-state {
    text-align: center;
    padding: 100rpx 40rpx;
    background: white;
    border-radius: 20rpx;
    margin: 20rpx;
}

.empty-icon {
    font-size: 80rpx;
    display: block;
    margin-bottom: 30rpx;
}

.empty-text {
    font-size: 32rpx;
    color: #333;
    font-weight: 500;
    display: block;
    margin-bottom: 15rpx;
}

.empty-subtext {
    font-size: 28rpx;
    color: #666;
}

.fab-button {
    position: fixed;
    bottom: 120rpx;
    right: 40rpx;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 25rpx 35rpx;
    border-radius: 50rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 8rpx 25rpx rgba(102, 126, 234, 0.3);
    z-index: 1000;
}

.fab-icon {
    font-size: 32rpx;
    font-weight: bold;
    margin-right: 10rpx;
}

.fab-text {
    font-size: 28rpx;
    font-weight: 500;
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
    z-index: 2000;
}

.review-modal {
    background: white;
    border-radius: 20rpx;
    width: 90%;
    max-width: 600rpx;
    max-height: 80vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx;
    border-bottom: 2rpx solid #f0f0f0;
}

.modal-title {
    font-size: 32rpx;
    font-weight: 600;
    color: #333;
}

.modal-close {
    font-size: 40rpx;
    color: #999;
    padding: 0 10rpx;
}

.review-form {
    padding: 30rpx;
}

.rating-section {
    margin-bottom: 40rpx;
}

.rating-label {
    font-size: 28rpx;
    color: #333;
    display: block;
    margin-bottom: 20rpx;
}

.rating-stars {
    display: flex;
    gap: 15rpx;
}

.star {
    font-size: 48rpx;
    color: #ddd;
    cursor: pointer;
    transition: color 0.2s ease;
}

.star.active {
    color: #ffa726;
}

.comment-section {
    margin-bottom: 50rpx;
}

.comment-label {
    font-size: 28rpx;
    color: #333;
    display: block;
    margin-bottom: 20rpx;
}

.comment-input {
    width: 100%;
    height: 200rpx;
    padding: 20rpx;
    border: 2rpx solid #e9ecef;
    border-radius: 10rpx;
    font-size: 28rpx;
    color: #333;
    background: #f8f9fa;
}

.char-count {
    text-align: right;
    font-size: 24rpx;
    color: #999;
    margin-top: 10rpx;
}

.review-actions {
    display: flex;
    gap: 20rpx;
}

.cancel-btn, .submit-btn {
    flex: 1;
    padding: 25rpx;
    border-radius: 10rpx;
    text-align: center;
    font-size: 28rpx;
}

.cancel-btn {
    background: #f8f9fa;
    color: #666;
    border: 2rpx solid #e9ecef;
}

.submit-btn {
    background: #667eea;
    color: white;
}
</style>
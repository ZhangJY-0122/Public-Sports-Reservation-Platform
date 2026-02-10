<template>
    <view class="bookings-container">
        <!-- 顶部导航栏 -->
        <view class="header">
            <view class="back-btn" @click="goBack">←</view>
            <text class="header-title">我的预约</text>
            <view class="calendar-btn" @click="showCalendar = !showCalendar">📅</view>
        </view>

        <!-- 统计卡片 -->
        <view class="stats-section">
            <view class="stat-card">
                <text class="stat-number">{{ totalBookings }}</text>
                <text class="stat-label">总预约数</text>
            </view>
            <view class="stat-card">
                <text class="stat-number">{{ upcomingBookings }}</text>
                <text class="stat-label">即将开始</text>
            </view>
            <view class="stat-card">
                <text class="stat-number">{{ completedBookings }}</text>
                <text class="stat-label">已完成</text>
            </view>
        </view>

        <!-- 筛选标签 -->
        <view class="filter-tabs">
            <view class="filter-tab" 
                  :class="{ active: selectedFilter === 'all' }" 
                  @click="setFilter('all')">
                全部预约
            </view>
            <view class="filter-tab" 
                  :class="{ active: selectedFilter === 'upcoming' }" 
                  @click="setFilter('upcoming')">
                进行中
            </view>
            <view class="filter-tab" 
                  :class="{ active: selectedFilter === 'completed' }" 
                  @click="setFilter('completed')">
                已完成
            </view>
            <view class="filter-tab" 
                  :class="{ active: selectedFilter === 'cancelled' }" 
                  @click="setFilter('cancelled')">
                已取消
            </view>
        </view>

        <!-- 预约列表 -->
        <scroll-view class="bookings-list" scroll-y="true">
            <view class="booking-item" v-for="booking in filteredBookings" :key="booking.id">
                <view class="booking-header">
                    <view class="venue-info">
                        <text class="venue-icon">{{ booking.venueIcon }}</text>
                        <view class="venue-details">
                            <text class="venue-name">{{ booking.venueName }}</text>
                            <text class="venue-type">{{ booking.venueType }}</text>
                        </view>
                    </view>
                    <view class="booking-status" :class="booking.status">
                        {{ booking.statusText }}
                    </view>
                </view>

                <view class="booking-details">
                    <view class="booking-time">
                        <text class="time-label">预约时间</text>
                        <text class="time-value">{{ booking.date }} {{ booking.time }}</text>
                    </view>
                    <view class="booking-duration">
                        <text class="duration-label">时长</text>
                        <text class="duration-value">{{ booking.duration }}</text>
                    </view>
                    <view class="booking-price">
                        <text class="price-label">费用</text>
                        <text class="price-value">¥{{ booking.price }}</text>
                    </view>
                </view>

                <view class="booking-info">
                    <text class="booking-desc">{{ booking.description }}</text>
                </view>

                <view class="booking-actions">
                    <view class="action-btn" 
                          :class="booking.status === 'upcoming' ? 'primary' : 'secondary'"
                          @click="viewBookingDetails(booking)">
                        查看详情
                    </view>
                    <view class="action-btn" 
                          v-if="booking.status === 'upcoming'"
                          @click="modifyBooking(booking)">
                        修改预约
                    </view>
                    <view class="action-btn danger" 
                          v-if="booking.status === 'upcoming'"
                          @click="cancelBooking(booking)">
                        取消预约
                    </view>
                </view>
            </view>

            <!-- 空状态 -->
            <view class="empty-state" v-if="filteredBookings.length === 0">
                <text class="empty-icon">📅</text>
                <text class="empty-text">暂无{{ getFilterText() }}预约</text>
                <text class="empty-subtext">快去预约心仪的场馆吧！</text>
            </view>
        </scroll-view>

        <!-- 快捷预约 -->
        <view class="quick-book">
            <view class="quick-book-btn" @click="quickBooking">
                <text class="btn-icon">+</text>
                <text class="btn-text">快速预约</text>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    name: 'MyBookingsPage',
    data() {
        return {
            showCalendar: false,
            selectedFilter: 'all',
            
            bookingsList: [
                {
                    id: 1,
                    venueName: '中央体育馆A馆',
                    venueType: '篮球场',
                    venueIcon: '🏀',
                    date: '2024-01-15',
                    time: '19:00-21:00',
                    duration: '2小时',
                    price: '200',
                    status: 'upcoming',
                    statusText: '即将开始',
                    description: '和朋友一起打篮球，享受运动乐趣'
                },
                {
                    id: 2,
                    venueName: '游泳中心',
                    venueType: '游泳池',
                    venueIcon: '🏊‍♂️',
                    date: '2024-01-16',
                    time: '14:00-15:30',
                    duration: '1.5小时',
                    price: '80',
                    status: 'upcoming',
                    statusText: '已预约',
                    description: '游泳训练课程，提升游泳技能'
                },
                {
                    id: 3,
                    venueName: '健身中心',
                    venueType: '健身房',
                    venueIcon: '💪',
                    date: '2024-01-14',
                    time: '18:00-19:00',
                    duration: '1小时',
                    price: '50',
                    status: 'completed',
                    statusText: '已完成',
                    description: '力量训练，加强肌肉锻炼'
                },
                {
                    id: 4,
                    venueName: '羽毛球馆',
                    venueType: '羽毛球场',
                    venueIcon: '🏸',
                    date: '2024-01-13',
                    time: '10:00-12:00',
                    duration: '2小时',
                    price: '120',
                    status: 'cancelled',
                    statusText: '已取消',
                    description: '羽毛球比赛，临时有事取消'
                },
                {
                    id: 5,
                    venueName: '瑜伽工作室',
                    venueType: '瑜伽室',
                    venueIcon: '🧘‍♀️',
                    date: '2024-01-17',
                    time: '09:00-10:30',
                    duration: '1.5小时',
                    price: '100',
                    status: 'upcoming',
                    statusText: '已预约',
                    description: '放松身心的瑜伽课程'
                },
                {
                    id: 6,
                    venueName: '网球场',
                    venueType: '网球场',
                    venueIcon: '🎾',
                    date: '2024-01-12',
                    time: '16:00-18:00',
                    duration: '2小时',
                    price: '180',
                    status: 'completed',
                    statusText: '已完成',
                    description: '网球训练，学习新技术'
                }
            ]
        }
    },
    computed: {
        totalBookings() {
            return this.bookingsList.length
        },
        
        upcomingBookings() {
            return this.bookingsList.filter(booking => booking.status === 'upcoming').length
        },
        
        completedBookings() {
            return this.bookingsList.filter(booking => booking.status === 'completed').length
        },
        
        filteredBookings() {
            let filtered = this.bookingsList
            
            if (this.selectedFilter !== 'all') {
                filtered = filtered.filter(booking => booking.status === this.selectedFilter)
            }
            
            return filtered
        }
    },
    methods: {
        goBack() {
            uni.navigateBack()
        },
        
        setFilter(filter) {
            this.selectedFilter = filter
        },
        
        getFilterText() {
            switch (this.selectedFilter) {
                case 'upcoming': return '即将开始'
                case 'completed': return '已完成'
                case 'cancelled': return '已取消'
                default: return ''
            }
        },
        
        viewBookingDetails(booking) {
            uni.showModal({
                title: '预约详情',
                content: `场馆：${booking.venueName}\n类型：${booking.venueType}\n时间：${booking.date} ${booking.time}\n时长：${booking.duration}\n费用：¥${booking.price}\n\n${booking.description}`,
                showCancel: false
            })
        },
        
        modifyBooking(booking) {
            uni.showModal({
                title: '修改预约',
                content: `确定要修改"${booking.venueName}"的预约吗？`,
                success: (res) => {
                    if (res.confirm) {
                        uni.showToast({
                            title: '跳转到修改页面...',
                            icon: 'none'
                        })
                    }
                }
            })
        },
        
        cancelBooking(booking) {
            uni.showModal({
                title: '取消预约',
                content: `确定要取消"${booking.venueName}"的预约吗？\n（取消政策可能产生费用）`,
                success: (res) => {
                    if (res.confirm) {
                        const index = this.bookingsList.findIndex(b => b.id === booking.id)
                        if (index !== -1) {
                            this.bookingsList[index].status = 'cancelled'
                            this.bookingsList[index].statusText = '已取消'
                        }
                        
                        uni.showToast({
                            title: '预约已取消',
                            icon: 'success'
                        })
                        
                        uni.vibrateShort()
                    }
                }
            })
        },
        
        quickBooking() {
            uni.showModal({
                title: '快速预约',
                content: '即将跳转到场馆列表选择心仪场地...',
                showCancel: false
            })
        }
    }
}
</script>

<style scoped>
.bookings-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 顶部导航栏 */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20rpx 30rpx;
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: #fff;
}

.back-btn {
    width: 80rpx;
    height: 80rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    font-size: 36rpx;
}

.header-title {
    font-size: 36rpx;
    font-weight: bold;
}

.calendar-btn {
    width: 80rpx;
    height: 80rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    font-size: 36rpx;
}

/* 统计卡片 */
.stats-section {
    display: flex;
    padding: 30rpx;
    gap: 20rpx;
}

.stat-card {
    flex: 1;
    background: #fff;
    border-radius: 20rpx;
    padding: 30rpx 20rpx;
    text-align: center;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.stat-number {
    font-size: 48rpx;
    font-weight: bold;
    color: #4a90e2;
    display: block;
    margin-bottom: 10rpx;
}

.stat-label {
    font-size: 26rpx;
    color: #666;
    display: block;
}

/* 筛选标签 */
.filter-tabs {
    display: flex;
    background: #fff;
    padding: 20rpx 30rpx;
    border-bottom: 1px solid #e1e8ed;
}

.filter-tab {
    flex: 1;
    text-align: center;
    padding: 15rpx 0;
    background: #f8f9fa;
    color: #666;
    border-radius: 25rpx;
    font-size: 28rpx;
    margin: 0 5rpx;
    border: 2rpx solid transparent;
}

.filter-tab.active {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: #fff;
}

/* 预约列表 */
.bookings-list {
    flex: 1;
    padding: 30rpx;
    height: calc(100vh - 400rpx);
}

.booking-item {
    background: #fff;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.booking-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20rpx;
}

.venue-info {
    display: flex;
    align-items: center;
}

.venue-icon {
    font-size: 60rpx;
    margin-right: 20rpx;
}

.venue-details {
    flex: 1;
}

.venue-name {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.venue-type {
    font-size: 26rpx;
    color: #666;
    display: block;
}

.booking-status {
    padding: 8rpx 16rpx;
    border-radius: 20rpx;
    font-size: 24rpx;
    font-weight: bold;
}

.booking-status.upcoming {
    background: #e3f2fd;
    color: #1976d2;
}

.booking-status.completed {
    background: #f3e5f5;
    color: #7b1fa2;
}

.booking-status.cancelled {
    background: #ffebee;
    color: #c62828;
}

.booking-details {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20rpx;
    padding: 20rpx;
    background: #f8f9fa;
    border-radius: 15rpx;
}

.booking-time,
.booking-duration,
.booking-price {
    text-align: center;
    flex: 1;
}

.time-label,
.duration-label,
.price-label {
    font-size: 24rpx;
    color: #999;
    display: block;
    margin-bottom: 8rpx;
}

.time-value,
.duration-value,
.price-value {
    font-size: 26rpx;
    color: #333;
    font-weight: bold;
    display: block;
}

.booking-info {
    margin-bottom: 20rpx;
}

.booking-desc {
    font-size: 28rpx;
    color: #666;
    display: block;
    line-height: 1.5;
}

.booking-actions {
    display: flex;
    gap: 15rpx;
}

.action-btn {
    flex: 1;
    text-align: center;
    padding: 15rpx 0;
    border-radius: 25rpx;
    font-size: 28rpx;
    font-weight: bold;
}

.action-btn.primary {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: #fff;
}

.action-btn.secondary {
    background: #f8f9fa;
    color: #666;
    border: 2rpx solid #e1e8ed;
}

.action-btn.danger {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
    color: #fff;
}

/* 空状态 */
.empty-state {
    text-align: center;
    padding: 100rpx 30rpx;
}

.empty-icon {
    font-size: 120rpx;
    display: block;
    margin-bottom: 30rpx;
}

.empty-text {
    font-size: 32rpx;
    color: #333;
    display: block;
    margin-bottom: 15rpx;
}

.empty-subtext {
    font-size: 26rpx;
    color: #666;
    display: block;
}

/* 快捷预约 */
.quick-book {
    padding: 30rpx;
    background: #fff;
    border-top: 1px solid #e1e8ed;
}

.quick-book-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: #fff;
    padding: 25rpx;
    border-radius: 25rpx;
    font-size: 32rpx;
    font-weight: bold;
}

.btn-icon {
    font-size: 40rpx;
    margin-right: 15rpx;
}

/* 点击效果 */
.back-btn:active,
.calendar-btn:active,
.filter-tab:active,
.action-btn:active,
.quick-book-btn:active {
    transform: scale(0.95);
}
</style>
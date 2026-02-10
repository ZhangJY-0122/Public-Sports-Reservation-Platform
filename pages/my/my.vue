<template>
    <view class="user-center-container">
        <!-- 顶部导航栏 -->
        <view class="header">
            <view class="back-btn" @click="goBack">←</view>
            <text class="header-title">用户中心</text>
            <view class="settings-btn" @click="openSettings">⚙️</view>
        </view>

        <!-- 用户信息区域 -->
        <view class="user-info">
            <view class="avatar-container">
                <view class="avatar">🏃‍♂️</view>
                <view class="status-badge"></view>
            </view>
            <text class="user-name">{{ userInfo.name }}</text>
            <view class="user-level">VIP会员</view>
            
            <view class="user-stats">
                <view class="stat-item">
                    <text class="stat-number">{{ userInfo.exerciseDays }}</text>
                    <text class="stat-label">运动天数</text>
                </view>
                <view class="stat-item">
                    <text class="stat-number">{{ userInfo.friendsCount }}</text>
                    <text class="stat-label">好友数量</text>
                </view>
                <view class="stat-item">
                    <text class="stat-number">{{ userInfo.points }}</text>
                    <text class="stat-label">积分</text>
                </view>
            </view>
        </view>

        <!-- 功能菜单区域 -->
        <view class="menu-section">
            <text class="menu-title">我的服务</text>
            <view class="menu-list">
                <view class="menu-item" @click="navigateTo('my-activities')">
                    <view class="menu-icon my-activities">📅</view>
                    <view class="menu-content">
                        <text class="menu-title-text">我的活动</text>
                        <text class="menu-subtitle">参与的运动活动记录</text>
                    </view>
                    <view class="menu-badge" v-if="pendingActivities > 0">{{ pendingActivities }}</view>
                    <text class="menu-arrow">›</text>
                </view>
                
           <!--     <view class="menu-item" @click="navigateTo('my-friends')">
                    <view class="menu-icon my-friends">👥</view>
                    <view class="menu-content">
                        <text class="menu-title-text">我的朋友</text>
                        <text class="menu-subtitle">运动伙伴和好友列表</text>
                    </view>
                    <text class="menu-arrow">›</text>
                </view> -->
                
                <view class="menu-item" @click="navigateTo('my-bookings')">
                    <view class="menu-icon my-bookings">📋</view>
                    <view class="menu-content">
                        <text class="menu-title-text">我的预约</text>
                        <text class="menu-subtitle">场地预约和管理</text>
                    </view>
                    <view class="menu-badge" v-if="pendingBookings > 0">{{ pendingBookings }}</view>
                    <text class="menu-arrow">›</text>
                </view>
                
                <view class="menu-item" @click="navigateTo('my-events')">
                    <view class="menu-icon my-events">🏆</view>
                    <view class="menu-content">
                        <text class="menu-title-text">我的赛事</text>
                        <text class="menu-subtitle">报名和参与的赛事</text>
                    </view>
                    <text class="menu-arrow">›</text>
                </view>
                <view class="menu-item" @click="navigateTo('coach')">
                    <view class="menu-icon my-bills">👥</view>
                    <view class="menu-content">
                        <text class="menu-title-text">预约教练</text>
                        <text class="menu-subtitle">我预约的教练</text>
                    </view>
                    <text class="menu-arrow">›</text>
                </view>
           <!--    <view class="menu-item" @click="navigateTo('my-bills')">
                    <view class="menu-icon my-bills">💳</view>
                    <view class="menu-content">
                        <text class="menu-title-text">我的费用单</text>
                        <text class="menu-subtitle">账单明细和支付记录</text>
                    </view>
                    <text class="menu-arrow">›</text>
                </view> -->
            </view>
        </view>

        <!-- 快捷操作区域 -->
        <view class="quick-actions">
            <text class="quick-actions-title">快捷操作</text>
            <view class="action-grid">
                <view class="action-item" @click="quickAction('book-venue')">
                    <text class="action-icon">🏟️</text>
                    <text class="action-text">预约场地</text>
                </view>
                <view class="action-item" @click="quickAction('join-activity')">
                    <text class="action-icon">🎯</text>
                    <text class="action-text">发起活动</text>
                </view>
                <view class="action-item" @click="quickAction('find-friends')">
                    <text class="action-icon">🔍</text>
                    <text class="action-text">找朋友</text>
                </view>
            </view>
        </view>

      
    </view>
</template>

<script>
export default {
    name: 'UserCenter',
    data() {
        return {
            userInfo: {
                name: '运动达人',
                exerciseDays: 128,
                friendsCount: 45,
                points: 892
            },
            pendingActivities: 3,
            pendingBookings: 2
        }
    },
    onLoad() {
        // 页面加载时获取用户数据
        this.loadUserData()
    },
    methods: {
        goBack() {
            uni.navigateBack()
        },
        
        openSettings() {
            uni.showToast({
                title: '设置功能开发中',
                icon: 'none'
            })
        },
        
        navigateTo(module) {
            // 添加点击反馈
            this.addClickFeedback()
            
            const routes = {
                'my-activities': '/pages/my/activities',
                'my-friends': '/pages/my/friends',
                'my-bookings': '/pages/my/bookin',
                'my-events': '/pages/my/events',
                'my-bills': '/pages/my/fee',
				"coach":"pages/my/coach"
            }
            
            const titles = {
                'my-activities': '我的活动',
                'my-friends': '我的朋友',
                'my-bookings': '我的预约',
                'my-events': '我的赛事',
                'my-bills': '我的费用单'
            }
			

            
           uni.navigateTo({
           	"url":routes[module]
           })
        },
        
        quickAction(action) {
            this.addClickFeedback()
            
            const messages = {
                'book-venue': '快速预约场地',
                'join-activity': '快速参加活动',
                'find-friends': '快速寻找朋友'
            }
            
            uni.showModal({
                title: '快捷操作',
                content: `${messages[action]}\n\n这是快捷操作功能演示。\n在实际应用中，这里会直接跳转到相应功能。`,
                showCancel: false
            })
        },
        
        addClickFeedback() {
            // 点击反馈效果
            setTimeout(() => {
                uni.vibrateShort()
            }, 50)
        },
        
        loadUserData() {
            // 模拟加载用户数据
            uni.showLoading({
                title: '加载中...'
            })
            
            setTimeout(() => {
                uni.hideLoading()
                // 这里可以调用API获取真实的用户数据
                console.log('用户数据加载完成')
            }, 1000)
        }
    }
}
</script>

<style scoped>
.user-center-container {
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

.settings-btn {
    width: 80rpx;
    height: 80rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    font-size: 36rpx;
}

/* 用户信息区域 */
.user-info {
    padding: 80rpx 60rpx 60rpx;
    text-align: center;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.avatar-container {
    position: relative;
    display: inline-block;
    margin-bottom: 40rpx;
}

.avatar {
    width: 160rpx;
    height: 160rpx;
    border-radius: 50%;
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 72rpx;
    color: #fff;
    border: 8rpx solid #fff;
}

.status-badge {
    position: absolute;
    bottom: 10rpx;
    right: 10rpx;
    width: 40rpx;
    height: 40rpx;
    background: #28a745;
    border-radius: 50%;
    border: 6rpx solid #fff;
}

.user-name {
    font-size: 40rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
    display: block;
}

.user-level {
    display: inline-block;
    padding: 8rpx 24rpx;
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
    color: #fff;
    border-radius: 24rpx;
    font-size: 24rpx;
    font-weight: bold;
}

.user-stats {
    display: flex;
    justify-content: space-around;
    margin-top: 40rpx;
    padding-top: 40rpx;
    border-top: 2rpx solid #e1e8ed;
}

.stat-item {
    text-align: center;
}

.stat-number {
    font-size: 36rpx;
    font-weight: bold;
    color: #4a90e2;
    display: block;
}

.stat-label {
    font-size: 24rpx;
    color: #666;
    margin-top: 8rpx;
}

/* 功能菜单区域 */
.menu-section {
    padding: 40rpx 0;
}

.menu-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin: 0 60rpx 30rpx;
}

.menu-list {
    background: #fff;
}

.menu-item {
    display: flex;
    align-items: center;
    padding: 36rpx 60rpx;
    border-bottom: 2rpx solid #f1f3f4;
    position: relative;
}

.menu-item:last-child {
    border-bottom: none;
}

.menu-icon {
    width: 80rpx;
    height: 80rpx;
    border-radius: 24rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40rpx;
    margin-right: 30rpx;
    color: #fff;
}

.menu-icon.my-activities {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
}

.menu-icon.my-friends {
    background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
}

.menu-icon.my-bookings {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
}

.menu-icon.my-events {
    background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
}

.menu-icon.my-bills {
    background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
}

.menu-content {
    flex: 1;
}

.menu-title-text {
    font-size: 32rpx;
    font-weight: 500;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.menu-subtitle {
    font-size: 26rpx;
    color: #666;
    display: block;
}

.menu-badge {
    background: #ff4757;
    color: #fff;
    padding: 4rpx 16rpx;
    border-radius: 20rpx;
    font-size: 22rpx;
    font-weight: bold;
    margin-right: 20rpx;
}

.menu-arrow {
    color: #ccc;
    font-size: 32rpx;
    margin-left: 20rpx;
}

/* 快捷操作区域 */
.quick-actions {
    padding: 40rpx 60rpx 60rpx;
    background: #f8f9fa;
}

.quick-actions-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 30rpx;
}

.action-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30rpx;
}

.action-item {
    text-align: center;
    padding: 40rpx 20rpx;
    background: #fff;
    border-radius: 24rpx;
    border: 4rpx solid transparent;
}

.action-icon {
    font-size: 48rpx;
    margin-bottom: 16rpx;
    display: block;
}

.action-text {
    font-size: 24rpx;
    color: #666;
    display: block;
}

/* 功能描述 */
.features-section {
    background: #f8f9fa;
    padding: 40rpx 60rpx;
    border-top: 2rpx solid #e1e8ed;
}

.features-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 30rpx;
}

.features-list {
    background: #fff;
    padding: 40rpx;
    border-radius: 24rpx;
}

.feature-item {
    font-size: 28rpx;
    color: #666;
    margin-bottom: 16rpx;
    display: block;
    line-height: 1.5;
}

.feature-item:last-child {
    margin-bottom: 0;
}

/* 点击效果 */
.menu-item:active {
    background: #f8f9fa;
    transform: scale(0.98);
}

.action-item:active {
    transform: scale(0.95);
    border-color: #4a90e2;
}

.back-btn:active,
.settings-btn:active {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(0.95);
}
</style>
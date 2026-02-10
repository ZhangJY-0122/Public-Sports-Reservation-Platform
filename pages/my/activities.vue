<template>
    <view class="activities-container">
        <!-- 顶部导航栏 -->
        <view class="header">
            <view class="back-btn" @click="goBack">←</view>
            <text class="header-title">我的活动</text>
            <view class="filter-btn" @click="showFilter = !showFilter">🔍</view>
        </view>

        <!-- 统计卡片 -->
        <view class="stats-section">
            <view class="stat-card">
                <text class="stat-number">{{ totalActivities }}</text>
                <text class="stat-label">参与活动</text>
            </view>
            <view class="stat-card">
                <text class="stat-number">{{ upcomingActivities }}</text>
                <text class="stat-label">即将开始</text>
            </view>
            <view class="stat-card">
                <text class="stat-number">{{ completedActivities }}</text>
                <text class="stat-label">已完成</text>
            </view>
        </view>

        <!-- 筛选选项 -->
        <view class="filter-section" v-show="showFilter">
            <view class="filter-tabs">
                <view class="filter-tab" 
                      :class="{ active: selectedFilter === 'all' }" 
                      @click="setFilter('all')">
                    全部活动
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
            </view>
        </view>

        <!-- 活动列表 -->
        <scroll-view class="activities-list" scroll-y="true">
            <view class="activity-item" v-for="activity in filteredActivities" :key="activity.id">
                <view class="activity-header">
                    <view class="activity-icon">
                        <text class="icon-emoji">{{ activity.icon }}</text>
                    </view>
                    <view class="activity-info">
                        <text class="activity-title">{{ activity.title }}</text>
                        <text class="activity-time">{{ activity.time }}</text>
                        <text class="activity-location">📍 {{ activity.location }}</text>
                    </view>
                    <view class="activity-status" :class="activity.status">
                        {{ activity.statusText }}
                    </view>
                </view>
                
                <view class="activity-details">
                    <text class="activity-description">{{ activity.description }}</text>
                    <view class="activity-stats">
                        <text class="participant-count">👥 {{ activity.current_participants }}人参与</text>
                        <text class="activity-date">活动日期:{{ activity.start_date }}</text>
                    </view>
                </view>

                <view class="activity-actions">
                <!--    <view class="action-btn primary" @click="viewDetails(activity)">
                        查看详情
                    </view> -->
                    <view class="action-btn secondary" @click="joinActivity(activity)">
                        {{ activity.isJoined ? '已参与' : '立即参与' }}
                    </view>
                </view>
            </view>

            <!-- 空状态 -->
            <view class="empty-state" v-if="filteredActivities.length === 0">
                <text class="empty-icon">🎯</text>
                <text class="empty-text">暂无{{ getFilterText() }}活动</text>
                <text class="empty-subtext">快去发现新的运动活动吧！</text>
            </view>
        </scroll-view>

        <!-- 底部操作栏 -->
        <view class="bottom-actions">
            <view class="create-activity-btn" @click="createActivity">
                <text class="btn-text">+ 创建活动</text>
            </view>
        </view>
    </view>
</template>

<script>
	import { http } from '@/utils/http.js'
export default {
	
    name: 'MyActivitiesPage',
    data() {
        return {
            showFilter: false,
            selectedFilter: 'all',
            
            activitiesList: [
                {
                    id: 1,
                    title: '晨跑健身团',
                    icon: '🏃‍♂️',
                    time: '每天 06:00-07:30',
                    location: '中央公园',
                    status: 'upcoming',
                    statusText: '即将开始',
                    description: '每天早上与运动爱好者一起晨跑，分享健康生活方式',
                    participantCount: 15,
                    date: '2024-01-15',
                    isJoined: true
                },
                {
                    id: 2,
                    title: '篮球友谊赛',
                    icon: '🏀',
                    time: '每周二、四 19:00-21:00',
                    location: '体育馆A馆',
                    status: 'upcoming',
                    statusText: '报名中',
                    description: '篮球爱好者聚会，无论你是新手还是高手都欢迎参加',
                    participantCount: 22,
                    date: '2024-01-16',
                    isJoined: false
                },
                {
                    id: 3,
                    title: '瑜伽放松课程',
                    icon: '🧘‍♀️',
                    time: '每周六 09:00-10:30',
                    location: '瑜伽工作室',
                    status: 'completed',
                    statusText: '已完成',
                    description: '专业瑜伽老师指导，帮助身心放松，提升柔韧性',
                    participantCount: 8,
                    date: '2024-01-13',
                    isJoined: true
                },
                {
                    id: 4,
                    title: '游泳训练班',
                    icon: '🏊‍♂️',
                    time: '每周一、三、五 18:00-19:30',
                    location: '游泳馆',
                    status: 'upcoming',
                    statusText: '进行中',
                    description: '专业游泳教练指导，提升游泳技能，适合各水平',
                    participantCount: 12,
                    date: '2024-01-17',
                    isJoined: true
                },
                {
                    id: 5,
                    title: '徒步登山团',
                    icon: '🥾',
                    time: '每周日 08:00-16:00',
                    location: '山国家森林公园',
                    status: 'completed',
                    statusText: '已完成',
                    description: '挑战自我，享受自然美景，与朋友一起徒步探险',
                    participantCount: 18,
                    date: '2024-01-14',
                    isJoined: false
                }
            ]
        }
    },
    computed: {
        totalActivities() {
            return this.activitiesList.length
        },
        
        upcomingActivities() {
            return this.activitiesList.filter(activity => activity.status === 'upcoming').length
        },
        
        completedActivities() {
            return this.activitiesList.filter(activity => activity.status === 'completed').length
        },
        
        filteredActivities() {
            let filtered = this.activitiesList
            
            if (this.selectedFilter === 'upcoming') {
                filtered = filtered.filter(activity => activity.status === 'upcoming')
            } else if (this.selectedFilter === 'completed') {
                filtered = filtered.filter(activity => activity.status === 'completed')
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
            this.showFilter = false
        },
        
        getFilterText() {
            switch (this.selectedFilter) {
                case 'upcoming': return '即将开始'
                case 'completed': return '已完成'
                default: return ''
            }
        },
        
        viewDetails(activity) {
            uni.showModal({
                title: '活动详情',
                content: `${activity.title}\n\n时间：${activity.time}\n地点：${activity.location}\n\n${activity.description}\n\n参与人数：${activity.participantCount}人`,
                showCancel: false
            })
        },
        
        joinActivity(activity) {
            if (activity.isJoined) {
                uni.showToast({
                    title: '您已参与此活动',
                    icon: 'none'
                })
                return
            }
            
            uni.showModal({
                title: '加入活动',
                content: `确定要加入"${activity.title}"吗？`,
                success: (res) => {
                    if (res.confirm) {
                        const index = this.activitiesList.findIndex(a => a.id === activity.id)
                        if (index !== -1) {
                            this.activitiesList[index].isJoined = true
                            this.activitiesList[index].participantCount += 1
                        }
                        
                        uni.showToast({
                            title: '加入成功！',
                            icon: 'success'
                        })
                        
                        uni.vibrateShort()
                    }
                }
            })
        },
        
        createActivity() {
          uni.navigateTo({
          	url:"/pages/activity/activity"
          })
        },
		loaddata(){
			http.get("activity/list ").then(res=>{
				this.activitiesList=res.activities
			})
		}
    },
	onLoad() {
		this.loaddata()
	}
}
</script>

<style scoped>
.activities-container {
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

.filter-btn {
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

/* 筛选选项 */
.filter-section {
    background: #fff;
    padding: 20rpx 30rpx;
    border-bottom: 1px solid #e1e8ed;
}

.filter-tabs {
    display: flex;
    gap: 20rpx;
}

.filter-tab {
    flex: 1;
    text-align: center;
    padding: 15rpx 0;
    background: #f8f9fa;
    color: #666;
    border-radius: 25rpx;
    font-size: 28rpx;
    border: 2rpx solid transparent;
}

.filter-tab.active {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: #fff;
}

/* 活动列表 */
.activities-list {
    flex: 1;
    padding: 30rpx;
}

.activity-item {
    background: #fff;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.activity-header {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.activity-icon {
    margin-right: 20rpx;
}

.icon-emoji {
    font-size: 60rpx;
    display: block;
}

.activity-info {
    flex: 1;
}

.activity-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.activity-time {
    font-size: 26rpx;
    color: #666;
    display: block;
    margin-bottom: 8rpx;
}

.activity-location {
    font-size: 24rpx;
    color: #999;
    display: block;
}

.activity-status {
    padding: 8rpx 16rpx;
    border-radius: 20rpx;
    font-size: 24rpx;
    font-weight: bold;
}

.activity-status.upcoming {
    background: #e3f2fd;
    color: #1976d2;
}

.activity-status.completed {
    background: #f3e5f5;
    color: #7b1fa2;
}

.activity-details {
    margin-bottom: 20rpx;
}

.activity-description {
    font-size: 28rpx;
    color: #666;
    display: block;
    margin-bottom: 15rpx;
    line-height: 1.5;
}

.activity-stats {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.participant-count {
    font-size: 24rpx;
    color: #999;
}

.activity-date {
    font-size: 24rpx;
    color: #999;
}

.activity-actions {
    display: flex;
    gap: 20rpx;
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

/* 底部操作栏 */
.bottom-actions {
    padding: 30rpx;
    background: #fff;
    border-top: 1px solid #e1e8ed;
}

.create-activity-btn {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: #fff;
    text-align: center;
    padding: 25rpx;
    border-radius: 25rpx;
    font-size: 32rpx;
    font-weight: bold;
}

/* 点击效果 */
.back-btn:active,
.filter-btn:active,
.action-btn:active,
.create-activity-btn:active {
    transform: scale(0.95);
}

.filter-tab:active {
    transform: scale(0.98);
}
</style>
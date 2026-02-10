<template>
    <view class="competitions-container">
        <!-- 顶部导航栏 -->
        <view class="header">
            <view class="back-btn" @click="goBack">←</view>
            <text class="header-title">我的赛事</text>
            <view class="trophy-btn" @click="showTrophies">🏆</view>
        </view>

        <!-- 统计卡片 -->
        <view class="stats-section">
            <view class="stat-card">
                <text class="stat-number">{{ totalCompetitions }}</text>
                <text class="stat-label">参加赛事</text>
            </view>
            <view class="stat-card">
                <text class="stat-number">{{ wonCompetitions }}</text>
                <text class="stat-label">获得名次</text>
            </view>
            <view class="stat-card">
                <text class="stat-number">{{ upcomingCompetitions }}</text>
                <text class="stat-label">即将开始</text>
            </view>
        </view>

        <!-- 筛选标签 -->
        <view class="filter-tabs">
            <view class="filter-tab" 
                  :class="{ active: selectedFilter === 'all' }" 
                  @click="setFilter('all')">
                全部赛事
            </view>
            <view class="filter-tab" 
                  :class="{ active: selectedFilter === 'upcoming' }" 
                  @click="setFilter('upcoming')">
                即将开始
            </view>
            <view class="filter-tab" 
                  :class="{ active: selectedFilter === 'ongoing' }" 
                  @click="setFilter('ongoing')">
                进行中
            </view>
            <view class="filter-tab" 
                  :class="{ active: selectedFilter === 'completed' }" 
                  @click="setFilter('completed')">
                已结束
            </view>
        </view>

        <!-- 赛事列表 -->
        <scroll-view class="competitions-list" scroll-y="true">
            <view class="competition-item" v-for="competition in filteredCompetitions" :key="competition.id">
                <view class="competition-header">
                    <view class="competition-icon">
                        <text class="icon-emoji">{{ competition.icon }}</text>
                    </view>
                    <view class="competition-info">
                        <text class="competition-title">{{ competition.title }}</text>
                        <text class="competition-type">{{ competition.type }}</text>
                        <text class="competition-level">🏅 {{ competition.level }}</text>
                    </view>
                    <view class="competition-status" :class="competition.status">
                        {{ competition.statusText }}
                    </view>
                </view>

                <view class="competition-details">
                    <view class="detail-item">
                        <text class="detail-label">📅 日期</text>
                        <text class="detail-value">{{ competition.date }}</text>
                    </view>
                    <view class="detail-item">
                        <text class="detail-label">🕒 时间</text>
                        <text class="detail-value">{{ competition.time }}</text>
                    </view>
                    <view class="detail-item">
                        <text class="detail-label">📍 地点</text>
                        <text class="detail-value">{{ competition.location }}</text>
                    </view>
                    <view class="detail-item">
                        <text class="detail-label">👥 参与人数</text>
                        <text class="detail-value">{{ competition.participants }}人</text>
                    </view>
                </view>

                <view class="competition-prizes" v-if="competition.status === 'completed'">
                    <text class="prize-label">🏆 获奖情况</text>
                    <text class="prize-value" :class="competition.result">
                        {{ competition.resultText }}
                    </text>
                </view>

                <view class="competition-actions">
                    <view class="action-btn primary" @click="viewDetails(competition)">
                        查看详情
                    </view>
                    <view class="action-btn secondary" @click="shareCompetition(competition)">
                        分享赛事
                    </view>
                    <view class="action-btn" 
                          :class="competition.isJoined ? 'joined' : 'join'"
                          @click="toggleJoin(competition)">
                        {{ competition.isJoined ? '已报名' : '立即报名' }}
                    </view>
                </view>
            </view>

            <!-- 空状态 -->
            <view class="empty-state" v-if="filteredCompetitions.length === 0">
                <text class="empty-icon">🏆</text>
                <text class="empty-text">暂无{{ getFilterText() }}赛事</text>
                <text class="empty-subtext">快去挑战自我，赢取荣誉吧！</text>
            </view>
        </scroll-view>

        <!-- 排行榜浮动按钮 -->
        <view class="floating-btn" @click="showRanking">
            <text class="btn-text">📊</text>
        </view>
    </view>
</template>

<script>
export default {
    name: 'MyCompetitionsPage',
    data() {
        return {
            selectedFilter: 'all',
            
            competitionsList: [
                {
                    id: 1,
                    title: '城市篮球联赛',
                    type: '篮球',
                    icon: '🏀',
                    level: '市级',
                    date: '2024-01-20',
                    time: '09:00-18:00',
                    location: '市体育中心篮球馆',
                    participants: 128,
                    status: 'upcoming',
                    statusText: '即将开始',
                    isJoined: true,
                    result: '',
                    resultText: ''
                },
                {
                    id: 2,
                    title: '年度游泳锦标赛',
                    type: '游泳',
                    icon: '🏊‍♂️',
                    level: '省级',
                    date: '2024-01-25',
                    time: '08:00-17:00',
                    location: '省游泳中心',
                    participants: 85,
                    status: 'upcoming',
                    statusText: '报名中',
                    isJoined: false,
                    result: '',
                    resultText: ''
                },
                {
                    id: 3,
                    title: '羽毛球友谊赛',
                    type: '羽毛球',
                    icon: '🏸',
                    level: '区级',
                    date: '2024-01-18',
                    time: '14:00-17:00',
                    location: '社区体育馆',
                    participants: 64,
                    status: 'ongoing',
                    statusText: '进行中',
                    isJoined: true,
                    result: '',
                    resultText: ''
                },
                {
                    id: 4,
                    title: '晨跑挑战赛',
                    type: '跑步',
                    icon: '🏃‍♂️',
                    level: '市级',
                    date: '2024-01-10',
                    time: '06:00-08:00',
                    location: '城市公园',
                    participants: 256,
                    status: 'completed',
                    statusText: '已结束',
                    isJoined: true,
                    result: 'gold',
                    resultText: '🥇 第3名'
                },
                {
                    id: 5,
                    title: '瑜伽体式大赛',
                    type: '瑜伽',
                    icon: '🧘‍♀️',
                    level: '俱乐部',
                    date: '2024-01-15',
                    time: '10:00-16:00',
                    location: '瑜伽学院',
                    participants: 32,
                    status: 'completed',
                    statusText: '已结束',
                    isJoined: true,
                    result: 'silver',
                    resultText: '🥈 第2名'
                },
                {
                    id: 6,
                    title: '网球公开赛',
                    type: '网球',
                    icon: '🎾',
                    level: '省级',
                    date: '2024-02-01',
                    time: '09:00-18:00',
                    location: '网球中心',
                    participants: 156,
                    status: 'upcoming',
                    statusText: '报名中',
                    isJoined: false,
                    result: '',
                    resultText: ''
                },
                {
                    id: 7,
                    title: '足球杯赛',
                    type: '足球',
                    icon: '⚽',
                    level: '市级',
                    date: '2024-01-12',
                    time: '15:00-17:00',
                    location: '市体育场',
                    participants: 192,
                    status: 'completed',
                    statusText: '已结束',
                    isJoined: true,
                    result: 'bronze',
                    resultText: '🥉 第5名'
                }
            ]
        }
    },
    computed: {
        totalCompetitions() {
            return this.competitionsList.length
        },
        
        wonCompetitions() {
            return this.competitionsList.filter(comp => comp.result === 'gold' || comp.result === 'silver' || comp.result === 'bronze').length
        },
        
        upcomingCompetitions() {
            return this.competitionsList.filter(comp => comp.status === 'upcoming').length
        },
        
        filteredCompetitions() {
            let filtered = this.competitionsList
            
            if (this.selectedFilter !== 'all') {
                filtered = filtered.filter(comp => comp.status === this.selectedFilter)
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
                case 'ongoing': return '进行中'
                case 'completed': return '已结束'
                default: return ''
            }
        },
        
        viewDetails(competition) {
            const resultInfo = competition.result ? `\n获奖情况：${competition.resultText}` : ''
            uni.showModal({
                title: '赛事详情',
                content: `${competition.title}\n类型：${competition.type}\n级别：${competition.level}\n日期：${competition.date}\n时间：${competition.time}\n地点：${competition.location}\n参与人数：${competition.participants}人${resultInfo}`,
                showCancel: false
            })
        },
        
        shareCompetition(competition) {
            uni.showModal({
                title: '分享赛事',
                content: `我参加了"${competition.title}"，快来一起挑战吧！`,
                showCancel: false
            })
        },
        
        toggleJoin(competition) {
            if (competition.isJoined) {
                uni.showModal({
                    title: '取消报名',
                    content: `确定要取消"${competition.title}"的报名吗？`,
                    success: (res) => {
                        if (res.confirm) {
                            const index = this.competitionsList.findIndex(c => c.id === competition.id)
                            if (index !== -1) {
                                this.competitionsList[index].isJoined = false
                            }
                            
                            uni.showToast({
                                title: '已取消报名',
                                icon: 'success'
                            })
                            
                            uni.vibrateShort()
                        }
                    }
                })
            } else {
                uni.showModal({
                    title: '报名赛事',
                    content: `确定要报名参加"${competition.title}"吗？`,
                    success: (res) => {
                        if (res.confirm) {
                            const index = this.competitionsList.findIndex(c => c.id === competition.id)
                            if (index !== -1) {
                                this.competitionsList[index].isJoined = true
                            }
                            
                            uni.showToast({
                                title: '报名成功！',
                                icon: 'success'
                            })
                            
                            uni.vibrateShort()
                        }
                    }
                })
            }
        },
        
        showTrophies() {
            uni.showModal({
                title: '荣誉榜',
                content: `🥇 金牌：${this.competitionsList.filter(c => c.result === 'gold').length}个\n🥈 银牌：${this.competitionsList.filter(c => c.result === 'silver').length}个\n🥉 铜牌：${this.competitionsList.filter(c => c.result === 'bronze').length}个`,
                showCancel: false
            })
        },
        
        showRanking() {
            uni.showModal({
                title: '个人排行',
                content: '当前排名：第15名\n本月积分：285分\n运动类型：多项全能\n\n继续加油，冲击前十！',
                showCancel: false
            })
        }
    }
}
</script>

<style scoped>
.competitions-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 顶部导航栏 */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20rpx 30rpx;
    background: linear-gradient(135deg, #ff6b35 0%, #d63031 100%);
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

.trophy-btn {
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
    color: #ff6b35;
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
    background: linear-gradient(135deg, #ff6b35 0%, #d63031 100%);
    color: #fff;
}

/* 赛事列表 */
.competitions-list {
    flex: 1;
    padding: 30rpx;
    height: calc(100vh - 400rpx);
}

.competition-item {
    background: #fff;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
    position: relative;
}

.competition-header {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.competition-icon {
    margin-right: 20rpx;
}

.icon-emoji {
    font-size: 60rpx;
    display: block;
}

.competition-info {
    flex: 1;
}

.competition-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.competition-type {
    font-size: 26rpx;
    color: #ff6b35;
    display: block;
    margin-bottom: 8rpx;
}

.competition-level {
    font-size: 24rpx;
    color: #999;
    display: block;
}

.competition-status {
    padding: 8rpx 16rpx;
    border-radius: 20rpx;
    font-size: 24rpx;
    font-weight: bold;
}

.competition-status.upcoming {
    background: #e3f2fd;
    color: #1976d2;
}

.competition-status.ongoing {
    background: #fff3e0;
    color: #f57c00;
}

.competition-status.completed {
    background: #f3e5f5;
    color: #7b1fa2;
}

.competition-details {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15rpx;
    margin-bottom: 20rpx;
    padding: 20rpx;
    background: #f8f9fa;
    border-radius: 15rpx;
}

.detail-item {
    display: flex;
    flex-direction: column;
}

.detail-label {
    font-size: 24rpx;
    color: #999;
    margin-bottom: 8rpx;
}

.detail-value {
    font-size: 26rpx;
    color: #333;
    font-weight: 500;
}

.competition-prizes {
    margin-bottom: 20rpx;
    padding: 15rpx 20rpx;
    background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%);
    border-radius: 15rpx;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.prize-label {
    font-size: 26rpx;
    color: #333;
    font-weight: bold;
}

.prize-value {
    font-size: 28rpx;
    font-weight: bold;
}

.prize-value.gold {
    color: #ffd700;
}

.prize-value.silver {
    color: #c0c0c0;
}

.prize-value.bronze {
    color: #cd7f32;
}

.competition-actions {
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
    background: linear-gradient(135deg, #ff6b35 0%, #d63031 100%);
    color: #fff;
}

.action-btn.secondary {
    background: #f8f9fa;
    color: #666;
    border: 2rpx solid #e1e8ed;
}

.action-btn.join {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: #fff;
}

.action-btn.joined {
    background: #28a745;
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

/* 浮动按钮 */
.floating-btn {
    position: fixed;
    bottom: 120rpx;
    right: 40rpx;
    width: 120rpx;
    height: 120rpx;
    background: linear-gradient(135deg, #ff6b35 0%, #d63031 100%);
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8rpx 25rpx rgba(255, 107, 53, 0.3);
    z-index: 1000;
}

.btn-text {
    font-size: 50rpx;
}

/* 点击效果 */
.back-btn:active,
.trophy-btn:active,
.filter-tab:active,
.action-btn:active,
.floating-btn:active {
    transform: scale(0.95);
}
</style>
<template>
    <view class="friends-container">
        <!-- 顶部导航栏 -->
        <view class="header">
            <view class="back-btn" @click="goBack">←</view>
            <text class="header-title">添加朋友</text>
            <view class="search-btn" @click="toggleSearch">🔍</view>
        </view>

        <!-- 搜索栏 -->
        <view class="search-bar" v-show="showSearch">
            <input 
                class="search-input" 
                placeholder="搜索用户名..." 
                v-model="searchKeyword"
                @input="onSearch"
                confirm-type="search"
                @confirm="performSearch"
            />
            <view class="search-clear" @click="clearSearch" v-if="searchKeyword">✕</view>
        </view>

        <!-- 筛选选项 -->
        <view class="filter-section" v-show="!showSearch">
            <view class="filter-row">
                <text class="filter-label">筛选用户：</text>
                <scroll-view class="filter-tags" scroll-x="true">
                    <view class="filter-tag" 
                          :class="{ active: selectedFilter === 'all' }" 
                          @click="setFilter('all')">
                        全部
                    </view>
                    <view class="filter-tag" 
                          :class="{ active: selectedFilter === '运动' }" 
                          @click="setFilter('运动')">
                        运动达人
                    </view>
                    <view class="filter-tag" 
                          :class="{ active: selectedFilter === '健身' }" 
                          @click="setFilter('健身')">
                        健身爱好者
                    </view>
                    <view class="filter-tag" 
                          :class="{ active: selectedFilter === '跑步' }" 
                          @click="setFilter('跑步')">
                        跑步爱好者
                    </view>
                    <view class="filter-tag" 
                          :class="{ active: selectedFilter === '篮球' }" 
                          @click="setFilter('篮球')">
                        篮球迷
                    </view>
                </scroll-view>
            </view>
        </view>

        <!-- 标签页导航 -->
        <view class="tabs-nav">
            <view class="tab-item" 
                  :class="{ active: activeTab === 'all-users' }" 
                  @click="switchTab('all-users')">
                <text class="tab-text">用户列表</text>
                <text class="tab-badge">{{ getTotalUsers() }}</text>
            </view>
            <view class="tab-item" 
                  :class="{ active: activeTab === 'my-friends' }" 
                  @click="switchTab('my-friends')">
                <text class="tab-text">我的朋友</text>
                <text class="tab-badge">{{ friendsList.length }}</text>
            </view>
        </view>

        <!-- 内容区域 -->
        <scroll-view class="content-area" scroll-y="true">
            <!-- 用户列表 -->
            <view class="users-section" v-show="activeTab === 'all-users'">
                <view class="section-title">可添加的用户</view>
                <view class="users-grid">
                    <view class="user-card" v-for="user in filteredUsers" :key="user.id">
                        <view class="user-avatar">
                            <text class="avatar-emoji">{{ user.avatar }}</text>
                            <view class="online-status" :class="user.isOnline ? 'online' : 'offline'"></view>
                        </view>
                        <view class="user-info">
                            <text class="user-name">{{ user.name }}</text>
                            <text class="user-type">{{ user.type }}</text>
                            <text class="user-stats">{{ user.stats }}</text>
                        </view>
                        <view class="user-action">
                            <view class="add-btn" 
                                  @click="addFriend(user)"
                                  v-if="!user.isFriend">
                                添加
                            </view>
                            <view class="added-btn" v-else>
                                已是好友
                            </view>
                        </view>
                    </view>
                </view>
            </view>

            <!-- 我的朋友 -->
            <view class="friends-section" v-show="activeTab === 'my-friends'">
                <view class="section-title">我的朋友 ({{ friendsList.length }})</view>
                <view class="friends-list">
                    <view class="friend-item" v-for="friend in friendsList" :key="friend.id">
                        <view class="friend-avatar">
                            <text class="avatar-emoji">{{ friend.avatar }}</text>
                            <view class="online-status" :class="friend.isOnline ? 'online' : 'offline'"></view>
                        </view>
                        <view class="friend-info">
                            <text class="friend-name">{{ friend.name }}</text>
                            <text class="friend-type">{{ friend.type }}</text>
                            <text class="friend-activity">{{ friend.lastActivity }}</text>
                        </view>
                        <view class="friend-actions">
                            <view class="chat-btn" @click="chatWithFriend(friend)">💬</view>
                            <view class="remove-btn" @click="removeFriend(friend)">🗑️</view>
                        </view>
                    </view>
                </view>
                
                <!-- 空状态 -->
                <view class="empty-state" v-if="friendsList.length === 0">
                    <text class="empty-icon">👥</text>
                    <text class="empty-text">还没有朋友，快去添加一些吧！</text>
                </view>
            </view>
        </scroll-view>

        <!-- 底部提示 -->
        <view class="bottom-tip">
            <text class="tip-text">发现更多运动伙伴，一起开启健康生活！</text>
        </view>
    </view>
</template>

<script>
export default {
    name: 'FriendsPage',
    data() {
        return {
            activeTab: 'all-users',
            showSearch: false,
            searchKeyword: '',
            selectedFilter: 'all',
            
            // 所有用户列表
            allUsers: [
                {
                    id: 1,
                    name: '运动达人小李',
                    type: '运动',
                    stats: '🏃‍♂️ 连续运动30天',
                    avatar: '🏃‍♂️',
                    isOnline: true,
                    isFriend: false
                },
                {
                    id: 2,
                    name: '健身女神小王',
                    type: '健身',
                    stats: '💪 健身达人',
                    avatar: '💪',
                    isOnline: true,
                    isFriend: true
                },
                {
                    id: 3,
                    name: '篮球小子小张',
                    type: '篮球',
                    stats: '🏀 篮球爱好者',
                    avatar: '🏀',
                    isOnline: false,
                    isFriend: false
                },
                {
                    id: 4,
                    name: '跑步爱好者小刘',
                    type: '跑步',
                    stats: '🏃 马拉松选手',
                    avatar: '🏃',
                    isOnline: true,
                    isFriend: false
                },
                {
                    id: 5,
                    name: '瑜伽老师小美',
                    type: '健身',
                    stats: '🧘 瑜伽教练',
                    avatar: '🧘‍♀️',
                    isOnline: false,
                    isFriend: false
                },
                {
                    id: 6,
                    name: '游泳健将小陈',
                    type: '运动',
                    stats: '🏊 游泳高手',
                    avatar: '🏊‍♂️',
                    isOnline: true,
                    isFriend: false
                },
                {
                    id: 7,
                    name: '足球明星小赵',
                    type: '运动',
                    stats: '⚽ 足球队长',
                    avatar: '⚽',
                    isOnline: false,
                    isFriend: false
                },
                {
                    id: 8,
                    name: '健身教练小周',
                    type: '健身',
                    stats: '💪 专业教练',
                    avatar: '🏋️‍♂️',
                    isOnline: true,
                    isFriend: false
                }
            ],
            
            // 已添加的朋友
            friendsList: [
                {
                    id: 2,
                    name: '健身女神小王',
                    type: '健身',
                    avatar: '💪',
                    isOnline: true,
                    lastActivity: '刚刚在线'
                }
            ]
        }
    },
    computed: {
        filteredUsers() {
            let filtered = this.allUsers.filter(user => !user.isFriend)
            
            // 筛选关键词
            if (this.searchKeyword) {
                filtered = filtered.filter(user => 
                    user.name.includes(this.searchKeyword) ||
                    user.type.includes(this.searchKeyword)
                )
            }
            
            // 筛选类型
            if (this.selectedFilter !== 'all') {
                filtered = filtered.filter(user => user.type === this.selectedFilter)
            }
            
            return filtered
        }
    },
    methods: {
        goBack() {
            uni.navigateBack()
        },
        
        toggleSearch() {
            this.showSearch = !this.showSearch
            if (!this.showSearch) {
                this.clearSearch()
            }
        },
        
        onSearch() {
            // 实时搜索
            console.log('搜索关键词:', this.searchKeyword)
        },
        
        performSearch() {
            uni.showToast({
                title: `搜索: ${this.searchKeyword}`,
                icon: 'none'
            })
        },
        
        clearSearch() {
            this.searchKeyword = ''
        },
        
        setFilter(filter) {
            this.selectedFilter = filter
        },
        
        switchTab(tab) {
            this.activeTab = tab
        },
        
        getTotalUsers() {
            return this.allUsers.length
        },
        
        addFriend(user) {
            // 确认添加
            uni.showModal({
                title: '添加朋友',
                content: `确定要添加 ${user.name} 为朋友吗？`,
                success: (res) => {
                    if (res.confirm) {
                        // 更新用户状态
                        const userIndex = this.allUsers.findIndex(u => u.id === user.id)
                        if (userIndex !== -1) {
                            this.allUsers[userIndex].isFriend = true
                        }
                        
                        // 添加到朋友列表
                        const newFriend = {
                            ...user,
                            lastActivity: '刚刚添加'
                        }
                        this.friendsList.push(newFriend)
                        
                        uni.showToast({
                            title: '添加成功！',
                            icon: 'success'
                        })
                        
                        // 震动反馈
                        uni.vibrateShort()
                    }
                }
            })
        },
        
        removeFriend(friend) {
            // 确认移除
            uni.showModal({
                title: '移除朋友',
                content: `确定要从朋友列表中移除 ${friend.name} 吗？`,
                success: (res) => {
                    if (res.confirm) {
                        // 从朋友列表中移除
                        const index = this.friendsList.findIndex(f => f.id === friend.id)
                        if (index !== -1) {
                            this.friendsList.splice(index, 1)
                        }
                        
                        // 更新用户状态
                        const userIndex = this.allUsers.findIndex(u => u.id === friend.id)
                        if (userIndex !== -1) {
                            this.allUsers[userIndex].isFriend = false
                        }
                        
                        uni.showToast({
                            title: '已移除',
                            icon: 'success'
                        })
                        
                        uni.vibrateShort()
                    }
                }
            })
        },
        
        chatWithFriend(friend) {
            uni.showModal({
                title: '聊天',
                content: `与 ${friend.name} 聊天功能开发中...`,
                showCancel: false
            })
        }
    }
}
</script>

<style scoped>
.friends-container {
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

.search-btn {
    width: 80rpx;
    height: 80rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    font-size: 36rpx;
}

/* 搜索栏 */
.search-bar {
    display: flex;
    align-items: center;
    padding: 20rpx 30rpx;
    background: #fff;
    border-bottom: 1px solid #e1e8ed;
}

.search-input {
    flex: 1;
    height: 80rpx;
    background: #f8f9fa;
    border-radius: 40rpx;
    padding: 0 30rpx;
    font-size: 28rpx;
    border: 2rpx solid #e1e8ed;
}

.search-clear {
    width: 60rpx;
    height: 60rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: 20rpx;
    background: #ff6b6b;
    color: #fff;
    border-radius: 50%;
    font-size: 24rpx;
}

/* 筛选选项 */
.filter-section {
    background: #fff;
    padding: 20rpx 30rpx;
    border-bottom: 1px solid #e1e8ed;
}

.filter-row {
    display: flex;
    align-items: center;
}

.filter-label {
    font-size: 28rpx;
    color: #333;
    margin-right: 20rpx;
}

.filter-tags {
    flex: 1;
    white-space: nowrap;
}

.filter-tag {
    display: inline-block;
    padding: 12rpx 24rpx;
    margin-right: 20rpx;
    background: #f8f9fa;
    color: #666;
    border-radius: 20rpx;
    font-size: 24rpx;
    border: 2rpx solid transparent;
}

.filter-tag.active {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: #fff;
}

/* 标签页导航 */
.tabs-nav {
    display: flex;
    background: #fff;
    border-bottom: 1px solid #e1e8ed;
}

.tab-item {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 30rpx 0;
    position: relative;
}

.tab-item.active {
    color: #4a90e2;
}

.tab-item.active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 60rpx;
    height: 6rpx;
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    border-radius: 3rpx;
}

.tab-text {
    font-size: 32rpx;
    font-weight: 500;
    margin-right: 10rpx;
}

.tab-badge {
    background: #ff4757;
    color: #fff;
    padding: 4rpx 12rpx;
    border-radius: 20rpx;
    font-size: 20rpx;
    font-weight: bold;
}

/* 内容区域 */
.content-area {
    flex: 1;
    height: calc(100vh - 400rpx);
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    padding: 30rpx 30rpx 20rpx;
}

/* 用户列表 */
.users-grid {
    padding: 0 30rpx 30rpx;
}

.user-card {
    display: flex;
    align-items: center;
    background: #fff;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.user-avatar {
    position: relative;
    margin-right: 30rpx;
}

.avatar-emoji {
    font-size: 80rpx;
    display: block;
}

.online-status {
    position: absolute;
    bottom: 5rpx;
    right: 5rpx;
    width: 24rpx;
    height: 24rpx;
    border-radius: 50%;
    border: 4rpx solid #fff;
}

.online-status.online {
    background: #28a745;
}

.online-status.offline {
    background: #ccc;
}

.user-info {
    flex: 1;
}

.user-name {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.user-type {
    font-size: 26rpx;
    color: #4a90e2;
    display: block;
    margin-bottom: 8rpx;
}

.user-stats {
    font-size: 24rpx;
    color: #666;
    display: block;
}

.user-action {
    margin-left: 20rpx;
}

.add-btn {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: #fff;
    padding: 12rpx 24rpx;
    border-radius: 25rpx;
    font-size: 24rpx;
    font-weight: bold;
}

.added-btn {
    background: #e1e8ed;
    color: #666;
    padding: 12rpx 24rpx;
    border-radius: 25rpx;
    font-size: 24rpx;
}

/* 朋友列表 */
.friends-list {
    padding: 0 30rpx 30rpx;
}

.friend-item {
    display: flex;
    align-items: center;
    background: #fff;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.friend-avatar {
    position: relative;
    margin-right: 30rpx;
}

.friend-info {
    flex: 1;
}

.friend-name {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.friend-type {
    font-size: 26rpx;
    color: #4a90e2;
    display: block;
    margin-bottom: 8rpx;
}

.friend-activity {
    font-size: 24rpx;
    color: #666;
    display: block;
}

.friend-actions {
    display: flex;
    gap: 20rpx;
}

.chat-btn, .remove-btn {
    width: 80rpx;
    height: 80rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 36rpx;
}

.chat-btn {
    background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
    color: #fff;
}

.remove-btn {
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
    font-size: 28rpx;
    color: #666;
    display: block;
}

/* 底部提示 */
.bottom-tip {
    padding: 30rpx;
    text-align: center;
    background: #fff;
    border-top: 1px solid #e1e8ed;
}

.tip-text {
    font-size: 26rpx;
    color: #666;
}

/* 点击效果 */
.back-btn:active,
.search-btn:active,
.add-btn:active,
.chat-btn:active,
.remove-btn:active {
    transform: scale(0.95);
}

.friend-item:active,
.user-card:active {
    transform: scale(0.98);
}
</style>
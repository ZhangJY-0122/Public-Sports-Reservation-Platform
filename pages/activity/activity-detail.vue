<template>
  <view class="activity-detail-container">
    <!-- 顶部导航栏 -->
    <view class="header">
      <view class="nav-back" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="nav-title">活动详情</text>
      <view class="nav-actions" @click="shareActivity">
        <text class="share-icon">📤</text>
      </view>
    </view>

    <!-- 活动封面 -->
    <view class="activity-cover">
      <image 
        :src="activity.image || '/static/default-activity.jpg'" 
        mode="aspectFill" 
        class="cover-image"
      />
      <view class="status-overlay" :class="'status-' + activity.status">
        <text class="status-text">{{ getStatusText(activity.status) }}</text>
      </view>
    </view>

    <!-- 活动基本信息 -->
    <view class="activity-content">
      <view class="content-card">
        <view class="activity-header">
          <text class="activity-title">{{ activity.title }}</text>
          <view class="activity-type">{{ activity.activity_type || '未分类' }}</view>
        </view>
        
        <view class="activity-description">
          <text>{{ activity.description || '暂无描述' }}</text>
        </view>

        <!-- 活动统计 -->
        <view class="activity-stats">
          <view class="stat-item">
            <text class="stat-number">{{ activity.current_participants || 0 }}</text>
            <text class="stat-label">已报名</text>
          </view>
          <view class="stat-divider"></view>
          <view class="stat-item">
            <text class="stat-number">{{ activity.max_participants || '无限制' }}</text>
            <text class="stat-label">总人数</text>
          </view>
          <view class="stat-divider"></view>
          <view class="stat-item">
            <text class="stat-number">{{ activity.like_count || 0 }}</text>
            <text class="stat-label">收藏</text>
          </view>
        </view>
      </view>

      <!-- 活动信息卡片 -->
      <view class="info-card">
        <view class="card-header">
          <text class="card-icon">📋</text>
          <text class="card-title">活动信息</text>
        </view>
        
        <view class="info-item">
          <text class="info-icon">🕒</text>
          <view class="info-content">
            <text class="info-label">时间</text>
            <text class="info-value">{{ formatDateTime(activity.start_time) }}</text>
            <text v-if="activity.end_time" class="info-subvalue">至 {{ formatDateTime(activity.end_time) }}</text>
          </view>
        </view>

        <view class="info-item">
          <text class="info-icon">📍</text>
          <view class="info-content">
            <text class="info-label">地点</text>
            <text class="info-value">{{ activity.location || '未设置地点' }}</text>
          </view>
        </view>

        <view class="info-item">
          <text class="info-icon">👤</text>
          <view class="info-content">
            <text class="info-label">组织者</text>
            <text class="info-value">{{ activity.creator_name || '未知' }}</text>
          </view>
        </view>

        <view class="info-item">
          <text class="info-icon">👥</text>
          <view class="info-content">
            <text class="info-label">参与条件</text>
            <text class="info-value">
              {{ getGenderText(activity.gender_requirement) }}
              <text v-if="activity.age_requirement">, {{ activity.age_requirement }}</text>
            </text>
          </view>
        </view>

        <view v-if="activity.has_fee" class="info-item">
          <text class="info-icon">💰</text>
          <view class="info-content">
            <text class="info-label">费用</text>
            <text class="info-value">¥{{ activity.total_fee }}</text>
            <text v-if="activity.fee_description" class="info-subvalue">{{ activity.fee_description }}</text>
          </view>
        </view>
      </view>

      <!-- 参与者列表 -->
      <view v-if="participants.length > 0" class="participants-card">
        <view class="card-header">
          <text class="card-icon">👥</text>
          <text class="card-title">参与者 ({{ participants.length }})</text>
          <view class="view-all" @click="viewAllParticipants">
            <text>查看全部</text>
          </view>
        </view>
        
        <scroll-view scroll-x="true" class="participants-scroll">
          <view class="participants-list">
            <view 
              v-for="participant in participants" 
              :key="participant.id" 
              class="participant-item"
            >
              <view class="participant-avatar">
                <image 
                  :src="participant.user_avatar || '/static/default-avatar.png'" 
                  mode="aspectFill"
                />
              </view>
              <text class="participant-name">{{ participant.user_name || '匿名' }}</text>
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- 活动评价 -->
      <view v-if="reviews.length > 0" class="reviews-card">
        <view class="card-header">
          <text class="card-icon">⭐</text>
          <text class="card-title">活动评价</text>
          <view class="rating-summary">
            <text class="rating-score">{{ averageRating }}</text>
            <uni-rate :value="averageRating" readonly size="16" />
            <text class="rating-count">({{ reviews.length }})</text>
          </view>
        </view>
        
        <view class="reviews-list">
          <view 
            v-for="review in reviews" 
            :key="review.id" 
            class="review-item"
          >
            <view class="review-header">
              <view class="reviewer-avatar">
                <image 
                  :src="review.user_avatar || '/static/default-avatar.png'" 
                  mode="aspectFill"
                />
              </view>
              <view class="reviewer-info">
                <text class="reviewer-name">{{ review.user_name || '匿名用户' }}</text>
                <uni-rate :value="review.rating" readonly size="14" />
              </view>
              <text class="review-time">{{ formatRelativeTime(review.created_at) }}</text>
            </view>
            <view class="review-content">
              <text>{{ review.content }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部操作栏 -->
    <view class="bottom-actions">
      <view class="action-buttons">
        <view class="action-btn secondary" @click="toggleLike">
          <text class="action-icon">{{ activity.is_liked ? '❤️' : '🤍' }}</text>
          <text class="action-text">{{ activity.is_liked ? '已收藏' : '收藏' }}</text>
        </view>
        
        <view class="action-btn secondary" @click="shareActivity">
          <text class="action-icon">📤</text>
          <text class="action-text">分享</text>
        </view>
        
        <view 
          v-if="canJoin" 
          class="action-btn primary" 
          @click="joinActivity"
        >
          <text>加入活动</text>
        </view>
        
        <view 
          v-else-if="isParticipant" 
          class="action-btn secondary" 
          @click="leaveActivity"
        >
          <text>退出活动</text>
        </view>
        
        <view 
          v-else 
          class="action-btn disabled"
        >
          <text>{{ getJoinButtonText() }}</text>
        </view>
      </view>
    </view>

    <!-- 参与者列表弹窗 -->
    <uni-popup ref="participantsPopup" type="bottom" :mask-click="true">
      <view class="participants-popup">
        <view class="popup-header">
          <text class="popup-title">参与者列表</text>
          <view class="popup-close" @click="closeParticipantsPopup">×</view>
        </view>
        <scroll-view scroll-y="true" class="participants-popup-content">
          <view 
            v-for="participant in allParticipants" 
            :key="participant.id" 
            class="participant-detail-item"
          >
            <view class="participant-avatar">
              <image 
                :src="participant.user_avatar || '/static/default-avatar.png'" 
                mode="aspectFill"
              />
            </view>
            <view class="participant-info">
              <text class="participant-name">{{ participant.user_name || '匿名' }}</text>
              <text class="join-time">{{ formatDateTime(participant.joined_at) }}</text>
            </view>
            <view class="participant-status">
              <text class="status-text">{{ participant.status === 'joined' ? '已加入' : '已退出' }}</text>
            </view>
          </view>
        </scroll-view>
      </view>
    </uni-popup>
  </view>
</template>

<script>
import { http, BaseUrl } from '@/utils/http.js'
import { formatDateTime, formatRelativeTime } from '@/utils/helper.js'

export default {
  data() {
    return {
      activityId: null,
      activity: {},
      participants: [],
      allParticipants: [],
      reviews: [],
      loading: true
    }
  },

  computed: {
    isParticipant() {
      return this.activity.is_participant || false
    },

    canJoin() {
      if (!this.activity) return false
      if (this.isParticipant) return false
      
      // 检查是否已满
      const current = this.activity.current_participants || 0
      const max = this.activity.max_participants
      if (max && current >= max) return false

      // 检查活动状态
      if (this.activity.status === 'completed' || this.activity.status === 'cancelled') {
        return false
      }

      return true
    },

    averageRating() {
      if (this.reviews.length === 0) return 0
      const total = this.reviews.reduce((sum, review) => sum + review.rating, 0)
      return (total / this.reviews.length).toFixed(1)
    }
  },

  onLoad(options) {
    this.activityId = options.id
    this.loadActivityDetail()
  },

  methods: {
    // 返回上一页
    goBack() {
      uni.navigateBack()
    },

    // 加载活动详情
    async loadActivityDetail() {
      try {
        this.loading = true
        
        // 并行加载活动详情、参与者列表和评价
        const [activityRes, participantsRes, reviewsRes] = await Promise.all([
          http.get(`activity/${this.activityId}`),
          http.get(`activity/${this.activityId}/participants`, { page: 1, page_size: 10 }),
          http.get(`activity/${this.activityId}/reviews`)
        ])

        if (activityRes.code === 0) {
          this.activity = activityRes.data
        } else {
          throw new Error(activityRes.message || '获取活动详情失败')
        }

        if (participantsRes.code === 0) {
          this.participants = participantsRes.data.participants || []
        }

        if (reviewsRes.code === 0) {
          this.reviews = reviewsRes.data || []
        }
      } catch (error) {
        console.error('加载活动详情失败:', error)
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        })
      } finally {
        this.loading = false
      }
    },

    // 加载所有参与者
    async loadAllParticipants() {
      try {
        const response = await http.get(`activity/${this.activityId}/participants`, {
          page: 1,
          page_size: 100
        })
        
        if (response.code === 0) {
          this.allParticipants = response.data.participants || []
        }
      } catch (error) {
        console.error('加载参与者列表失败:', error)
      }
    },

    // 切换收藏状态
    async toggleLike() {
      try {
        const action = this.activity.is_liked ? 'unlike' : 'like'
        const response = await http.post(`activity/${this.activityId}/${action}`)
        
        if (response.code === 0) {
          this.activity.is_liked = !this.activity.is_liked
          uni.showToast({
            title: this.activity.is_liked ? '收藏成功' : '取消收藏',
            icon: 'success'
          })
        } else {
          throw new Error(response.message || '操作失败')
        }
      } catch (error) {
        console.error('收藏操作失败:', error)
        uni.showToast({
          title: '操作失败',
          icon: 'none'
        })
      }
    },

    // 分享活动
    shareActivity() {
      uni.showShareMenu({
        title: this.activity.title,
        path: `/pages/activity/activity-detail?id=${this.activityId}`,
        imageUrl: this.activity.image
      })
    },

    // 加入活动
    async joinActivity() {
      try {
        const response = await http.post(`activity/${this.activityId}/join`)
        
        if (response.code === 0) {
          uni.showToast({
            title: '加入成功',
            icon: 'success'
          })
          
          // 更新活动信息
          this.activity.is_participant = true
          this.activity.current_participants = (this.activity.current_participants || 0) + 1
          
          // 重新加载参与者列表
          this.loadActivityDetail()
        } else {
          throw new Error(response.message || '加入失败')
        }
      } catch (error) {
        console.error('加入活动失败:', error)
        uni.showToast({
          title: error.message || '加入失败',
          icon: 'none'
        })
      }
    },

    // 退出活动
    async leaveActivity() {
      try {
        const response = await http.post(`activity/${this.activityId}/leave`)
        
        if (response.code === 0) {
          uni.showToast({
            title: '退出成功',
            icon: 'success'
          })
          
          // 更新活动信息
          this.activity.is_participant = false
          this.activity.current_participants = Math.max((this.activity.current_participants || 1) - 1, 0)
          
          // 重新加载参与者列表
          this.loadActivityDetail()
        } else {
          throw new Error(response.message || '退出失败')
        }
      } catch (error) {
        console.error('退出活动失败:', error)
        uni.showToast({
          title: error.message || '退出失败',
          icon: 'none'
        })
      }
    },

    // 查看全部参与者
    viewAllParticipants() {
      this.loadAllParticipants()
      this.$refs.participantsPopup.open()
    },

    // 关闭参与者弹窗
    closeParticipantsPopup() {
      this.$refs.participantsPopup.close()
    },

    // 获取状态文本
    getStatusText(status) {
      const statusMap = {
        'upcoming': '即将开始',
        'ongoing': '进行中',
        'completed': '已结束',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    },

    // 获取性别要求文本
    getGenderText(gender) {
      const genderMap = {
        '不限': '性别不限',
        '仅限男性': '仅限男性',
        '仅限女性': '仅限女性'
      }
      return genderMap[gender] || '性别不限'
    },

    // 获取加入按钮文本
    getJoinButtonText() {
      if (this.activity.status === 'completed') return '活动已结束'
      if (this.activity.status === 'cancelled') return '活动已取消'
      
      const current = this.activity.current_participants || 0
      const max = this.activity.max_participants
      if (max && current >= max) return '名额已满'
      
      return '无法加入'
    },

    // 格式化日期时间
    formatDateTime(dateStr) {
      if (!dateStr) return '未设置'
      return formatDateTime(dateStr)
    },

    // 格式化相对时间
    formatRelativeTime(dateStr) {
      if (!dateStr) return ''
      return formatRelativeTime(dateStr)
    }
  }
}
</script>

<style scoped>
.activity-detail-container {
  background: #f5f5f5;
  min-height: 100vh;
  padding-bottom: 80px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 44px 20px 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.nav-back, .nav-actions {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.2);
  transition: all 0.3s;
}

.nav-back:active, .nav-actions:active {
  background: rgba(255, 255, 255, 0.3);
}

.back-icon, .share-icon {
  font-size: 20px;
  font-weight: bold;
}

.nav-title {
  font-size: 18px;
  font-weight: 600;
}

.activity-cover {
  position: relative;
  height: 250px;
}

.cover-image {
  width: 100%;
  height: 100%;
}

.status-overlay {
  position: absolute;
  top: 20px;
  left: 20px;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 14px;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.status-upcoming {
  background: rgba(255, 243, 205, 0.9);
  color: #856404;
}

.status-ongoing {
  background: rgba(212, 237, 218, 0.9);
  color: #155724;
}

.status-completed {
  background: rgba(248, 215, 218, 0.9);
  color: #721c24;
}

.status-cancelled {
  background: rgba(226, 227, 229, 0.9);
  color: #383d41;
}

.activity-content {
  padding: 15px 20px;
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.activity-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  flex: 1;
  margin-right: 12px;
  line-height: 1.4;
}

.activity-type {
  font-size: 12px;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  padding: 4px 8px;
  border-radius: 10px;
  flex-shrink: 0;
}

.activity-description {
  color: #666;
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.activity-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 15px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: #ddd;
  margin: 0 20px;
}

.info-card, .participants-card, .reviews-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.card-icon {
  font-size: 18px;
  margin-right: 8px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  flex: 1;
}

.view-all {
  font-size: 14px;
  color: #667eea;
}

.info-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.info-icon {
  font-size: 16px;
  margin-right: 12px;
  margin-top: 2px;
}

.info-content {
  flex: 1;
}

.info-label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.info-value {
  display: block;
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.info-subvalue {
  display: block;
  font-size: 14px;
  color: #999;
  margin-top: 2px;
}

.participants-scroll {
  white-space: nowrap;
}

.participants-list {
  display: flex;
  gap: 12px;
  padding: 5px 0;
}

.participant-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.participant-avatar {
  width: 50px;
  height: 50px;
  border-radius: 25px;
  overflow: hidden;
  margin-bottom: 6px;
}

.participant-avatar image {
  width: 100%;
  height: 100%;
}

.participant-name {
  font-size: 12px;
  color: #666;
  text-align: center;
  max-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rating-summary {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-score {
  font-size: 16px;
  font-weight: 600;
  color: #667eea;
}

.rating-count {
  font-size: 14px;
  color: #666;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.review-item {
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.review-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.reviewer-avatar {
  width: 36px;
  height: 36px;
  border-radius: 18px;
  overflow: hidden;
  margin-right: 10px;
}

.reviewer-avatar image {
  width: 100%;
  height: 100%;
}

.reviewer-info {
  flex: 1;
}

.reviewer-name {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 2px;
}

.review-time {
  font-size: 12px;
  color: #999;
}

.review-content {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin-left: 46px;
}

.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #eee;
  padding: 15px 20px;
  z-index: 100;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.action-btn {
  flex: 1;
  padding: 14px;
  border-radius: 25px;
  text-align: center;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s;
  border: none;
  outline: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.action-btn.secondary {
  background: #f8f9fa;
  color: #667eea;
  border: 1px solid #667eea;
}

.action-btn.disabled {
  background: #f0f0f0;
  color: #999;
}

.action-btn:active {
  transform: scale(0.98);
  opacity: 0.9;
}

.action-icon {
  font-size: 14px;
}

.action-text {
  font-size: 14px;
}

.participants-popup {
  background: white;
  border-radius: 20px 20px 0 0;
  max-height: 60vh;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.popup-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.popup-close {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #999;
}

.participants-popup-content {
  max-height: 50vh;
  padding: 10px 20px;
}

.participant-detail-item {
  display: flex;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
}

.participant-detail-item:last-child {
  border-bottom: none;
}

.participant-info {
  flex: 1;
  margin-left: 12px;
}

.participant-name {
  display: block;
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.join-time {
  font-size: 12px;
  color: #999;
}

.participant-status {
  flex-shrink: 0;
}

.status-text {
  font-size: 12px;
  color: #667eea;
}
</style>
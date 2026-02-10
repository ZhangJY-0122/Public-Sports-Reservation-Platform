<template>
  <view class="activity-list-container">
    <!-- 顶部导航栏 -->
    <view class="header">
      <view class="nav-back" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="nav-title">活动列表</text>
      <view class="nav-actions" @click="goToCreate">
        <text class="add-icon">+</text>
      </view>
    </view>

    <!-- 筛选和搜索栏 -->
    <view class="filter-bar">
      <view class="search-box">
        <uni-easyinput 
          v-model="searchQuery" 
          placeholder="搜索活动..."
          prefixIcon="search"
          @input="onSearch"
          @confirm="onSearchConfirm"
        />
      </view>
      
      <view class="filter-tabs">
        <view 
          v-for="(status, index) in statusOptions" 
          :key="index"
          class="filter-tab"
          :class="{ active: currentFilter === status.value }"
          @click="onFilterChange(status.value)"
        >
          <text>{{ status.label }}</text>
        </view>
      </view>
    </view>

    <!-- 活动列表 -->
    <view class="activity-list">
      <view v-if="loading" class="loading-container">
        <text class="loading-text">加载中...</text>
      </view>
      
      <view v-else-if="activities.length === 0" class="empty-container">
        <text class="empty-icon">📅</text>
        <text class="empty-text">暂无活动</text>
        <view class="empty-action" @click="goToCreate">
          <text class="action-text">创建第一个活动</text>
        </view>
      </view>
      
      <view v-else class="activity-items">
        <view 
          v-for="activity in activities" 
          :key="activity.id" 
          class="activity-card"
          @click="goToDetail(activity.id)"
        >
          <!-- 活动封面图 -->
          <view class="activity-cover">
            <image 
              :src="activity.image || '/static/default-activity.jpg'" 
              mode="aspectFill" 
              class="cover-image"
            />
            <view class="status-badge" :class="'status-' + activity.status">
              <text>{{ getStatusText(activity.status) }}</text>
            </view>
            <view class="action-buttons">
              <view class="action-btn edit" @click.stop="goToEdit(activity.id)">
                <text>编辑</text>
              </view>
              <view class="action-btn delete" @click.stop="deleteActivity(activity.id)">
                <text>删除</text>
              </view>
            </view>
          </view>
          
          <!-- 活动信息 -->
          <view class="activity-content">
            <view class="activity-header">
              <text class="activity-title">{{ activity.title }}</text>
              <text class="activity-type">{{ activity.activity_type || '未分类' }}</text>
            </view>
            
            <view class="activity-description">
              <text>{{ activity.description || '暂无描述' }}</text>
            </view>
            
            <view class="activity-meta">
              <view class="meta-item">
                <text class="meta-icon">🕒</text>
                <text class="meta-text">{{ formatDate(activity.start_time) }}</text>
              </view>
              
              <view class="meta-item">
                <text class="meta-icon">📍</text>
                <text class="meta-text">{{ activity.location || '未设置地点' }}</text>
              </view>
              
              <view class="meta-item">
                <text class="meta-icon">👥</text>
                <text class="meta-text">
                  {{ activity.current_participants || 0 }}/{{ activity.max_participants || '无限制' }}人
                </text>
              </view>
              
              <view v-if="activity.has_fee" class="meta-item">
                <text class="meta-icon">💰</text>
                <text class="meta-text">¥{{ activity.total_fee }}</text>
              </view>
            </view>
            
            <view class="activity-footer">
              <text class="activity-creator">创建者：{{ activity.creator_name || '未知' }}</text>
              <text class="activity-time">{{ formatRelativeTime(activity.created_at) }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 分页组件 -->
    <view v-if="totalPages > 1" class="pagination">
      <view class="page-info">
        <text>第 {{ currentPage }} 页，共 {{ totalPages }} 页</text>
      </view>
      <view class="page-buttons">
        <view 
          class="page-btn"
          :class="{ disabled: currentPage <= 1 }"
          @click="goToPage(currentPage - 1)"
        >
          <text>上一页</text>
        </view>
        <view 
          class="page-btn"
          :class="{ disabled: currentPage >= totalPages }"
          @click="goToPage(currentPage + 1)"
        >
          <text>下一页</text>
        </view>
      </view>
    </view>

    <!-- 删除确认弹窗 -->
    <uni-popup ref="deletePopup" type="dialog">
      <uni-popup-dialog 
        title="确认删除" 
        content="确定要删除这个活动吗？此操作不可恢复。"
        :before-close="true"
        @close="closeDeletePopup"
        @confirm="confirmDelete"
      />
    </uni-popup>
  </view>
</template>

<script>
import { http, BaseUrl } from '@/utils/http.js'
import { formatDate, formatRelativeTime } from '@/utils/helper.js'

export default {
  data() {
    return {
      activities: [],
      loading: true,
      currentPage: 1,
      pageSize: 10,
      totalPages: 1,
      total: 0,
      searchQuery: '',
      currentFilter: 'all',
      activityToDelete: null,
      statusOptions: [
        { label: '全部', value: 'all' },
        { label: '即将开始', value: 'upcoming' },
        { label: '进行中', value: 'ongoing' },
        { label: '已结束', value: 'completed' },
        { label: '已取消', value: 'cancelled' }
      ]
    }
  },

  onLoad() {
    this.loadActivities()
  },

  onPullDownRefresh() {
    this.currentPage = 1
    this.loadActivities()
  },

  onReachBottom() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++
      this.loadActivities()
    }
  },

  methods: {
    // 返回上一页
    goBack() {
      uni.navigateBack()
    },

    // 跳转到创建页面
    goToCreate() {
      uni.navigateTo({
        url: '/pages/activity/activity'
      })
    },

    // 跳转到详情页
    goToDetail(id) {
      uni.navigateTo({
        url: `/pages/activity/activity-detail?id=${id}`
      })
    },

    // 跳转到编辑页
    goToEdit(id) {
      uni.navigateTo({
        url: `/pages/activity/activity?id=${id}&edit=true`
      })
    },

    // 搜索
    onSearch() {
      // 防抖处理
      clearTimeout(this.searchTimer)
      this.searchTimer = setTimeout(() => {
        this.currentPage = 1
        this.loadActivities()
      }, 500)
    },

    // 搜索确认
    onSearchConfirm() {
      clearTimeout(this.searchTimer)
      this.currentPage = 1
      this.loadActivities()
    },

    // 筛选变化
    onFilterChange(status) {
      this.currentFilter = status
      this.currentPage = 1
      this.loadActivities()
    },

    // 加载活动列表
    async loadActivities() {
      try {
        this.loading = true
        
        const params = {
          page: this.currentPage,
          page_size: this.pageSize,
          search: this.searchQuery
        }

        // 根据筛选状态添加参数
        if (this.currentFilter !== 'all') {
          params.status = this.currentFilter
        }

        const response = await http.get('activity/list', params)
        
        if (response.code === 0) {
          this.activities = response.data.activities || []
          this.currentPage = response.data.pagination.current_page
          this.totalPages = response.data.pagination.total_pages
          this.total = response.data.pagination.total
        } else {
          throw new Error(response.message || '获取活动列表失败')
        }
      } catch (error) {
        console.error('加载活动失败:', error)
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        })
      } finally {
        this.loading = false
        uni.stopPullDownRefresh()
      }
    },

    // 删除活动
    deleteActivity(id) {
      this.activityToDelete = id
      this.$refs.deletePopup.open()
    },

    // 关闭删除弹窗
    closeDeletePopup() {
      this.$refs.deletePopup.close()
      this.activityToDelete = null
    },

    // 确认删除
    async confirmDelete() {
      if (!this.activityToDelete) return

      try {
        const response = await http.delete(`activity/${this.activityToDelete}`)
        
        if (response.code === 0) {
          uni.showToast({
            title: '删除成功',
            icon: 'success'
          })
          
          // 重新加载列表
          this.loadActivities()
        } else {
          throw new Error(response.message || '删除失败')
        }
      } catch (error) {
        console.error('删除活动失败:', error)
        uni.showToast({
          title: '删除失败',
          icon: 'none'
        })
      } finally {
        this.closeDeletePopup()
      }
    },

    // 跳转到指定页
    goToPage(page) {
      if (page < 1 || page > this.totalPages) return
      
      this.currentPage = page
      this.loadActivities()
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

    // 格式化日期
    formatDate(dateStr) {
      if (!dateStr) return '未设置'
      return formatDate(dateStr)
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
.activity-list-container {
  background: #f5f5f5;
  min-height: 100vh;
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

.back-icon, .add-icon {
  font-size: 20px;
  font-weight: bold;
}

.nav-title {
  font-size: 18px;
  font-weight: 600;
}

.filter-bar {
  background: white;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.search-box {
  margin-bottom: 12px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 5px;
}

.filter-tab {
  padding: 8px 16px;
  background: #f0f0f0;
  border-radius: 20px;
  font-size: 14px;
  color: #666;
  white-space: nowrap;
  transition: all 0.3s;
  flex-shrink: 0;
}

.filter-tab.active {
  background: #667eea;
  color: white;
}

.activity-list {
  flex: 1;
  padding: 15px 20px;
}

.loading-container, .empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.loading-text, .empty-text {
  color: #999;
  font-size: 16px;
  margin-top: 10px;
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.empty-action {
  margin-top: 20px;
  padding: 12px 24px;
  background: #667eea;
  border-radius: 25px;
}

.action-text {
  color: white;
  font-size: 14px;
}

.activity-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.activity-card:active {
  transform: scale(0.98);
}

.activity-cover {
  position: relative;
  height: 160px;
}

.cover-image {
  width: 100%;
  height: 100%;
}

.status-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-upcoming {
  background: #fff3cd;
  color: #856404;
}

.status-ongoing {
  background: #d4edda;
  color: #155724;
}

.status-completed {
  background: #f8d7da;
  color: #721c24;
}

.status-cancelled {
  background: #e2e3e5;
  color: #383d41;
}

.action-buttons {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.action-btn.edit {
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
}

.action-btn.delete {
  background: rgba(255, 71, 87, 0.9);
  color: white;
}

.activity-content {
  padding: 15px;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.activity-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  flex: 1;
  margin-right: 10px;
}

.activity-type {
  font-size: 12px;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  padding: 2px 8px;
  border-radius: 10px;
}

.activity-description {
  color: #666;
  font-size: 14px;
  line-height: 1.4;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.activity-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 10px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #666;
}

.meta-icon {
  font-size: 12px;
}

.activity-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.activity-creator {
  font-size: 12px;
  color: #999;
}

.activity-time {
  font-size: 12px;
  color: #999;
}

.pagination {
  background: white;
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-info {
  font-size: 14px;
  color: #666;
}

.page-buttons {
  display: flex;
  gap: 10px;
}

.page-btn {
  padding: 8px 16px;
  background: #f0f0f0;
  border-radius: 6px;
  font-size: 14px;
  color: #666;
  transition: all 0.3s;
}

.page-btn:not(.disabled):active {
  background: #667eea;
  color: white;
}

.page-btn.disabled {
  opacity: 0.5;
}
</style>
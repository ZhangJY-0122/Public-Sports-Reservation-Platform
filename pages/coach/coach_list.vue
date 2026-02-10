<template>
  <view class="coach-list-page">
    <!-- 顶部导航栏 -->
    <view class="nav-bar">
      <view class="nav-content">
        <view class="back-btn" @click="goBack">
          <text class="back-icon">←</text>
        </view>
        <text class="nav-title">选择教练</text>
        <view class="nav-actions">
          <text class="filter-icon" @click="showFilter = !showFilter">🔍</text>
        </view>
      </view>
    </view>

    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-bar">
        <text class="search-icon">🔍</text>
        <input 
          v-model="searchKeyword"
          placeholder="搜索教练姓名或专业领域"
          class="search-input"
          @input="onSearchInput"
        />
        <text v-if="searchKeyword" class="clear-icon" @click="clearSearch">✕</text>
      </view>
    </view>

    <!-- 筛选面板 -->
    <view v-if="showFilter" class="filter-panel">
      <view class="filter-section">
        <text class="filter-label">专业领域</text>
        <picker mode="selector" :range="specializations" @change="onSpecializationChange">
          <view class="filter-picker">
            <text class="filter-value">{{ selectedSpecialization || '全部专业' }}</text>
            <text class="filter-arrow">▼</text>
          </view>
        </picker>
      </view>
      
      <view class="filter-section">
        <text class="filter-label">评分筛选</text>
        <picker mode="selector" :range="ratingRanges" @change="onRatingChange">
          <view class="filter-picker">
            <text class="filter-value">{{ selectedRating || '不限' }}</text>
            <text class="filter-arrow">▼</text>
          </view>
        </picker>
      </view>
      
      <view class="filter-actions">
        <text class="reset-btn" @click="resetFilters">重置</text>
        <text class="apply-btn" @click="applyFilters">应用</text>
      </view>
    </view>

    <!-- 教练列表 -->
    <scroll-view 
      class="coaches-container" 
      scroll-y 
      refresher-enabled
      :refresher-triggered="refresherTriggered"
      @refresherrefresh="onRefresh"
    >
      <view 
        v-for="coach in filteredCoaches" 
        :key="coach.id"
        class="coach-card"
        @click="selectCoach(coach)"
      >
        <view class="coach-header">
          <view class="coach-avatar">
            <image 
              :src="coach.avatar || '/static/nav/n1.png'" 
              mode="aspectFill" 
              class="avatar-img" 
            />
            <view v-if="coach.is_active" class="status-badge available">可预约</view>
            <view v-else class="status-badge unavailable">暂停服务</view>
          </view>
          
          <view class="coach-info">
            <view class="coach-name">{{ coach.name }}</view>
            <view class="coach-specialization">{{ coach.specialization }}</view>
            <view class="coach-rating">
              <view class="stars">
                <text 
                  v-for="n in 5" 
                  :key="n"
                  class="star"
                  :class="{ filled: n <= Math.floor(coach.rating) }"
                >⭐</text>
              </view>
              <text class="rating-text">{{ coach.rating }}分</text>
              <text class="rating-count">({{ coach.total_sessions || 0 }}次授课)</text>
            </view>
            <view class="coach-price">
              <text class="price-label">时薪：</text>
              <text class="price-value">¥{{ coach.hourly_rate }}</text>
            </view>
          </view>
          
          <view class="coach-arrow">
            <text class="arrow-icon">›</text>
          </view>
        </view>
        
        <view class="coach-intro" v-if="coach.bio">
          <text class="intro-text">{{ coach.bio.substring(0, 100) }}...</text>
        </view>
        
        <view class="coach-tags" v-if="coach.tags && coach.tags.length">
          <view 
            v-for="tag in coach.tags.slice(0, 3)" 
            :key="tag"
            class="tag"
          >{{ tag }}</view>
        </view>
      </view>
      
      <!-- 空状态 -->
      <view v-if="filteredCoaches.length === 0 && !loading" class="empty-state">
        <text class="empty-icon">🏃‍♂️</text>
        <text class="empty-text">暂无符合条件的教练</text>
        <text class="empty-subtext">请尝试调整筛选条件</text>
      </view>
      
      <!-- 加载更多 -->
      <view v-if="hasMore && !loading" class="load-more" @click="loadMore">
        <text>加载更多</text>
      </view>
    </scroll-view>

    <!-- 加载状态 -->
    <view v-if="loading" class="loading-state">
      <view class="loading-spinner"></view>
      <text class="loading-text">加载中...</text>
    </view>
  </view>
</template>

<script>
		import { http } from '@/utils/http.js'
export default {
  name: 'CoachList',
  data() {
    return {
      searchKeyword: '',
      showFilter: false,
      selectedSpecialization: '',
      selectedRating: '',
      loading: false,
      refresherTriggered: false,
      hasMore: true,
      currentPage: 1,
      coaches: [],
      specializations: [
        '全部专业', '网球', '篮球', '足球', '羽毛球', 
        '游泳', '健身', '瑜伽', '跑步', '乒乓球', '高尔夫'
      ],
      ratingRanges: ['不限', '4.5分以上', '4.0分以上', '3.5分以上']
    }
  },
  
  computed: {
    filteredCoaches() {
      let filtered = this.coaches;
      
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase();
        filtered = filtered.filter(coach => 
          coach.name.toLowerCase().includes(keyword) ||
          coach.specialization.toLowerCase().includes(keyword) ||
          (coach.bio && coach.bio.toLowerCase().includes(keyword))
        );
      }
      
      if (this.selectedSpecialization && this.selectedSpecialization !== '全部专业') {
        filtered = filtered.filter(coach => 
          coach.specialization.includes(this.selectedSpecialization)
        );
      }
      
      if (this.selectedRating && this.selectedRating !== '不限') {
        const minRating = parseFloat(this.selectedRating);
        filtered = filtered.filter(coach => coach.rating >= minRating);
      }
      
      return filtered;
    }
  },
  
  onLoad() {
    this.loadCoaches();
  },
  
  methods: {
    async loadCoaches() {
    
      
     
        const response = await http.get("coaches/list")
		this.coaches=response.coaches
	  
		
       
    },
    
    onSearchInput() {
      // 实时搜索延迟处理
      clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => {
        // 搜索逻辑已在computed中实现
      }, 300);
    },
    
    clearSearch() {
      this.searchKeyword = '';
    },
    
    onSpecializationChange(e) {
      this.selectedSpecialization = this.specializations[e.detail.value];
    },
    
    onRatingChange(e) {
      this.selectedRating = this.ratingRanges[e.detail.value];
    },
    
    resetFilters() {
      this.selectedSpecialization = '';
      this.selectedRating = '';
      this.searchKeyword = '';
    },
    
    applyFilters() {
      this.showFilter = false;
      this.currentPage = 1;
      this.loadCoaches();
    },
    
    onRefresh() {
      this.refresherTriggered = true;
      this.currentPage = 1;
      this.loadCoaches();
    },
    
    loadMore() {
      if (this.hasMore && !this.loading) {
        this.loadCoaches();
      }
    },
    
    selectCoach(coach) {
      // 跳转到教练详情页面
      uni.navigateTo({
        url: `/pages/coach/coach_detail?id=${coach.id}`
      });
    },
    
    goBack() {
      uni.navigateBack();
    }
  }
}
</script>

<style scoped>
.coach-list-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

.back-icon {
  font-size: 20px;
}

.nav-title {
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.filter-icon {
  font-size: 20px;
}

.search-section {
  padding: 20px;
}

.search-bar {
  background: white;
  border-radius: 25px;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.search-icon {
  font-size: 18px;
  color: #999;
}

.search-input {
  flex: 1;
  font-size: 16px;
  border: none;
  outline: none;
}

.clear-icon {
  font-size: 16px;
  color: #999;
}

.filter-panel {
  background: white;
  margin: 0 20px;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.filter-section {
  margin-bottom: 15px;
}

.filter-label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.filter-picker {
  background: #f8f9fa;
  padding: 12px 15px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.filter-arrow {
  font-size: 12px;
  color: #999;
}

.filter-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.reset-btn, .apply-btn {
  flex: 1;
  padding: 12px;
  border-radius: 10px;
  text-align: center;
  font-size: 16px;
}

.reset-btn {
  background: #f8f9fa;
  color: #666;
}

.apply-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.coaches-container {
  padding: 20px;
  height: calc(100vh - 200px);
}

.coach-card {
  background: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.coach-card:active {
  transform: scale(0.98);
}

.coach-header {
  display: flex;
  align-items: center;
  gap: 15px;
}

.coach-avatar {
  position: relative;
}

.avatar-img {
  width: 60px;
  height: 60px;
  border-radius: 30px;
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.status-badge {
  position: absolute;
  bottom: -5px;
  right: -5px;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 10px;
  font-weight: bold;
}

.status-badge.available {
  background: #4CAF50;
  color: white;
}

.status-badge.unavailable {
  background: #FF5722;
  color: white;
}

.coach-info {
  flex: 1;
}

.coach-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.coach-specialization {
  font-size: 14px;
  color: #667eea;
  margin-bottom: 5px;
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
  font-size: 14px;
  color: #ddd;
}

.star.filled {
  color: #FFD700;
}

.rating-text {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.rating-count {
  font-size: 12px;
  color: #999;
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

.coach-arrow {
  font-size: 24px;
  color: #ccc;
}

.coach-intro {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.intro-text {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.coach-tags {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 20px;
  display: block;
}

.empty-text {
  font-size: 18px;
  color: #333;
  margin-bottom: 10px;
}

.empty-subtext {
  font-size: 14px;
  color: #999;
}

.load-more {
  text-align: center;
  padding: 20px;
  color: #667eea;
  font-size: 16px;
}

.loading-state {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 16px;
  color: #666;
}
</style>
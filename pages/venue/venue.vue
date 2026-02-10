<template>
  <view class="container">
    <!-- 顶部搜索栏 -->
    <view class="search-bar">
      <view class="search-container">
        <text class="search-icon">🔍</text>
        <input 
          type="text" 
          placeholder="搜索场馆名称或类型..." 
          class="search-input"
          v-model="searchKeyword"
          @input="handleSearch"
        />
      </view>
    </view>

<!--    分类导航
    <view class="category-nav">
      <scroll-view class="category-scroll" scroll-x>
        <view class="category-list">
          <view 
            class="category-item" 
            :class="{ active: selectedCategory === item.id }"
            v-for="item in categoryList" 
            :key="item.id"
            @click="selectCategory(item.id)"
          >
            <text class="category-icon">{{ item.icon }}</text>
            <text class="category-text">{{ item.name }}</text>
          </view>
        </view>
      </scroll-view>
    </view> -->

    <!-- 场馆卡片列表 -->
    <scroll-view class="venue-scroll" scroll-y>
      <view class="venue-list">
        <view 
          class="venue-card" 
          v-for="item in filteredVenueList" 
          :key="item.id"
          @click="goToDetail(item)"
        >
          <!-- 左侧图片 -->
          <image :src="item.image" class="venue-image" mode="aspectFill"></image>
          
          <!-- 右侧内容 -->
          <view class="venue-content">
            <text class="venue-name">{{ item.name }}</text>
            <text class="venue-type">{{ item.type }}</text>
            <text class="venue-location">{{ item.location }}</text>
            <text class="venue-desc">{{ item.description }}</text>
            
            <!-- 底部信息 -->
            <view class="venue-footer">
              <view class="price-info">
                <text class="price-symbol">¥</text>
                <text class="venue-price">{{ item.price }}</text>
                <text class="price-unit">/小时</text>
              </view>
              <button class="book-btn" @click="bookVenue(item)">预约</button>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- 底部导航栏 -->
  
  </view>
</template>

<script setup>
import { ref, reactive,computed } from 'vue'
import { http,BaseUrl } from '@/utils/http.js'
import {onShow,	onLoad,	onReady} from '@dcloudio/uni-app'

// 搜索关键词
const searchKeyword = ref('')

// 选中的分类
const selectedCategory = ref('all')

// 分类数据
const categoryList = ref([
  { id: 'all', name: '全部', icon: '🏟️' },
  { id: 'badminton', name: '羽毛球', icon: '🏸' },
  { id: 'basketball', name: '篮球', icon: '🏀' },
  { id: 'swimming', name: '游泳', icon: '🏊' },
  { id: 'fitness', name: '健身', icon: '💪' },
  { id: 'tennis', name: '网球', icon: '🎾' },
  { id: 'football', name: '足球', icon: '⚽' },
  { id: 'tabletennis', name: '乒乓球', icon: '🏓' }
])

// 场馆数据
const venueList = ref([
  {
    id: 1,
    name: '奥林匹克体育中心',
    type: '室内综合场馆',
    location: '市中心区',
    description: '国际标准场地，设施完善，服务一流',
    image: '/static/images/venue1.jpg',
    price: '80',
    category: 'badminton'
  },
  {
    id: 2,
    name: '市民健身中心',
    type: '健身综合体',
    location: '城东新区',
    description: '现代化健身场馆，器械齐全，环境舒适',
    image: '/static/images/venue2.jpg',
    price: '60',
    category: 'fitness'
  },
  {
    id: 3,
    name: '大学城体育馆',
    type: '标准篮球场',
    location: '大学城',
    description: '标准篮球场，木地板，适合比赛和训练',
    image: '/static/images/venue3.jpg',
    price: '100',
    category: 'basketball'
  },
  {
    id: 4,
    name: '阳光游泳馆',
    type: '室内泳池',
    location: '城西开发区',
    description: '50米标准泳池，水质清澈，设施先进',
    image: '/static/images/venue4.jpg',
    price: '50',
    category: 'swimming'
  },
  {
    id: 5,
    name: '绿茵足球场',
    type: '户外足球场',
    location: '南山区',
    description: '标准11人制足球场，天然草坪',
    image: '/static/images/venue5.jpg',
    price: '120',
    category: 'football'
  },
  {
    id: 6,
    name: '威尔网球中心',
    type: '专业网球场',
    location: '北城区',
    description: '标准网球场，专业灯光，适合比赛训练',
    image: '/static/images/venue6.jpg',
    price: '90',
    category: 'tennis'
  }
])

const loadData=()=>{
	http.get("venue/list").then(res=>{
		console.log(res);
		venueList.value=res.venues
	})
}

loadData()

// 筛选后的场馆列表
const filteredVenueList = computed(() => {
  let result = venueList.value
  
  // 按分类筛选
  if (selectedCategory.value !== 'all') {
    result = result.filter(item => item.category === selectedCategory.value)
  }
  
  // 按关键词搜索
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(item => 
      item.name.toLowerCase().includes(keyword) ||
      item.type.toLowerCase().includes(keyword) ||
      item.location.toLowerCase().includes(keyword)
    )
  }
  
  return result
})

// 选择分类
const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
}

// 搜索处理
const handleSearch = () => {
  // 搜索逻辑已在computed中实现
  console.log('搜索关键词:', searchKeyword.value)
}

// 跳转到详情页
const goToDetail = (venue) => {
  uni.navigateTo({
    url: `/pages/venue-detail/venue-detail?id=${venue.id}`
  })
}

// 预约场馆
const bookVenue = (venue) => {
 uni.navigateTo({
   url: `/pages/cgbookin/cgbookin?id=${venue.id}`
 })
}
</script>

<style lang="scss" scoped>
.container {
  height: 100vh;
  background-color: #f8f9fa;
  display: flex;
  flex-direction: column;
}

// 顶部搜索栏
.search-bar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20rpx 30rpx;
  
  .search-container {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 50rpx;
    padding: 20rpx 30rpx;
    display: flex;
    align-items: center;
    backdrop-filter: blur(10rpx);
    
    .search-icon {
      font-size: 32rpx;
      margin-right: 20rpx;
      color: #666;
    }
    
    .search-input {
      flex: 1;
      font-size: 28rpx;
      color: #333;
      border: none;
      outline: none;
      background: transparent;
    }
  }
}

// 分类导航
.category-nav {
  background: #fff;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #eee;
  
  .category-scroll {
    white-space: nowrap;
  }
  
  .category-list {
    display: flex;
    padding: 0 30rpx;
    
    .category-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-right: 40rpx;
      padding: 10rpx;
      border-radius: 16rpx;
      transition: all 0.3s ease;
      
      &.active {
        background: #667eea;
        
        .category-icon,
        .category-text {
          color: #fff;
        }
      }
      
      .category-icon {
        font-size: 48rpx;
        margin-bottom: 8rpx;
        color: #666;
      }
      
      .category-text {
        font-size: 24rpx;
        color: #666;
        white-space: nowrap;
      }
    }
  }
}

// 场馆列表滚动区域
.venue-scroll {
  flex: 1;
  
  .venue-list {
    padding: 30rpx;
  }
}

// 场馆卡片
.venue-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  display: flex;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  
  &:active {
    transform: scale(0.98);
    box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.12);
  }
  
  .venue-image {
    width: 300rpx;
    height: 300rpx;
    border-radius: 16rpx;
    margin-right: 30rpx;
    background: #f0f0f0;
  }
  
  .venue-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    
    .venue-name {
      font-size: 28rpx;
      font-weight: bold;
      color: #333;
      margin-bottom: 10rpx;
    }
    
    .venue-type {
      font-size: 24rpx;
      color: #667eea;
      margin-bottom: 8rpx;
    }
    
    .venue-location {
      font-size: 22rpx;
      color: #999;
      margin-bottom: 10rpx;
    }
    
    .venue-desc {
      font-size: 22rpx;
      color: #666;
      line-height: 1.5;
      margin-bottom: 20rpx;
      flex: 1;
    }
    
    .venue-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .price-info {
        display: flex;
        align-items: baseline;
        
        .price-symbol {
          font-size: 24rpx;
          color: #ff6b35;
        }
        
        .venue-price {
          font-size: 28rpx;
          font-weight: bold;
          color: #ff6b35;
          margin: 0 4rpx;
        }
        
        .price-unit {
          font-size: 24rpx;
          color: #999;
        }
      }
      
      .book-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        border: none;
        border-radius: 25rpx;
        padding: 4rpx 30rpx;
        font-size: 26rpx;
        
        &::after {
          border: none;
        }
        
        &:active {
          opacity: 0.8;
        }
      }
    }
  }
}

// 底部导航栏
.bottom-nav {
  background: #fff;
  border-top: 1rpx solid #eee;
  display: flex;
  padding: 10rpx 0;
  
  .nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10rpx;
    
    &.active {
      .nav-icon,
      .nav-text {
        color: #667eea;
      }
    }
    
    .nav-icon {
      font-size: 40rpx;
      margin-bottom: 8rpx;
      color: #999;
    }
    
    .nav-text {
      font-size: 24rpx;
      color: #666;
    }
  }
}
</style>
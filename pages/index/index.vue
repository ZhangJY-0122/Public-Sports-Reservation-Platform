<template>
  <view class="container">
    <!-- 顶部搜索栏 -->
    <view class="search-bar">
      <view class="search-box">
        <text class="search-icon">🔍</text>
        <input 
          type="text" 
          placeholder="搜索场馆或赛事..." 
          class="search-input"
          v-model="searchValue"
          @confirm="handleSearch"
        />
      </view>
    </view>

    <!-- 轮播图 -->
    <view class="swiper-container">
      <swiper class="swiper" circular autoplay interval="3000" duration="500">
        <swiper-item v-for="(item, index) in bannerList" :key="index">
          <image :src="item.image" mode="aspectFill" class="swiper-image"></image>
        </swiper-item>
      </swiper>
    </view>
	
	<!-- 图片导航 -->
	<view class="image-nav">
	  <view class="image-nav-item" v-for="item in imageNavList" :key="item.id">
	    <image :src="item.image" class="image-nav-img"></image>
	    <text class="image-nav-text">{{ item.name }}</text>
	  </view>
	</view>

  

    <!-- Tabs组件 -->
    <view class="tabs-container">
      <view class="tabs-header">
        <view 
          class="tab-item" 
          :class="{ active: currentTab === 'venues' }"
          @click="currentTab = 'venues'"
        >
          热门场馆
        </view>
        <view 
          class="tab-item" 
          :class="{ active: currentTab === 'events' }"
          @click="currentTab = 'events'"
        >
          赛事活动
        </view>
      </view>

      <!-- 热门场馆内容 -->
      <view class="tab-content" v-if="currentTab === 'venues'">
   
		
		<!-- 功能导航 -->
		<view class="nav-grid">
		  <view class="nav-item" v-for="item in categories" :key="item.id" @click="handleNavClick(item)">
		    <image :src="item.icon" class="nav-icon"></image>
		    <text class="nav-text">{{ item.name }}</text>
		  </view>
		</view>
		<!-- 功能导航 -->
	<!-- 			<view class="nav-grid">
				  <view class="nav-item" v-for="item in navList" :key="item.id" @click="handleNavClick(item)">
				    <text class="nav-icon">{{ item.icon }}</text>
				    <text class="nav-text">{{ item.name }}</text>
				  </view>
				</view>
		 -->

        <!-- 场馆卡片列表 -->
        <view class="card-list">
          <view class="venue-card" v-for="item in sportfacility" :key="item.id">
            <image :src="item.img" class="card-image"></image>
            <view class="card-content">
              <text class="card-title">{{ item.name }}</text>
              <text class="card-desc">{{ item.description }}</text>
              <view class="card-footer">
                <text class="card-price">¥{{ item.capacity}}/小时</text>
                <button class="reserve-btn" @click="handleReserve(item)">预约</button>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 赛事活动内容 -->
      <view class="tab-content" v-if="currentTab === 'events'">
        <view class="card-list">
          <view class="event-card" v-for="item in events" :key="item.id">
            <image :src="item.image" class="card-image"></image>
            <view class="card-content">
              <text class="card-title">{{ item.name }}</text>
              <text class="card-desc">{{ item.description }}</text>
              <text class="card-time">{{ item.time }}</text>
              <view class="card-footer">
                <text class="card-status">{{ item.status }}</text>
                <button class="detail-btn" @click="handleEventDetail(item)">查看详情</button>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>


  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { http,BaseUrl } from '@/utils/http.js'
import {onShow,	onLoad,	onReady} from '@dcloudio/uni-app'

// 搜索值
const searchValue = ref('')

// 当前选中的Tab
const currentTab = ref('venues')

// 轮播图数据
const bannerList = reactive([
  { image: '/static/banner/1.jpg' },
  { image: '/static/banner/2.jpg' },
  { image: '/static/banner/3.jpg' }
])

// 功能导航数据
// 功能导航数据
const navList = reactive([
  { id: 1, name: '羽毛球', icon: '/static/play/羽毛球.png' },
  { id: 2, name: '篮球', icon: '/static/play/篮球.png' },
  { id: 3, name: '游泳', icon: '/static/play/游泳.png' },
  { id: 4, name: '健身', icon: '/static/play/健身.png' },
  { id: 5, name: '网球', icon: '/static/play/网球.png' },
  { id: 6, name: '乒乓球', icon: '/static/play/乒乓球.png' },
  { id: 7, name: '足球', icon: '/static/play/足球.png' },
  { id: 8, name: '全部', icon: '/static/play/全部.png' }
])

const cates=reactive([
	{ id: 1, name: '羽毛球', icon: '/static/play/羽毛球.png' },
	{ id: 2, name: '篮球', icon: '/static/play/篮球.png' },
	{ id: 3, name: '游泳', icon: '/static/play/游泳.png' },
	{ id: 4, name: '健身', icon: '/static/play/健身.png' },
	{ id: 5, name: '网球', icon: '/static/play/网球.png' },
	{ id: 6, name: '乒乓球', icon: '/static/play/乒乓球.png' },
	{ id: 7, name: '足球', icon: '/static/play/足球.png' },
	{ id: 8, name: '全部', icon: '/static/play/全部.png' }
])





// 图片导航数据
const imageNavList = reactive([
  { id: 1, name: '室内场馆', image: '/static/nav/n1.png' },
  { id: 2, name: '室外场地', image: '/static/nav/n2.png' },
  { id: 3, name: '专业训练', image: '/static/nav/n3.png' },
  { id: 4, name: '休闲娱乐', image: '/static/nav/n4.png' }
])


function getIconByName(name) {
  const item = cates.find(c => c.name === name);
  return item ? item.icon : '';
}

// 场馆列表数据
const venueList = reactive([
  {
    id: 1,
    name: '奥林匹克体育中心',
    description: '国际标准室内羽毛球馆，专业场地，设施完善',
    image: '/static/banner/1.jpg',
    price: '80'
  },
  {
    id: 2,
    name: '市民健身中心',
    description: '现代化健身场馆，器械齐全，环境舒适',
    image: '/static/banner/1.jpg',
    price: '60'
  },
  {
    id: 3,
    name: '大学城体育馆',
    description: '标准篮球场，木地板，适合比赛和训练',
    image: '/static/banner/1.jpg',
    price: '100'
  }
])

// 赛事活动数据
const eventList = reactive([
  {
    id: 1,
    name: '2024春季羽毛球公开赛',
    description: '全市羽毛球爱好者交流赛，分设多个组别',
    image: '/static/images/event1.jpg',
    time: '2024-03-15 09:00',
    status: '报名中'
  },
  {
    id: 2,
    name: '篮球3V3挑战赛',
    description: '街头篮球挑战赛，奖金丰厚，等你来战',
    image: '/static/images/event2.jpg',
    time: '2024-03-20 14:00',
    status: '即将开始'
  },
  {
    id: 3,
    name: '游泳锦标赛',
    description: '年度游泳盛事，各项泳姿全面比拼',
    image: '/static/images/event3.jpg',
    time: '2024-03-25 08:30',
    status: '报名截止'
  }
])

// 搜索功能
const handleSearch = () => {
  console.log('搜索:', searchValue.value)
  uni.showToast({
    title: `搜索: ${searchValue.value}`,
    icon: 'none'
  })
}

// 导航点击
const handleNavClick = (item) => {
  console.log('点击导航:', item.name)
  uni.showToast({
    title: `${item.name}`,
    icon: 'none'
  })
}

// 预约功能
const handleReserve = (venue) => {
  console.log('预约场馆:', venue.name)
  uni.navigateTo({
    url: `/pages/cgbookin/cgbookin?id=${venue.id}`
  })
}

// 赛事详情
const handleEventDetail = (event) => {
  console.log('查看赛事详情:', event.name)
  uni.navigateTo({
    url: `/pages/event/event?id=${event.id}`
  })
}

// 底部导航点击
const handleTabClick = (tab) => {
  console.log('底部导航:', tab)
  switch(tab) {
    case 'venues':
      uni.navigateTo({ url: '/pages/venues/venues' })
      break
    case 'orders':
      uni.navigateTo({ url: '/pages/orders/orders' })
      break
    case 'profile':
      uni.navigateTo({ url: '/pages/profile/profile' })
      break
  }
}




const categories=ref([])
const sportfacility=ref([])
const events=ref([])
//加载数据
const loadData_category=()=>{
	http.get('venue/categories').then(res=>{
		let data=[]
		console.log(res,"res");
		let _d=res.venues
		console.log(res,"res");
		
		for(let i=0;i<res.length;i++){
			 
			 
		           if(res[i].name=="全部")
				   {
					   continue;
				   }
			 
				   data.push({
					id:res[i].id,
					name:res[i].name,
					icon:getIconByName(res[i].name)
				  })
			 
		}
	
		console.log(data,"new data");
		categories.value=data
		
		
	})
}

const loadData_sportfacility=()=>{
	http.get('venue/hot ').then(res=>{
		
		let data=[]
		
		for(let i=0;i<res.length;i++){
			 
			 
		          console.log(res[i],"duix");
			 
				   data.push({
					    "id": res[i].id,
					    "name": res[i].name,
					    "city": res[i].city,
					    "facility_type": res[i].facility_type,
					    "address": res[i].address,
					    "hourly_rate": res[i].hourly_rate,
					    "capacity": res[i].capacity,
					    "is_active": res[i].is_active,
					 
					    "img": res[i].img?BaseUrl+res[i].img:"/static/banner/1.jpg",
					    "description": res[i].description
				  })
				  
		}
		
		console.log(data,"new data img");
		sportfacility.value=data
		
		
	})
			 

}

const loadData_events=()=>{
	http.get("events/list").then(res=>{
		console.log(res.events,"eevent_res");
		events.value=res.events
	})
}
onLoad(()=>{
	loadData_category()
	loadData_sportfacility()
	loadData_events()
})


</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 100rpx;
}

// 搜索栏
.search-bar {
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
  padding: 20rpx 30rpx;
  
  .search-box {
    background: #fff;
    border-radius: 50rpx;
    padding: 20rpx 30rpx;
    display: flex;
    align-items: center;
    
    .search-icon {
      font-size: 32rpx;
      margin-right: 20rpx;
      color: #999;
    }
    
    .search-input {
      flex: 1;
      font-size: 28rpx;
      color: #333;
      border: none;
      outline: none;
    }
  }
}

// 轮播图
.swiper-container {
  margin: 5rpx 15rpx;
  border-radius: 5rpx;
  overflow: hidden;
  
  .swiper {
    height: 450rpx;
  }
  
  .swiper-image {
    width: 100%;
    height: 100%;
  }
}

// 功能导航
.nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20rpx;
  padding: 30rpx;
  background: #fff;
  margin: 20rpx 30rpx;
  border-radius: 20rpx;
  
  .nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx;
    
    .nav-icon {
      width: 80rpx;
      height: 80rpx;
      margin-bottom: 10rpx;
    }
    
    .nav-text {
      font-size: 24rpx;
      color: #333;
    }
  }
}




// Tabs组件
.tabs-container {
  margin: 20rpx 5rpx;
  background: #fff;
  border-radius: 20rpx;
  
  .tabs-header {
    display: flex;
    border-bottom: 1rpx solid #eee;
    
    .tab-item {
      flex: 1;
      text-align: center;
      padding: 5rpx;
      font-size: 32rpx;
      color: #666;
      position: relative;
      
      &.active {
        color: #4a90e2;
        font-weight: bold;
        
        &::after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 50%;
          transform: translateX(-50%);
          width: 60rpx;
          height: 4rpx;
          background: #4a90e2;
          border-radius: 2rpx;
        }
      }
    }
  }
  
  .tab-content {
    padding: 30rpx;
  }
}

// 图片导航
.image-nav {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 5upx;
  margin: 30rpx;
  
  .image-nav-item {
    position: relative;
    border-radius: 16rpx;
    overflow: hidden;
    
    .image-nav-img {
      width: 90%;
      height: 120upx;
    }
    
    .image-nav-text {
      position: absolute;
      bottom: 20rpx;
      left: 20rpx;
      color: #fff;
      font-size: 28rpx;
      font-weight: bold;
      text-shadow: 0 2rpx 4rpx rgba(0,0,0,0.5);
    }
  }
}

// 卡片列表
.card-list {
  .venue-card, .event-card {
    display: flex;
    background: #f8f9fa;
    border-radius: 16rpx;
    padding: 2rpx;
    margin-bottom: 5rpx;
    
    .card-image {
      width: 250rpx;
      height: 200rpx;
      border-radius: 5rpx;
      margin-right: 25rpx;
    }
    
    .card-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      
      .card-title {
        font-size: 28rpx;
        font-weight: bold;
        color: #333;
        margin-bottom: 10rpx;
      }
      
      .card-desc {
        font-size: 24rpx;
        color: #666;
        line-height: 1.4;
        margin-bottom: 10rpx;
        flex: 1;
      }
      
      .card-time {
        font-size: 24rpx;
        color: #999;
        margin-bottom: 10rpx;
      }
      
      .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .card-price {
          font-size: 32rpx;
          color: #ff6b35;
          font-weight: bold;
        }
        
        .card-status {
          font-size: 24rpx;
          color: #4a90e2;
        }
        
        .reserve-btn, .detail-btn {
          background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
          color: #fff;
          border: none;
          border-radius: 25rpx;
          padding: 12rpx 24rpx;
          font-size: 24rpx;
          
          &:active {
            opacity: 0.8;
          }
        }
      }
    }
  }
}

// 底部导航
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  background: #fff;
  border-top: 1rpx solid #eee;
  padding: 10rpx 0;
  
  .bottom-nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10rpx;
    
    &.active {
      .nav-icon, .nav-text {
        color: #4a90e2;
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

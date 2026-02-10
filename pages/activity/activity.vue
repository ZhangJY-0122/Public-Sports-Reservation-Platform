<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="header">
      <view class="back-btn" @click="handleBack">
        <text class="back-icon">←</text>
      </view>
      <text class="header-title">创建活动</text>
      <view class="placeholder"></view>
    </view>

    <!-- 创建活动表单 -->
    <view class="create-form">
      <!-- Logo区域 -->
      <view class="logo-section">
        <view class="logo-circle">
          <text class="logo-text">⚽</text>
        </view>
        <text class="app-name">创建新活动</text>
        <text class="app-slogan">组织精彩的体育活动，与朋友们一起运动</text>
      </view>

      <!-- 表单输入区 -->
      <view class="form-section">
        <!-- 活动标题 -->
        <view class="input-group">
          <text class="input-label">活动标题</text>
          <view class="input-container">
            <text class="input-icon">📝</text>
            <input 
              type="text" 
              placeholder="请输入活动标题"
              class="input-field"
              v-model="formData.title"
              @blur="validateField('title')"
              maxlength="50"
            />
          </view>
          <text class="error-text" v-if="errors.title">{{ errors.title }}</text>
        </view>

        <!-- 活动类型 -->
        <view class="input-group">
          <text class="input-label">活动类型</text>
          <view class="input-container">
            <text class="input-icon">🏷️</text>
            <picker 
              mode="selector" 
              :range="activityTypes" 
              @change="onActivityTypeChange"
              class="picker-field"
            >
              <view class="picker-value">
                {{ formData.activity_type || '请选择活动类型' }}
              </view>
            </picker>
          </view>
          <text class="error-text" v-if="errors.activity_type">{{ errors.activity_type }}</text>
        </view>

        <!-- 活动描述 -->
        <view class="input-group">
          <text class="input-label">活动描述</text>
          <view class="input-container textarea-container">
            <text class="input-icon">📄</text>
            <textarea 
              placeholder="请描述活动内容、要求等信息"
              class="textarea-field"
              v-model="formData.description"
              maxlength="500"
              :show-confirm-bar="false"
            />
          </view>
          <text class="char-count">{{ formData.description.length }}/500</text>
        </view>

        <!-- 选择场馆 -->
        <view class="input-group">
          <text class="input-label">选择场馆</text>
          <view class="input-container" @click="openVenuePicker">
            <text class="input-icon">🏟️</text>
            <view class="picker-value">
              {{ selectedVenue.name || '请选择活动场馆' }}
            </view>
            <text class="arrow-icon">›</text>
          </view>
          <text class="error-text" v-if="errors.venue_id">{{ errors.venue_id }}</text>
          
          <!-- 场馆详情卡片 -->
          <view class="venue-card" v-if="selectedVenue.name">
            <view class="venue-info">
              <text class="venue-name">{{ selectedVenue.name }}</text>
              <text class="venue-location">📍 {{ selectedVenue.location }}</text>
              <text class="venue-price">💰 {{ selectedVenue.price_per_hour || 0 }}元/小时</text>
              <text class="venue-facilities">🏓 设施: {{ selectedVenue.facilities || '齐全' }}</text>
            </view>
          </view>
        </view>

        <!-- 开始日期 -->
        <view class="input-group">
          <text class="input-label">开始日期</text>
          <view class="input-container">
            <text class="input-icon">📅</text>
            <picker 
              mode="date" 
              :value="formData.start_date"
              @change="onStartDateChange"
              class="picker-field"
            >
              <view class="picker-value">
                {{ formData.start_date || '请选择开始日期' }}
              </view>
            </picker>
          </view>
          <text class="error-text" v-if="errors.start_date">{{ errors.start_date }}</text>
        </view>

        <!-- 结束日期 -->
        <view class="input-group">
          <text class="input-label">结束日期</text>
          <view class="input-container">
            <text class="input-icon">📅</text>
            <picker 
              mode="date" 
              :value="formData.end_date"
              @change="onEndDateChange"
              class="picker-field"
            >
              <view class="picker-value">
                {{ formData.end_date || '请选择结束日期' }}
              </view>
            </picker>
          </view>
          <text class="error-text" v-if="errors.end_date">{{ errors.end_date }}</text>
        </view>

        <!-- 开始时间 -->
        <view class="input-group">
          <text class="input-label">开始时间</text>
          <view class="input-container">
            <text class="input-icon">⏰</text>
            <picker 
              mode="time" 
              :value="formData.start_time"
              @change="onStartTimeChange"
              class="picker-field"
            >
              <view class="picker-value">
                {{ formData.start_time || '请选择开始时间' }}
              </view>
            </picker>
          </view>
          <text class="error-text" v-if="errors.start_time">{{ errors.start_time }}</text>
        </view>

        <!-- 结束时间 -->
        <view class="input-group">
          <text class="input-label">结束时间</text>
          <view class="input-container">
            <text class="input-icon">⏰</text>
            <picker 
              mode="time" 
              :value="formData.end_time"
              @change="onEndTimeChange"
              class="picker-field"
            >
              <view class="picker-value">
                {{ formData.end_time || '请选择结束时间' }}
              </view>
            </picker>
          </view>
          <text class="error-text" v-if="errors.end_time">{{ errors.end_time }}</text>
        </view>

        <!-- 最大参与人数 -->
        <view class="input-group">
          <text class="input-label">最大参与人数</text>
          <view class="input-container">
            <text class="input-icon">👥</text>
            <input 
              type="number" 
              placeholder="请输入最大参与人数"
              class="input-field"
              v-model="formData.max_participants"
              @blur="validateField('max_participants')"
            />
          </view>
          <text class="error-text" v-if="errors.max_participants">{{ errors.max_participants }}</text>
        </view>

        <!-- 邀请朋友 -->
        <view class="input-group">
          <text class="input-label">邀请朋友</text>
          <view class="invite-section">
            <!-- 已选择的朋友 -->
            <view class="selected-friends" v-if="selectedFriends.length > 0">
              <view 
                v-for="friend in selectedFriends" 
                :key="friend.id" 
                class="friend-tag"
                @click="removeFriend(friend.id)"
              >
                <text class="friend-name">{{ friend.username }}</text>
                <text class="remove-icon">×</text>
              </view>
            </view>
            
            <!-- 邀请按钮 -->
            <view class="invite-btn" @click="openFriendPicker">
              <text class="invite-icon">👥</text>
              <text class="invite-text">邀请朋友参与</text>
            </view>
          </view>
        </view>

        <!-- 创建按钮 -->
        <button 
          class="create-btn" 
          :class="{ active: canCreate }"
          :disabled="!canCreate"
          @click="handleCreateActivity"
        >
          立即创建活动
        </button>
      </view>
    </view>

    <!-- 场馆选择弹窗 -->
    <uni-popup ref="venuePopup" type="bottom" background-color="#fff">
      <view class="popup-content">
        <view class="popup-header">
          <text class="popup-title">选择场馆</text>
          <text class="popup-close" @click="closeVenuePicker">完成</text>
        </view>
        <scroll-view class="popup-list" scroll-y>
          <view 
            v-for="venue in venues" 
            :key="venue.id"
            class="venue-item"
            :class="{ selected: selectedVenue.id === venue.id }"
            @click="selectVenue(venue)"
          >
            <view class="venue-item-info">
              <text class="venue-item-name">{{ venue.name }}</text>
              <text class="venue-item-location">📍 {{ venue.location }}</text>
              <text class="venue-item-price">💰 {{ venue.price_per_hour || 0 }}元/小时</text>
              <text class="venue-item-facilities">🏓 {{ venue.facilities || '设施齐全' }}</text>
            </view>
            <text class="check-icon" v-if="selectedVenue.id === venue.id">✓</text>
          </view>
          
          <!-- 空状态 -->
          <view class="empty-state" v-if="venues.length === 0">
            <text class="empty-icon">🏟️</text>
            <text class="empty-text">暂无可用场馆</text>
          </view>
        </scroll-view>
      </view>
    </uni-popup>

    <!-- 朋友选择弹窗 -->
    <uni-popup ref="friendPopup" type="bottom" background-color="#fff">
      <view class="popup-content">
        <view class="popup-header">
          <text class="popup-title">邀请朋友</text>
          <text class="popup-close" @click="closeFriendPicker">完成</text>
        </view>
        
        <!-- 朋友分类 -->
       
        
        <scroll-view class="popup-list" scroll-y>
          <view 
            v-for="friend in filteredFriends" 
            :key="friend.id"
            class="friend-item"
            :class="{ selected: isFriendSelected(friend.id) }"
            @click="toggleFriend(friend)"
          >
            <view class="friend-avatar">
              <text class="avatar-icon">{{ friend.avatar || '👤' }}</text>
            </view>
            <view class="friend-info">
              <text class="friend-name">{{ friend.friend_name }}</text>
              <text class="friend-sport">🏸 {{ friend.favorite_sport || '运动爱好者' }}</text>
            </view>
            <text class="check-icon" v-if="isFriendSelected(friend.id)">✓</text>
          </view>
          
          <!-- 空状态 -->
          <view class="empty-state" v-if="filteredFriends.length === 0">
            <text class="empty-icon">👥</text>
            <text class="empty-text">暂无好友可邀请</text>
          </view>
        </scroll-view>
      </view>
    </uni-popup>
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { http } from '@/utils/http.js'

// 活动类型选项
const activityTypes = ref([
  '篮球', '足球', '羽毛球', '乒乓球', '网球', 
  '游泳', '跑步', '健身', '瑜伽', '其他'
])

// 表单数据
const formData = reactive({
  title: '',
  description: '',
  activity_type: '',
  venue_id: '',
  start_date: '',
  end_date: '',
  start_time: '',
  end_time: '',
  location: '',
  max_participants: '',
  invited_friends: []
})

// 错误信息
const errors = reactive({
  title: '',
  activity_type: '',
  venue_id: '',
  start_date: '',
  end_date: '',
  start_time: '',
  end_time: '',
  location: '',
  max_participants: ''
})

// 场馆数据
const venues = ref([])
const selectedVenue = ref({})

// 朋友数据
const friends = ref([])
const selectedFriends = ref([])


// 弹窗引用
const venuePopup = ref(null)
const friendPopup = ref(null)

// 朋友分类
const friendCategories = ref([
  { type: 'all', name: '全部好友' },
  { type: 'recent', name: '最近联系' },
  { type: 'same_sport', name: '相同运动' },
  { type: 'nearby', name: '附近好友' }
])

// 计算属性
const canCreate = computed(() => {
  return (
    formData.title.trim() &&
    formData.activity_type.trim() &&
    formData.venue_id &&
    formData.start_date &&
    formData.end_date &&
    formData.start_time &&
    formData.end_time &&
    formData.max_participants &&
    !errors.title &&
    !errors.activity_type &&
    !errors.venue_id &&
    !errors.start_date &&
    !errors.end_date &&
    !errors.start_time &&
    !errors.end_time &&
    !errors.max_participants
  )
})

const filteredFriends = computed(() => friends.value)

// 生命周期
onMounted(() => {
  loadVenues()
  loadFriends()
})

// 打开场馆选择
const openVenuePicker = () => {
  if (venuePopup.value) {
    venuePopup.value.open()
  } else {
    console.error('venuePopup ref 未找到')
  }
}

// 关闭场馆选择
const closeVenuePicker = () => {
  if (venuePopup.value) {
    venuePopup.value.close()
  }
}

// 打开朋友选择
const openFriendPicker = () => {
  if (friendPopup.value) {
    friendPopup.value.open()
  } else {
    console.error('friendPopup ref 未找到')
  }
}

// 关闭朋友选择
const closeFriendPicker = () => {
  if (friendPopup.value) {
    friendPopup.value.close()
  }
}

// 加载场馆列表
  const loadVenues = async () => {
    try {
      uni.showLoading({ title: '加载场馆中…' });
      // 正确写法：第二个参数是 config 对象，params 挂在里面
      const res = await http.get('/venue/list', { params: { page_size: 100 } });
      venues.value = res.venues || [];
  
      // 兜底 mock
      if (venues.value.length === 0) {
        venues.value = [
          {
            id: 1,
            name: '城市运动中心',
            location: '北京市朝阳区建国路88号',
            price_per_hour: 120,
            facilities: '篮球场、羽毛球场、游泳池'
          },
          {
            id: 2,
            name: '奥林匹克体育馆',
            location: '北京市朝阳区国家体育场北路',
            price_per_hour: 200,
            facilities: '专业篮球场、健身房'
          },
          {
            id: 3,
            name: '社区体育公园',
            location: '北京市海淀区中关村大街',
            price_per_hour: 80,
            facilities: '羽毛球场、乒乓球场'
          }
        ];
      }
    } catch (err) {
      console.error('加载场馆失败:', err);
      // 异常时同样给 mock 数据
      venues.value = [
        {
          id: 1,
          name: '城市运动中心',
          location: '北京市朝阳区建国路88号',
          price_per_hour: 120,
          facilities: '篮球场、羽毛球场、游泳池'
        },
        {
          id: 2,
          name: '奥林匹克体育馆',
          location: '北京市朝阳区国家体育场北路',
          price_per_hour: 200,
          facilities: '专业篮球场、健身房'
        }
      ];
      uni.showToast({ title: '使用模拟场馆数据', icon: 'none' });
    } finally {
      uni.hideLoading();
    }
  };

// 加载朋友列表
const loadFriends = async () => {
  try {
    const res = await http.get('/friends/list', {
      params: { page_size: 100 }
    })
    friends.value = res.friends ||  []
    
    // 如果没有数据，使用模拟数据
    if (friends.value.length === 0) {
      friends.value = [
        { id: 1, username: '张三', favorite_sport: '篮球', avatar: '🏀' },
        { id: 2, username: '李四', favorite_sport: '足球', avatar: '⚽' },
        { id: 3, username: '王五', favorite_sport: '羽毛球', avatar: '🏸' },
        { id: 4, username: '赵六', favorite_sport: '乒乓球', avatar: '🏓' },
        { id: 5, username: '钱七', favorite_sport: '网球', avatar: '🎾' },
        { id: 6, username: '孙八', favorite_sport: '游泳', avatar: '🏊' },
        { id: 7, username: '周九', favorite_sport: '跑步', avatar: '🏃' },
        { id: 8, username: '吴十', favorite_sport: '健身', avatar: '💪' }
      ]
    }
  } catch (err) {
    console.error('加载朋友列表失败:', err)
    // 使用模拟数据
    friends.value = [
      { id: 1, username: '张三', favorite_sport: '篮球', avatar: '🏀' },
      { id: 2, username: '李四', favorite_sport: '足球', avatar: '⚽' },
      { id: 3, username: '王五', favorite_sport: '羽毛球', avatar: '🏸' },
      { id: 4, username: '赵六', favorite_sport: '乒乓球', avatar: '🏓' },
      { id: 5, username: '钱七', favorite_sport: '网球', avatar: '🎾' }
    ]
  }
}

// 选择场馆
const selectVenue = (venue) => {
  selectedVenue.value = venue
  formData.venue_id = venue.id
  formData.location = venue.location
  validateField('venue_id')
  closeVenuePicker()
}

// 切换朋友选择
const toggleFriend = (friend) => {
  const index = selectedFriends.value.findIndex(f => f.id === friend.id)
  if (index > -1) {
    selectedFriends.value.splice(index, 1)
  } else {
    selectedFriends.value.push(friend)
  }
  formData.invited_friends = selectedFriends.value.map(f => f.id)
}

// 移除已选择的朋友
const removeFriend = (friendId) => {
  const index = selectedFriends.value.findIndex(f => f.id === friendId)
  if (index > -1) {
    selectedFriends.value.splice(index, 1)
    formData.invited_friends = selectedFriends.value.map(f => f.id)
  }
}

// 检查朋友是否已选择
const isFriendSelected = (friendId) => {
  return selectedFriends.value.some(f => f.id === friendId)
}

// 活动类型选择
const onActivityTypeChange = (e) => {
  const index = e.detail.value
  formData.activity_type = activityTypes.value[index]
  validateField('activity_type')
}

// 日期时间选择方法
const onStartDateChange = (e) => {
  formData.start_date = e.detail.value
  validateField('start_date')
  validateDateRange()
}

const onEndDateChange = (e) => {
  formData.end_date = e.detail.value
  validateField('end_date')
  validateDateRange()
}

const onStartTimeChange = (e) => {
  formData.start_time = e.detail.value
  validateField('start_time')
  validateTimeRange()
}

const onEndTimeChange = (e) => {
  formData.end_time = e.detail.value
  validateField('end_time')
  validateTimeRange()
}

// 字段验证
const validateField = (field) => {
  const value = formData[field]
  
  switch (field) {
    case 'title':
      if (!value.trim()) {
        errors.title = '请输入活动标题'
      } else if (value.length < 2) {
        errors.title = '活动标题至少2个字符'
      } else {
        errors.title = ''
      }
      break
      
    case 'activity_type':
      if (!value.trim()) {
        errors.activity_type = '请选择活动类型'
      } else {
        errors.activity_type = ''
      }
      break
      
    case 'venue_id':
      if (!value) {
        errors.venue_id = '请选择活动场馆'
      } else {
        errors.venue_id = ''
      }
      break
      
    case 'start_date':
      if (!value) {
        errors.start_date = '请选择开始日期'
      } else {
        errors.start_date = ''
      }
      break
      
    case 'end_date':
      if (!value) {
        errors.end_date = '请选择结束日期'
      } else {
        errors.end_date = ''
      }
      break
      
    case 'start_time':
      if (!value) {
        errors.start_time = '请选择开始时间'
      } else {
        errors.start_time = ''
      }
      break
      
    case 'end_time':
      if (!value) {
        errors.end_time = '请选择结束时间'
      } else {
        errors.end_time = ''
      }
      break
      
    case 'max_participants':
      if (!value) {
        errors.max_participants = '请输入最大参与人数'
      } else if (value < 2) {
        errors.max_participants = '参与人数至少2人'
      } else if (value > 100) {
        errors.max_participants = '参与人数最多100人'
      } else {
        errors.max_participants = ''
      }
      break
  }
}

// 验证日期范围
const validateDateRange = () => {
  if (formData.start_date && formData.end_date) {
    const startDate = new Date(formData.start_date)
    const endDate = new Date(formData.end_date)
    
    if (startDate > endDate) {
      errors.end_date = '结束日期不能早于开始日期'
    } else {
      errors.end_date = ''
    }
  }
}

// 验证时间范围
const validateTimeRange = () => {
  if (formData.start_time && formData.end_time && formData.start_date === formData.end_date) {
    const startTime = formData.start_time
    const endTime = formData.end_time
    
    if (startTime >= endTime) {
      errors.end_time = '结束时间必须晚于开始时间'
    } else {
      errors.end_time = ''
    }
  }
}

// 创建活动处理
const handleCreateActivity = async () => {
  if (!canCreate.value) return
  
  // 验证所有字段
  Object.keys(formData).forEach(field => {
    if (field !== 'description' && field !== 'invited_friends') {
      validateField(field)
    }
  })
  
  // 检查是否有错误
  const hasErrors = Object.values(errors).some(error => error !== '')
  if (hasErrors) {
    uni.showToast({
      title: '请完善活动信息',
      icon: 'none'
    })
    return
  }
  
  // 创建活动请求
  uni.showLoading({ title: '创建中...' })
  
  try {
    const res = await http.post('/activity/create', {
      title: formData.title,
      description: formData.description,
      activity_type: formData.activity_type,
      venue_id: formData.venue_id,
      start_date: formData.start_date,
      end_date: formData.end_date,
      start_time: formData.start_time,
      end_time: formData.end_time,
      location: formData.location,
      max_participants: parseInt(formData.max_participants),
      invited_friends: formData.invited_friends
    })
    
    // 创建成功
    console.log('活动创建成功:', res)
    
    uni.showToast({
      title: '活动创建成功！',
      icon: 'success'
    })
    
    // 跳转到活动列表或详情页面
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
    
  } catch (err) {
    // 创建失败
    console.error('活动创建失败:', err)
    uni.showToast({
      title: err.message || '创建失败，请重试',
      icon: 'none'
    })
  } finally {
    uni.hideLoading()
  }
}

// 返回按钮
const handleBack = () => {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

// 顶部导航栏
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 60rpx 40rpx 40rpx;
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
  
  .back-btn {
    width: 60rpx;
    height: 60rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    
    .back-icon {
      font-size: 32rpx;
      color: #fff;
    }
  }
  
  .header-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #fff;
  }
  
  .placeholder {
    width: 60rpx;
  }
}

// 创建活动表单
.create-form {
  padding: 60rpx 40rpx;
  
  // Logo区域
  .logo-section {
    text-align: center;
    margin-bottom: 60rpx;
    
    .logo-circle {
      width: 120rpx;
      height: 120rpx;
      background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 30rpx;
      box-shadow: 0 8rpx 32rpx rgba(74, 144, 226, 0.3);
      
      .logo-text {
        font-size: 60rpx;
      }
    }
    
    .app-name {
      display: block;
      font-size: 40rpx;
      font-weight: bold;
      color: #333;
      margin-bottom: 10rpx;
    }
    
    .app-slogan {
      font-size: 26rpx;
      color: #666;
    }
  }
  
  // 表单区域
  .form-section {
    background: #fff;
    border-radius: 24rpx;
    padding: 40rpx;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
    
    // 输入组
    .input-group {
      margin-bottom: 40rpx;
      
      .input-label {
        display: block;
        font-size: 28rpx;
        font-weight: 500;
        color: #333;
        margin-bottom: 15rpx;
      }
      
      .input-container {
        position: relative;
        display: flex;
        align-items: center;
        border: 2rpx solid #e1e8ed;
        border-radius: 16rpx;
        padding: 0 30rpx;
        transition: all 0.3s ease;
        min-height: 90rpx;
        
        &:focus-within {
          border-color: #4a90e2;
          box-shadow: 0 0 0 6rpx rgba(74, 144, 226, 0.1);
        }
        
        .input-icon {
          font-size: 32rpx;
          margin-right: 20rpx;
          color: #666;
        }
        
        .input-field {
          flex: 1;
          height: 90rpx;
          font-size: 28rpx;
          color: #333;
          border: none;
          outline: none;
          background: transparent;
        }
        
        .picker-field {
          flex: 1;
          height: 90rpx;
          display: flex;
          align-items: center;
        }
        
        .picker-value {
          font-size: 28rpx;
          color: #333;
        }
        
        .arrow-icon {
          font-size: 36rpx;
          color: #999;
        }
        
        // 文本域容器特殊样式
        &.textarea-container {
          align-items: flex-start;
          padding: 30rpx;
          
          .textarea-field {
            flex: 1;
            min-height: 120rpx;
            font-size: 28rpx;
            color: #333;
            border: none;
            outline: none;
            background: transparent;
            line-height: 1.5;
          }
        }
      }
      
      .error-text {
        display: block;
        font-size: 24rpx;
        color: #ff4757;
        margin-top: 10rpx;
      }
      
      .char-count {
        display: block;
        text-align: right;
        font-size: 24rpx;
        color: #999;
        margin-top: 10rpx;
      }
      
      // 场馆卡片
      .venue-card {
        margin-top: 20rpx;
        padding: 20rpx;
        background: #f8f9fa;
        border-radius: 12rpx;
        border: 1rpx solid #e9ecef;
        
        .venue-info {
          display: flex;
          flex-direction: column;
          gap: 8rpx;
          
          .venue-name {
            font-size: 28rpx;
            font-weight: bold;
            color: #333;
          }
          
          .venue-location,
          .venue-price,
          .venue-facilities {
            font-size: 24rpx;
            color: #666;
          }
        }
      }
      
      // 邀请朋友区域
      .invite-section {
        .selected-friends {
          display: flex;
          flex-wrap: wrap;
          gap: 16rpx;
          margin-bottom: 20rpx;
          
          .friend-tag {
            display: flex;
            align-items: center;
            background: #e3f2fd;
            padding: 12rpx 20rpx;
            border-radius: 20rpx;
            border: 1rpx solid #bbdefb;
            
            .friend-name {
              font-size: 24rpx;
              color: #1976d2;
              margin-right: 8rpx;
            }
            
            .remove-icon {
              font-size: 24rpx;
              color: #f44336;
              font-weight: bold;
            }
          }
        }
        
        .invite-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20rpx;
          border: 2rpx dashed #4a90e2;
          border-radius: 16rpx;
          background: #f8fbff;
          
          .invite-icon {
            font-size: 32rpx;
            margin-right: 12rpx;
          }
          
          .invite-text {
            font-size: 28rpx;
            color: #4a90e2;
            font-weight: 500;
          }
        }
      }
    }
    
    // 创建按钮
    .create-btn {
      width: 100%;
      height: 90rpx;
      background: linear-gradient(135deg, #e1e8ed 0%, #d1d9e0 100%);
      color: #999;
      border: none;
      border-radius: 45rpx;
      font-size: 32rpx;
      font-weight: bold;
      transition: all 0.3s ease;
      margin-top: 20rpx;
      
      &.active {
        background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
        color: #fff;
        transform: translateY(0);
        
        &:active {
          transform: translateY(2rpx);
          box-shadow: 0 4rpx 16rpx rgba(74, 144, 226, 0.3);
        }
      }
      
      &:disabled {
        opacity: 0.6;
      }
    }
  }
}

// 弹窗样式
.popup-content {
  background: #fff;
  border-radius: 24rpx 24rpx 0 0;
  max-height: 80vh;
  
  .popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx 40rpx;
    border-bottom: 1rpx solid #e1e8ed;
    
    .popup-title {
      font-size: 32rpx;
      font-weight: bold;
      color: #333;
    }
    
    .popup-close {
      font-size: 28rpx;
      color: #4a90e2;
    }
  }
  
  .friend-categories {
    display: flex;
    padding: 20rpx 40rpx;
    border-bottom: 1rpx solid #e1e8ed;
    
    .category-tab {
      padding: 12rpx 24rpx;
      font-size: 26rpx;
      color: #666;
      border-radius: 20rpx;
      margin-right: 16rpx;
      
      &.active {
        background: #4a90e2;
        color: #fff;
      }
    }
  }
  
  .popup-list {
    max-height: 60vh;
    padding: 20rpx 0;
  }
  
  // 场馆项
  .venue-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 30rpx 40rpx;
    border-bottom: 1rpx solid #f5f5f5;
    
    &.selected {
      background: #f0f7ff;
    }
    
    .venue-item-info {
      flex: 1;
      
      .venue-item-name {
        display: block;
        font-size: 28rpx;
        font-weight: bold;
        color: #333;
        margin-bottom: 8rpx;
      }
      
      .venue-item-location,
      .venue-item-price,
      .venue-item-facilities {
        display: block;
        font-size: 24rpx;
        color: #666;
        margin-bottom: 4rpx;
      }
    }
    
    .check-icon {
      font-size: 32rpx;
      color: #4a90e2;
      font-weight: bold;
    }
  }
  
  // 朋友项
  .friend-item {
    display: flex;
    align-items: center;
    padding: 24rpx 40rpx;
    border-bottom: 1rpx solid #f5f5f5;
    
    &.selected {
      background: #f0f7ff;
    }
    
    .friend-avatar {
      width: 80rpx;
      height: 80rpx;
      border-radius: 50%;
      background: #e3f2fd;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 20rpx;
      
      .avatar-icon {
        font-size: 36rpx;
      }
    }
    
    .friend-info {
      flex: 1;
      
      .friend-name {
        display: block;
        font-size: 28rpx;
        font-weight: 500;
        color: #333;
        margin-bottom: 6rpx;
      }
      
      .friend-sport {
        font-size: 24rpx;
        color: #666;
      }
    }
    
    .check-icon {
      font-size: 32rpx;
      color: #4a90e2;
      font-weight: bold;
    }
  }
  
  // 空状态
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80rpx 40rpx;
    
    .empty-icon {
      font-size: 80rpx;
      margin-bottom: 20rpx;
    }
    
    .empty-text {
      font-size: 28rpx;
      color: #999;
    }
  }
}
</style>
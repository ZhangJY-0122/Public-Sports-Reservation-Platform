<template>
  <view class="facility-booking-page">
    <!-- 顶部导航 -->
    <view class="navbar">
      <view class="navbar-content">
        <text class="navbar-title">设施预订</text>
      </view>
    </view>

    <!-- 设施信息 -->
    <view class="facility-card" v-if="facility_info">
      <view class="facility-header">
        <text class="facility-name">{{ facility_info.name }}</text>
        <text class="facility-rate">¥{{ facility_info.hourly_rate }}/小时</text>
      </view>
      <view class="facility-details">
        <text class="facility-location">{{ facility_info.location }}</text>
        <text class="facility-capacity">容量: {{ facility_info.capacity }}人</text>
      </view>
      <view class="facility-description" v-if="facility_info.description">
        {{ facility_info.description }}
      </view>
    </view>

    <!-- 预订表单 -->
    <view class="booking-form">
      <view class="form-section">
        <text class="section-title">预订信息</text>
        
        <!-- 开始时间 -->
        <view class="form-item" @click="showStartTimePicker = true">
          <text class="form-label">开始时间</text>
          <view class="time-display" :class="{ placeholder: !form_data.start_time }">
            {{ form_data.start_time ? formatDisplayTime(form_data.start_time) : '选择开始时间' }}
          </view>
        </view>

        <!-- 结束时间 -->
        <view class="form-item" @click="showEndTimePicker = true">
          <text class="form-label">结束时间</text>
          <view class="time-display" :class="{ placeholder: !form_data.end_time }">
            {{ form_data.end_time ? formatDisplayTime(form_data.end_time) : '选择结束时间' }}
          </view>
        </view>

        <!-- 预订时长和费用 -->
        <view class="info-row" v-if="form_data.total_hours > 0">
          <view class="info-item">
            <text class="info-label">预订时长</text>
            <text class="info-value">{{ form_data.total_hours }} 小时</text>
          </view>
          <view class="info-item">
            <text class="info-label">总费用</text>
            <text class="info-value price">¥{{ form_data.total_cost }}</text>
          </view>
        </view>

        <!-- 费用分摊开关 -->
        <view class="form-item switch-item">
          <text class="form-label">费用分摊</text>
          <switch 
            :checked="form_data.cost_sharing" 
            @change="onCostSharingChange"
            color="#007AFF"
          />
        </view>

        <!-- 费用分摊详情 -->
        <view class="cost-sharing-details" v-if="form_data.cost_sharing && form_data.total_cost > 0">
          <view class="sharing-header">
            <text class="sharing-title">选择分摊朋友</text>
            <text class="sharing-tip">已选择 {{ selected_friends_count }} 人</text>
          </view>
          
          <!-- 朋友搜索 -->
          <view class="friend-search">
            <input 
              v-model="friend_search_keyword"
              placeholder="搜索朋友"
              class="search-input"
              @input="searchFriends"
            />
          </view>

          <!-- 朋友列表 -->
          <scroll-view class="friend-list" scroll-y>
            <view 
              class="friend-item" 
              v-for="friend in filtered_friends" 
              :key="friend.id"
              @click="toggleFriendSelection(friend)"
            >
              <view class="friend-info">
                <view class="friend-avatar">
                  <text class="avatar-text">{{ getAvatarText(friend.username) }}</text>
                </view>
                <view class="friend-details">
                  <text class="friend-name">{{ friend.username }}</text>
                  <text class="friend-email">{{ friend.email }}</text>
                </view>
              </view>
              <view class="friend-selection">
                <view 
                  class="selection-checkbox" 
                  :class="{ selected: isFriendSelected(friend.id) }"
                >
                  <text class="checkmark" v-if="isFriendSelected(friend.id)">✓</text>
                </view>
              </view>
            </view>
            
            <view class="empty-state" v-if="filtered_friends.length === 0">
              <text class="empty-text">暂无朋友</text>
            </view>
          </scroll-view>

          <!-- 分摊设置 -->
          <view class="sharing-settings" v-if="selected_friends_count > 0">
            <text class="settings-title">分摊设置</text>
            
            <view class="sharing-option">
              <radio-group @change="onSharingMethodChange">
                <label class="radio-item">
                  <radio value="equal" :checked="sharing_method === 'equal'" color="#007AFF" />
                  <text class="radio-label">平均分摊 (每人 ¥{{ equal_share_amount }})</text>
                </label>
                <label class="radio-item">
                  <radio value="custom" :checked="sharing_method === 'custom'" color="#007AFF" />
                  <text class="radio-label">自定义金额</text>
                </label>
              </radio-group>
            </view>

            <!-- 自定义金额输入 -->
            <view class="custom-amounts" v-if="sharing_method === 'custom'">
              <view 
                class="amount-item" 
                v-for="friend in selected_friends_list" 
                :key="friend.id"
              >
                <text class="friend-name">{{ friend.username }}</text>
                <view class="amount-input-wrapper">
                  <text class="currency-symbol">¥</text>
                  <input 
                    v-model="custom_amounts[friend.id]"
                    type="digit"
                    placeholder="0.00"
                    class="amount-input"
                    @input="validateCustomAmounts"
                  />
                </view>
              </view>
              
              <view class="amount-summary">
                <text class="summary-label">总计: ¥{{ custom_total_amount }}</text>
                <text 
                  class="summary-status" 
                  :class="{ valid: custom_total_amount === parseFloat(form_data.total_cost) }"
                >
                  {{ getAmountStatusText() }}
                </text>
              </view>
            </view>

            <!-- 分摊摘要 -->
            <view class="sharing-summary">
              <text class="summary-title">费用分摊摘要</text>
              <view class="summary-details">
                <text class="detail-item">总费用: ¥{{ form_data.total_cost }}</text>
                <text class="detail-item">分摊人数: {{ selected_friends_count + 1 }} 人</text>
                <text class="detail-item">您需支付: ¥{{ my_share_amount }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="action-buttons">
      <button 
        class="submit-btn" 
        :class="{ disabled: !canSubmit }"
        :disabled="!canSubmit"
        @click="submitBooking"
        :loading="submitting"
      >
        {{ submitting ? '提交中...' : '确认预订' }}
      </button>
    </view>

    <!-- 开始时间选择器 -->
    <view v-if="showStartTimePicker" class="picker-modal">
      <view class="picker-mask" @click="showStartTimePicker = false"></view>
      <view class="picker-content">
        <view class="picker-header">
          <text class="picker-cancel" @click="showStartTimePicker = false">取消</text>
          <text class="picker-title">选择开始时间</text>
          <text class="picker-confirm" @click="confirmStartTime">确定</text>
        </view>
        <picker-view 
          class="picker-view" 
          :value="startTimeValue" 
          @change="onStartTimePickerChange"
          indicator-style="height: 50px;"
        >
          <picker-view-column>
            <view class="picker-item" v-for="(item, index) in years" :key="index">{{ item }}年</view>
          </picker-view-column>
          <picker-view-column>
            <view class="picker-item" v-for="(item, index) in months" :key="index">{{ item }}月</view>
          </picker-view-column>
          <picker-view-column>
            <view class="picker-item" v-for="(item, index) in days" :key="index">{{ item }}日</view>
          </picker-view-column>
          <picker-view-column>
            <view class="picker-item" v-for="(item, index) in hours" :key="index">{{ item }}时</view>
          </picker-view-column>
          <picker-view-column>
            <view class="picker-item" v-for="(item, index) in minutes" :key="index">{{ item }}分</view>
          </picker-view-column>
        </picker-view>
      </view>
    </view>

    <!-- 结束时间选择器 -->
    <view v-if="showEndTimePicker" class="picker-modal">
      <view class="picker-mask" @click="showEndTimePicker = false"></view>
      <view class="picker-content">
        <view class="picker-header">
          <text class="picker-cancel" @click="showEndTimePicker = false">取消</text>
          <text class="picker-title">选择结束时间</text>
          <text class="picker-confirm" @click="confirmEndTime">确定</text>
        </view>
        <picker-view 
          class="picker-view" 
          :value="endTimeValue" 
          @change="onEndTimePickerChange"
          indicator-style="height: 50px;"
        >
          <picker-view-column>
            <view class="picker-item" v-for="(item, index) in years" :key="index">{{ item }}年</view>
          </picker-view-column>
          <picker-view-column>
            <view class="picker-item" v-for="(item, index) in months" :key="index">{{ item }}月</view>
          </picker-view-column>
          <picker-view-column>
            <view class="picker-item" v-for="(item, index) in days" :key="index">{{ item }}日</view>
          </picker-view-column>
          <picker-view-column>
            <view class="picker-item" v-for="(item, index) in hours" :key="index">{{ item }}时</view>
          </picker-view-column>
          <picker-view-column>
            <view class="picker-item" v-for="(item, index) in minutes" :key="index">{{ item }}分</view>
          </picker-view-column>
        </picker-view>
      </view>
    </view>

    <!-- 预订成功弹窗 -->
    <uni-popup ref="successPopup" type="center">
      <view class="success-popup">
        <view class="success-icon">✓</view>
        <text class="success-title">预订成功</text>
        <text class="success-message">您的设施预订已提交，请等待确认</text>
        <button class="popup-btn" @click="onSuccessConfirm">确定</button>
      </view>
    </uni-popup>
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'


// 响应式数据
const facility_info = ref(null)
const submitting = ref(false)
const successPopup = ref()

// 朋友列表相关
const friends_list = ref([])
const filtered_friends = ref([])
const friend_search_keyword = ref('')
const selected_friends = ref(new Set())
const sharing_method = ref('equal')
const custom_amounts = ref({})

// 时间选择器相关
const showStartTimePicker = ref(false)
const showEndTimePicker = ref(false)
const startTimeValue = ref([0, 0, 0, 0, 0])
const endTimeValue = ref([0, 0, 0, 0, 0])

// 时间选项
const years = ref([])
const months = ref([])
const days = ref([])
const hours = ref([])
const minutes = ref([])

// 表单数据
const form_data = reactive({
  facility_id: null,
  start_time: '',
  end_time: '',
  total_hours: 0,
  total_cost: 0,
  cost_sharing: false,
  status: 'pending',
  cost_sharings: []
})

// 计算属性
const canSubmit = computed(() => {
  let baseValid = form_data.start_time && 
         form_data.end_time && 
         form_data.total_hours > 0 &&
         !submitting.value
  
  if (form_data.cost_sharing) {
    if (sharing_method.value === 'equal') {
      return baseValid
    } else {
      return baseValid && custom_total_amount.value === parseFloat(form_data.total_cost)
    }
  }
  
  return baseValid
})

// 朋友相关计算属性
const selected_friends_count = computed(() => selected_friends.value.size)

const selected_friends_list = computed(() => {
  return friends_list.value.filter(friend => selected_friends.value.has(friend.id))
})

const equal_share_amount = computed(() => {
  if (selected_friends_count.value === 0) return form_data.total_cost
  const total = parseFloat(form_data.total_cost)
  const shareCount = selected_friends_count.value + 1
  return (total / shareCount).toFixed(2)
})

const my_share_amount = computed(() => {
  if (!form_data.cost_sharing || selected_friends_count.value === 0) {
    return form_data.total_cost
  }
  
  if (sharing_method.value === 'equal') {
    return equal_share_amount.value
  } else {
    const friendsTotal = Object.values(custom_amounts.value).reduce((sum, amount) => {
      return sum + (parseFloat(amount) || 0)
    }, 0)
    return (parseFloat(form_data.total_cost) - friendsTotal).toFixed(2)
  }
})

const custom_total_amount = computed(() => {
  return Object.values(custom_amounts.value).reduce((sum, amount) => {
    return sum + (parseFloat(amount) || 0)
  }, 0)
})

// 页面加载
onLoad((options) => {
  initTimeOptions()
  
  if (options.facility_id) {
    form_data.facility_id = parseInt(options.facility_id)
    loadFacilityInfo(options.facility_id)
  } else {
    uni.showToast({
      title: '设施ID不存在',
      icon: 'error'
    })
 
  }
})

// 初始化时间选项
const initTimeOptions = () => {
  const now = new Date()
  
  // 年份：当前年到后5年
  const currentYear = now.getFullYear()
  for (let i = 0; i < 6; i++) {
    years.value.push(currentYear + i)
  }
  
  // 月份：1-12
  for (let i = 1; i <= 12; i++) {
    months.value.push(i)
  }
  
  // 日期：1-31
  for (let i = 1; i <= 31; i++) {
    days.value.push(i)
  }
  
  // 小时：0-23
  for (let i = 0; i < 24; i++) {
    hours.value.push(i)
  }
  
  // 分钟：0-59
  for (let i = 0; i < 60; i++) {
    minutes.value.push(i)
  }
  
  // 设置默认时间为1小时后
  const defaultStart = new Date(now)
  defaultStart.setHours(now.getHours() + 1)
  defaultStart.setMinutes(0)
  
  const defaultEnd = new Date(defaultStart)
  defaultEnd.setHours(defaultStart.getHours() + 1)
  
  setDefaultTimeValues(defaultStart, defaultEnd)
}

// 设置默认时间值
const setDefaultTimeValues = (startTime, endTime) => {
  form_data.start_time = formatDateForAPI(startTime)
  startTimeValue.value = [
    years.value.indexOf(startTime.getFullYear()),
    startTime.getMonth(),
    startTime.getDate() - 1,
    startTime.getHours(),
    startTime.getMinutes()
  ]
  
  form_data.end_time = formatDateForAPI(endTime)
  endTimeValue.value = [
    years.value.indexOf(endTime.getFullYear()),
    endTime.getMonth(),
    endTime.getDate() - 1,
    endTime.getHours(),
    endTime.getMinutes()
  ]
  
  calculateHoursAndCost()
}

// 格式化日期为 API 需要的格式
const formatDateForAPI = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  
  return `${year}-${month}-${day}T${hours}:${minutes}:00`
}

// 格式化显示时间
const formatDisplayTime = (timeStr) => {
  if (!timeStr) return ''
  
  const date = new Date(timeStr)
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  
  return `${month}月${day}日 ${hours}:${minutes}`
}

// 加载设施信息
const loadFacilityInfo = async (facility_id) => {
  try {
    uni.showLoading({ title: '加载中...' })
    
    const res = await request.post('/sport_facility/detail', { id: facility_id })
    facility_info.value = res.data.data
    
    calculateHoursAndCost()
    
    uni.hideLoading()
  } catch (error) {
    uni.hideLoading()
    uni.showToast({
      title: '加载设施信息失败',
      icon: 'error'
    })
    console.error('加载设施信息失败:', error)
  }
}

// 开始时间选择器变化
const onStartTimePickerChange = (event) => {
  startTimeValue.value = event.detail.value
}

// 结束时间选择器变化
const onEndTimePickerChange = (event) => {
  endTimeValue.value = event.detail.value
}

// 确认开始时间
const confirmStartTime = () => {
  const [yearIndex, monthIndex, dayIndex, hourIndex, minuteIndex] = startTimeValue.value
  
  const selectedDate = new Date(
    years.value[yearIndex],
    months.value[monthIndex] - 1,
    days.value[dayIndex],
    hours.value[hourIndex],
    minutes.value[minuteIndex]
  )
  
  form_data.start_time = formatDateForAPI(selectedDate)
  showStartTimePicker.value = false
  calculateHoursAndCost()
}

// 确认结束时间
const confirmEndTime = () => {
  const [yearIndex, monthIndex, dayIndex, hourIndex, minuteIndex] = endTimeValue.value
  
  const selectedDate = new Date(
    years.value[yearIndex],
    months.value[monthIndex] - 1,
    days.value[dayIndex],
    hours.value[hourIndex],
    minutes.value[minuteIndex]
  )
  
  form_data.end_time = formatDateForAPI(selectedDate)
  showEndTimePicker.value = false
  calculateHoursAndCost()
}

// 计算时长和费用
const calculateHoursAndCost = () => {
  if (form_data.start_time && form_data.end_time) {
    const start = new Date(form_data.start_time)
    const end = new Date(form_data.end_time)
    
    if (end > start) {
      const diffMs = end - start
      const hours = Math.ceil(diffMs / (1000 * 60 * 60))
      form_data.total_hours = hours
      
      if (facility_info.value && facility_info.value.hourly_rate) {
        form_data.total_cost = (hours * facility_info.value.hourly_rate).toFixed(2)
      } else {
        form_data.total_cost = (hours * 50).toFixed(2)
      }
    } else {
      form_data.total_hours = 0
      form_data.total_cost = 0
      uni.showToast({
        title: '结束时间必须晚于开始时间',
        icon: 'error'
      })
    }
  }
}

// 费用分摊开关变化
const onCostSharingChange = (event) => {
  form_data.cost_sharing = event.detail.value
  
  if (form_data.cost_sharing) {
    loadFriendsList()
  } else {
    selected_friends.value.clear()
    custom_amounts.value = {}
  }
}

// 加载朋友列表
const loadFriendsList = async () => {
  try {
    const current_user_id = 1 // 实际项目中应该从登录状态获取
    
    const res = await request.post('/friend/list', {
      user_id: current_user_id,
      page: 1,
      page_size: 100
    })
    
    friends_list.value = res.data.data.list || []
    filtered_friends.value = [...friends_list.value]
    
  } catch (error) {
    console.error('加载朋友列表失败:', error)
    uni.showToast({
      title: '加载朋友列表失败',
      icon: 'error'
    })
  }
}

// 搜索朋友
const searchFriends = () => {
  const keyword = friend_search_keyword.value.toLowerCase()
  if (!keyword) {
    filtered_friends.value = [...friends_list.value]
  } else {
    filtered_friends.value = friends_list.value.filter(friend => 
      friend.username.toLowerCase().includes(keyword) || 
      friend.email.toLowerCase().includes(keyword)
    )
  }
}

// 切换朋友选择
const toggleFriendSelection = (friend) => {
  if (selected_friends.value.has(friend.id)) {
    selected_friends.value.delete(friend.id)
    if (custom_amounts.value[friend.id]) {
      delete custom_amounts.value[friend.id]
    }
  } else {
    selected_friends.value.add(friend.id)
    if (sharing_method.value === 'custom') {
      custom_amounts.value[friend.id] = ''
    }
  }
}

// 检查朋友是否被选中
const isFriendSelected = (friendId) => {
  return selected_friends.value.has(friendId)
}

// 获取头像文本
const getAvatarText = (username) => {
  return username ? username.charAt(0).toUpperCase() : 'U'
}

// 分摊方式变化
const onSharingMethodChange = (event) => {
  sharing_method.value = event.detail.value
  
  if (sharing_method.value === 'equal') {
    custom_amounts.value = {}
  } else {
    selected_friends_list.value.forEach(friend => {
      if (!custom_amounts.value[friend.id]) {
        custom_amounts.value[friend.id] = ''
      }
    })
  }
}

// 验证自定义金额
const validateCustomAmounts = () => {
  Object.keys(custom_amounts.value).forEach(friendId => {
    let amount = custom_amounts.value[friendId]
    if (amount && (isNaN(amount) || parseFloat(amount) < 0)) {
      custom_amounts.value[friendId] = ''
    }
  })
}

// 获取金额状态文本
const getAmountStatusText = () => {
  const total = parseFloat(form_data.total_cost)
  const currentTotal = custom_total_amount.value
  
  if (currentTotal === total) {
    return '金额正确'
  } else if (currentTotal < total) {
    return `还差 ¥${(total - currentTotal).toFixed(2)}`
  } else {
    return `超出 ¥${(currentTotal - total).toFixed(2)}`
  }
}

// 构建分摊数据
const buildCostSharingData = () => {
  if (!form_data.cost_sharing || selected_friends_count.value === 0) {
    return []
  }
  
  const sharingData = []
  const totalCost = parseFloat(form_data.total_cost)
  
  if (sharing_method.value === 'equal') {
    const shareAmount = (totalCost / (selected_friends_count.value + 1)).toFixed(2)
    
    selected_friends_list.value.forEach(friend => {
      sharingData.push({
        user_id: friend.id,
        share_amount: shareAmount,
        paid_amount: 0,
        status: 'pending'
      })
    })
  } else {
    selected_friends_list.value.forEach(friend => {
      const amount = parseFloat(custom_amounts.value[friend.id]) || 0
      sharingData.push({
        user_id: friend.id,
        share_amount: amount.toFixed(2),
        paid_amount: 0,
        status: 'pending'
      })
    })
  }
  
  return sharingData
}

// 提交预订
const submitBooking = async () => {
  if (!canSubmit.value) return
  
  try {
    submitting.value = true
    
    const bookingData = {
      ...form_data,
      cost_sharings: form_data.cost_sharing ? buildCostSharingData() : []
    }
    
    // 检查时间冲突
    const conflictCheck = await request.post('/facility_booking/check_conflict', {
      facility_id: form_data.facility_id,
      start_time: form_data.start_time,
      end_time: form_data.end_time
    })
    
    if (conflictCheck.data.data.has_conflict) {
      uni.showModal({
        title: '时间冲突',
        content: '该时间段已被预订，请选择其他时间',
        showCancel: false
      })
      submitting.value = false
      return
    }
    
    // 提交预订
    const res = await request.post('/facility_booking/add', bookingData)
    
    submitting.value = false
    
    // 显示成功弹窗
    successPopup.value.open()
    
  } catch (error) {
    submitting.value = false
    uni.showToast({
      title: '预订失败',
      icon: 'error'
    })
    console.error('提交预订失败:', error)
  }
}

// 成功确认
const onSuccessConfirm = () => {
  successPopup.value.close()
  uni.navigateBack()
}
</script>

<style scoped>
.facility-booking-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 120rpx;
}

/* 导航栏 */
.navbar {
  background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
  color: white;
  padding: 40rpx 30rpx 20rpx;
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-title {
  font-size: 36rpx;
  font-weight: 600;
}

/* 设施卡片 */
.facility-card {
  background: white;
  margin: 20rpx 30rpx;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.facility-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20rpx;
}

.facility-name {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  flex: 1;
}

.facility-rate {
  font-size: 28rpx;
  font-weight: 600;
  color: #FF6B6B;
}

.facility-details {
  margin-bottom: 20rpx;
}

.facility-location,
.facility-capacity {
  display: block;
  font-size: 26rpx;
  color: #666;
  margin-bottom: 8rpx;
}

.facility-description {
  font-size: 26rpx;
  color: #888;
  line-height: 1.5;
}

/* 预订表单 */
.booking-form {
  background: white;
  margin: 20rpx 30rpx;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.form-section {
  margin-bottom: 30rpx;
}

.section-title {
  display: block;
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 30rpx;
}

.form-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.form-item:last-child {
  border-bottom: none;
}

.form-label {
  font-size: 28rpx;
  color: #333;
}

.time-display {
  font-size: 28rpx;
  color: #007AFF;
}

.time-display.placeholder {
  color: #999;
}

.switch-item {
  border-bottom: none;
  margin-top: 20rpx;
}

/* 信息行 */
.info-row {
  display: flex;
  justify-content: space-between;
  background: #f8f9fa;
  padding: 30rpx;
  border-radius: 12rpx;
  margin: 30rpx 0;
}

.info-item {
  text-align: center;
}

.info-label {
  display: block;
  font-size: 24rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.info-value {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
}

.info-value.price {
  color: #FF6B6B;
}

/* 费用分摊详情 */
.cost-sharing-details {
  margin-top: 30rpx;
  border-top: 1rpx solid #f0f0f0;
  padding-top: 30rpx;
}

.sharing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.sharing-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
}

.sharing-tip {
  font-size: 24rpx;
  color: #007AFF;
}

/* 朋友搜索 */
.friend-search {
  margin-bottom: 20rpx;
}

.search-input {
  width: 100%;
  padding: 20rpx;
  border: 1rpx solid #e0e0e0;
  border-radius: 10rpx;
  font-size: 28rpx;
}

/* 朋友列表 */
.friend-list {
  max-height: 400rpx;
  margin-bottom: 30rpx;
}

.friend-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx;
  border-bottom: 1rpx solid #f5f5f5;
}

.friend-item:last-child {
  border-bottom: none;
}

.friend-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.friend-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
}

.avatar-text {
  color: white;
  font-size: 28rpx;
  font-weight: 600;
}

.friend-details {
  flex: 1;
}

.friend-name {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 5rpx;
}

.friend-email {
  display: block;
  font-size: 24rpx;
  color: #999;
}

.friend-selection {
  margin-left: 20rpx;
}

.selection-checkbox {
  width: 40rpx;
  height: 40rpx;
  border: 2rpx solid #ddd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.selection-checkbox.selected {
  background: #007AFF;
  border-color: #007AFF;
}

.checkmark {
  color: white;
  font-size: 24rpx;
  font-weight: bold;
}

.empty-state {
  padding: 60rpx 0;
  text-align: center;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}

/* 分摊设置 */
.sharing-settings {
  border-top: 1rpx solid #f0f0f0;
  padding-top: 30rpx;
}

.settings-title {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 20rpx;
}

.radio-item {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.radio-label {
  font-size: 28rpx;
  color: #333;
  margin-left: 20rpx;
}

/* 自定义金额 */
.custom-amounts {
  margin-top: 20rpx;
}

.amount-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
}

.amount-item:last-child {
  border-bottom: none;
}

.amount-input-wrapper {
  display: flex;
  align-items: center;
  border: 1rpx solid #e0e0e0;
  border-radius: 8rpx;
  padding: 10rpx 15rpx;
  width: 200rpx;
}

.currency-symbol {
  font-size: 28rpx;
  color: #333;
  margin-right: 10rpx;
}

.amount-input {
  flex: 1;
  font-size: 28rpx;
  text-align: right;
}

.amount-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 30rpx;
  padding: 20rpx;
  background: #f8f9fa;
  border-radius: 10rpx;
}

.summary-label {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
}

.summary-status {
  font-size: 24rpx;
  color: #FF6B6B;
}

.summary-status.valid {
  color: #4CD964;
}

/* 分摊摘要 */
.sharing-summary {
  margin-top: 30rpx;
  padding: 30rpx;
  background: #f8f9fa;
  border-radius: 10rpx;
}

.summary-title {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 15rpx;
}

.detail-item {
  display: block;
  font-size: 26rpx;
  color: #666;
  margin-bottom: 8rpx;
}

/* 操作按钮 */
.action-buttons {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 20rpx 30rpx;
  border-top: 1rpx solid #f0f0f0;
}

.submit-btn {
  background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
  color: white;
  border: none;
  border-radius: 50rpx;
  padding: 25rpx;
  font-size: 32rpx;
  font-weight: 600;
}

.submit-btn.disabled {
  background: #ccc;
  color: #999;
}

/* 时间选择器样式 */
.picker-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 999;
}

.picker-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

.picker-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-radius: 20rpx 20rpx 0 0;
}

.picker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.picker-cancel,
.picker-confirm {
  font-size: 32rpx;
  color: #007AFF;
}

.picker-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
}

.picker-view {
  height: 400rpx;
}

.picker-item {
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28rpx;
}

/* 成功弹窗 */
.success-popup {
  background: white;
  border-radius: 20rpx;
  padding: 60rpx 40rpx;
  text-align: center;
  width: 500rpx;
}

.success-icon {
  width: 120rpx;
  height: 120rpx;
  background: #4CD964;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 50rpx;
  color: white;
  margin: 0 auto 30rpx;
}

.success-title {
  display: block;
  font-size: 36rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 20rpx;
}

.success-message {
  display: block;
  font-size: 28rpx;
  color: #666;
  line-height: 1.5;
  margin-bottom: 40rpx;
}

.popup-btn {
  background: #007AFF;
  color: white;
  border: none;
  border-radius: 50rpx;
  padding: 20rpx 40rpx;
  font-size: 28rpx;
}
</style>
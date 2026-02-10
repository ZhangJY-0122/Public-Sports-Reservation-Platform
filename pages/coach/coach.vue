<template>
    <view class="coach-list-page">
        <!-- 顶部导航栏 -->
        <view class="nav-bar">
            <view class="nav-content">
                <text class="nav-title">教练列表</text>
                <text class="nav-subtitle">{{ availableCount }}位教练可预约</text>
            </view>
        </view>
        
        <!-- 搜索栏 -->
        <view class="search-section">
            <view class="search-bar">
                <text class="search-icon">🔍</text>
                <input 
                    v-model="searchKeyword"
                    placeholder="搜索教练姓名或运动类型"
                    class="search-input"
                    @input="onSearch"
                />
                <text v-if="searchKeyword" class="clear-icon" @click="clearSearch">✕</text>
            </view>
        </view>
        
        <!-- 筛选选项 -->
        <view class="filter-section">
            <picker mode="selector" :range="sportTypes" @change="onSportTypeChange">
                <view class="filter-picker">
                    <text class="filter-label">运动类型</text>
                    <text class="filter-value">{{ selectedSportType || '全部' }}</text>
                    <text class="filter-arrow">▼</text>
                </view>
            </picker>
            
            <picker mode="selector" :range="cities" @change="onCityChange">
                <view class="filter-picker">
                    <text class="filter-label">城市</text>
                    <text class="filter-value">{{ selectedCity || '全部' }}</text>
                    <text class="filter-arrow">▼</text>
                </view>
            </picker>
            
            <picker mode="selector" :range="priceRanges" @change="onPriceRangeChange">
                <view class="filter-picker">
                    <text class="filter-label">价格</text>
                    <text class="filter-value">{{ selectedPriceRange || '不限' }}</text>
                    <text class="filter-arrow">▼</text>
                </view>
            </picker>
        </view>
        
        <!-- 教练列表 -->
        <view class="coaches-container">
            <view 
                v-for="coach in filteredCoaches" 
                :key="coach.id"
                class="coach-card"
                @click="viewCoachDetail(coach)"
            >
                <view class="coach-header">
                    <view class="coach-avatar">
                        <image 
                            :src="coach.img || '/static/images/场馆2.png'" 
                            mode="aspectFill" 
                            class="avatar-img" 
                        />
                        <view v-if="coach.is_available" class="available-badge">可预约</view>
                    </view>
                    <view class="coach-info">
                        <view class="coach-name">{{ coach.name }}</view>
                        <view class="coach-sport">{{ coach.sport_type }}</view>
                        <view class="coach-location">📍 {{ coach.city }}</view>
                        <view class="coach-rate">
                            <text class="rate-label">时薪：</text>
                            <text class="rate-value">¥{{ coach.hourly_rate }}</text>
                        </view>
                    </view>
                    <view class="coach-actions">
                        <view 
                            v-if="coach.is_available"
                            class="book-btn"
                            @click.stop="bookCoach(coach)"
                        >
                            预约
                        </view>
                        <view v-else class="unavailable-btn">已约满</view>
                    </view>
                </view>
                
                <view class="coach-description" v-if="coach.description">
                    <text class="description-text">{{ coach.description }}</text>
                </view>
                
                <view class="coach-footer">
                    <text class="coach-id">ID: {{ coach.id }}</text>
                    <text class="join-date">加入时间：{{ formatDate(coach.created_at) }}</text>
                </view>
            </view>
            
            <!-- 空状态 -->
            <view v-if="filteredCoaches.length === 0" class="empty-state">
                <text class="empty-icon">🏃‍♂️</text>
                <text class="empty-text">暂无符合条件的教练</text>
                <text class="empty-subtext">请尝试调整筛选条件</text>
            </view>
        </view>
        
        <!-- 预约弹窗 -->
        <view v-if="showBookingModal" class="modal-overlay" @click="closeBookingModal">
            <view class="booking-modal" @click.stop>
                <view class="modal-header">
                    <text class="modal-title">预约教练</text>
                    <text class="modal-close" @click="closeBookingModal">×</text>
                </view>
                
                <view class="selected-coach">
                    <text class="coach-name">{{ selectedCoach.name }}</text>
                    <text class="coach-details">{{ selectedCoach.sport_type }} · {{ selectedCoach.city }}</text>
                    <text class="hourly-rate">时薪：¥{{ selectedCoach.hourly_rate }}</text>
                </view>
                
                <view class="booking-form">
                    <view class="form-section">
                        <text class="form-label">选择场馆</text>
                        <picker mode="selector" :range="facilities" @change="onFacilityChange">
                            <view class="form-picker">
                                <text class="picker-text">{{ selectedFacility || '请选择场馆' }}</text>
                                <text class="picker-arrow">▼</text>
                            </view>
                        </picker>
                    </view>
                    
                    <view class="form-section">
                        <text class="form-label">开始时间</text>
                        <picker mode="date" :start="minDate" @change="onStartDateChange">
                            <view class="form-picker">
                                <text class="picker-text">{{ selectedStartDate || '请选择日期' }}</text>
                                <text class="picker-arrow">▼</text>
                            </view>
                        </picker>
                        <picker mode="time" @change="onStartTimeChange">
                            <view class="form-picker">
                                <text class="picker-text">{{ selectedStartTime || '请选择时间' }}</text>
                                <text class="picker-arrow">▼</text>
                            </view>
                        </picker>
                    </view>
                    
                    <view class="form-section">
                        <text class="form-label">结束时间</text>
                        <picker mode="date" :start="selectedStartDate || minDate" @change="onEndDateChange">
                            <view class="form-picker">
                                <text class="picker-text">{{ selectedEndDate || '请选择日期' }}</text>
                                <text class="picker-arrow">▼</text>
                            </view>
                        </picker>
                        <picker mode="time" @change="onEndTimeChange">
                            <view class="form-picker">
                                <text class="picker-text">{{ selectedEndTime || '请选择时间' }}</text>
                                <text class="picker-arrow">▼</text>
                            </view>
                        </picker>
                    </view>
                    
                    <view class="cost-calculation" v-if="totalHours > 0">
                        <text class="calc-text">预计费用：¥{{ totalCost }} ({{ totalHours }}小时)</text>
                    </view>
                </view>
                
                <view class="booking-actions">
                    <view class="cancel-btn" @click="closeBookingModal">取消</view>
                    <view class="confirm-btn" @click="confirmBooking">确认预约</view>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    name: 'CoachList',
    data() {
        return {
            searchKeyword: '',
            selectedSportType: '',
            selectedCity: '',
            selectedPriceRange: '',
            showBookingModal: false,
            selectedCoach: {},
            selectedFacility: '',
            selectedStartDate: '',
            selectedStartTime: '',
            selectedEndDate: '',
            selectedEndTime: '',
            sportTypes: ['全部', '网球', '篮球', '足球', '羽毛球', '游泳', '健身', '瑜伽', '跑步'],
            cities: ['全部', '北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉'],
            priceRanges: ['不限', '0-100元', '100-200元', '200-300元', '300元以上'],
            facilities: ['体育中心网球场', '奥林匹克篮球馆', '阳光游泳馆', '绿茵足球场', '羽毛球训练馆'],
            coaches: [
                {
                    id: 1,
                    name: '张教练',
                    sport_type: '网球',
                    city: '北京',
                    hourly_rate: 150.00,
                    description: '专业网球教练，擅长初学者教学，拥有10年教学经验，曾培养出多名青少年网球选手。',
                    is_available: true,
                    created_at: '2024-01-15 10:00:00',
                    img: '/static/images/场馆2.png'
                },
                {
                    id: 2,
                    name: '李教练',
                    sport_type: '篮球',
                    city: '上海',
                    hourly_rate: 120.00,
                    description: '前职业篮球运动员，专注于技巧训练和体能提升。',
                    is_available: true,
                    created_at: '2024-02-20 14:30:00',
                    img: '/static/images/场馆2.png'
                },
                {
                    id: 3,
                    name: '王教练',
                    sport_type: '游泳',
                    city: '广州',
                    hourly_rate: 180.00,
                    description: '国家级游泳教练，擅长各种泳姿教学，安全第一。',
                    is_available: false,
                    created_at: '2024-01-10 09:15:00',
                    img: '/static/images/场馆2.png'
                },
                {
                    id: 4,
                    name: '刘教练',
                    sport_type: '健身',
                    city: '深圳',
                    hourly_rate: 100.00,
                    description: '专业健身教练，提供个性化训练计划和营养指导。',
                    is_available: true,
                    created_at: '2024-03-05 16:45:00',
                    img: '/static/images/场馆2.png'
                },
                {
                    id: 5,
                    name: '陈教练',
                    sport_type: '瑜伽',
                    city: '杭州',
                    hourly_rate: 90.00,
                    description: '资深瑜伽导师，教授哈他瑜伽和流瑜伽，内外兼修。',
                    is_available: true,
                    created_at: '2024-02-28 11:20:00',
                    img: '/static/images/场馆2.png'
                }
            ]
        }
    },
    computed: {
        filteredCoaches() {
            let filtered = this.coaches
            
            // 搜索筛选
            if (this.searchKeyword) {
                const keyword = this.searchKeyword.toLowerCase()
                filtered = filtered.filter(coach => 
                    coach.name.toLowerCase().includes(keyword) ||
                    coach.sport_type.toLowerCase().includes(keyword)
                )
            }
            
            // 运动类型筛选
            if (this.selectedSportType && this.selectedSportType !== '全部') {
                filtered = filtered.filter(coach => coach.sport_type === this.selectedSportType)
            }
            
            // 城市筛选
            if (this.selectedCity && this.selectedCity !== '全部') {
                filtered = filtered.filter(coach => coach.city === this.selectedCity)
            }
            
            // 价格筛选
            if (this.selectedPriceRange && this.selectedPriceRange !== '不限') {
                filtered = filtered.filter(coach => {
                    const rate = parseFloat(coach.hourly_rate)
                    switch (this.selectedPriceRange) {
                        case '0-100元':
                            return rate <= 100
                        case '100-200元':
                            return rate > 100 && rate <= 200
                        case '200-300元':
                            return rate > 200 && rate <= 300
                        case '300元以上':
                            return rate > 300
                        default:
                            return true
                    }
                })
            }
            
            return filtered
        },
        availableCount() {
            return this.coaches.filter(coach => coach.is_available).length
        },
        minDate() {
            const today = new Date()
            return today.toISOString().split('T')[0]
        },
        totalHours() {
            if (!this.selectedStartDate || !this.selectedStartTime || !this.selectedEndDate || !this.selectedEndTime) {
                return 0
            }
            
            const start = new Date(`${this.selectedStartDate} ${this.selectedStartTime}`)
            const end = new Date(`${this.selectedEndDate} ${this.selectedEndTime}`)
            const diffMs = end.getTime() - start.getTime()
            const diffHours = diffMs / (1000 * 60 * 60)
            
            return diffHours > 0 ? Math.round(diffHours * 100) / 100 : 0
        },
        totalCost() {
            return this.totalHours * parseFloat(this.selectedCoach.hourly_rate || 0)
        }
    },
    methods: {
        onSearch() {
            // 搜索由computed属性自动处理
        },
        clearSearch() {
            this.searchKeyword = ''
        },
        onSportTypeChange(e) {
            const index = e.detail.value
            this.selectedSportType = this.sportTypes[index]
        },
        onCityChange(e) {
            const index = e.detail.value
            this.selectedCity = this.cities[index]
        },
        onPriceRangeChange(e) {
            const index = e.detail.value
            this.selectedPriceRange = this.priceRanges[index]
        },
        viewCoachDetail(coach) {
            uni.showModal({
                title: '教练详情',
                content: `姓名：${coach.name}\n运动类型：${coach.sport_type}\n所在城市：${coach.city}\n时薪：¥${coach.hourly_rate}\n状态：${coach.is_available ? '可预约' : '已约满'}\n简介：${coach.description || '暂无描述'}\n加入时间：${this.formatDate(coach.created_at)}`,
                showCancel: false
            })
        },
        bookCoach(coach) {
            if (!coach.is_available) {
                uni.showToast({
                    title: '教练当前不可预约',
                    icon: 'none'
                })
                return
            }
            
            this.selectedCoach = coach
            this.showBookingModal = true
        },
        closeBookingModal() {
            this.showBookingModal = false
            this.selectedCoach = {}
            this.selectedFacility = ''
            this.selectedStartDate = ''
            this.selectedStartTime = ''
            this.selectedEndDate = ''
            this.selectedEndTime = ''
        },
        onFacilityChange(e) {
            const index = e.detail.value
            this.selectedFacility = this.facilities[index]
        },
        onStartDateChange(e) {
            this.selectedStartDate = e.detail.value
        },
        onStartTimeChange(e) {
            this.selectedStartTime = e.detail.value
        },
        onEndDateChange(e) {
            this.selectedEndDate = e.detail.value
        },
        onEndTimeChange(e) {
            this.selectedEndTime = e.detail.value
        },
        confirmBooking() {
            // 验证必填项
            if (!this.selectedFacility) {
                uni.showToast({
                    title: '请选择场馆',
                    icon: 'none'
                })
                return
            }
            
            if (!this.selectedStartDate || !this.selectedStartTime) {
                uni.showToast({
                    title: '请选择开始时间',
                    icon: 'none'
                })
                return
            }
            
            if (!this.selectedEndDate || !this.selectedEndTime) {
                uni.showToast({
                    title: '请选择结束时间',
                    icon: 'none'
                })
                return
            }
            
            if (this.totalHours <= 0) {
                uni.showToast({
                    title: '结束时间必须晚于开始时间',
                    icon: 'none'
                })
                return
            }
            
            // 模拟创建预约
            const bookingData = {
                coach: this.selectedCoach,
                facility: this.selectedFacility,
                start_time: `${this.selectedStartDate} ${this.selectedStartTime}`,
                end_time: `${this.selectedEndDate} ${this.selectedEndTime}`,
                total_cost: this.totalCost
            }
            
            uni.showModal({
                title: '预约确认',
                content: `教练：${bookingData.coach.name}\n场馆：${bookingData.facility}\n时间：${bookingData.start_time} 至 ${bookingData.end_time}\n预计费用：¥${bookingData.total_cost}\n\n确认创建预约吗？`,
                success: (res) => {
                    if (res.confirm) {
                        uni.showToast({
                            title: '预约创建成功',
                            icon: 'success'
                        })
                        this.closeBookingModal()
                    }
                }
            })
        },
        formatDate(dateString) {
            const date = new Date(dateString)
            const year = date.getFullYear()
            const month = String(date.getMonth() + 1).padStart(2, '0')
            const day = String(date.getDate()).padStart(2, '0')
            const hours = String(date.getHours()).padStart(2, '0')
            const minutes = String(date.getMinutes()).padStart(2, '0')
            return `${year}-${month}-${day} ${hours}:${minutes}`
        }
    }
}
</script>

<style scoped>
.coach-list-page {
    min-height: 100vh;
    background-color: #f5f5f5;
}

.nav-bar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 40rpx 30rpx 30rpx;
    color: white;
}

.nav-content {
    text-align: center;
}

.nav-title {
    font-size: 36rpx;
    font-weight: 600;
    display: block;
    margin-bottom: 10rpx;
}

.nav-subtitle {
    font-size: 28rpx;
    opacity: 0.9;
}

.search-section {
    padding: 30rpx 20rpx 0;
}

.search-bar {
    background: white;
    border-radius: 50rpx;
    padding: 20rpx 30rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.search-icon {
    font-size: 32rpx;
    margin-right: 20rpx;
}

.search-input {
    flex: 1;
    font-size: 28rpx;
}

.clear-icon {
    font-size: 24rpx;
    color: #999;
    margin-left: 20rpx;
}

.filter-section {
    padding: 20rpx;
    display: flex;
    gap: 15rpx;
}

.filter-picker {
    flex: 1;
    background: white;
    border-radius: 20rpx;
    padding: 20rpx;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.filter-label {
    font-size: 24rpx;
    color: #666;
}

.filter-value {
    font-size: 28rpx;
    color: #333;
    font-weight: 500;
}

.filter-arrow {
    font-size: 20rpx;
    color: #999;
    margin-left: 10rpx;
}

.coaches-container {
    padding: 20rpx;
}

.coach-card {
    background: white;
    border-radius: 20rpx;
    margin-bottom: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.coach-header {
    display: flex;
    align-items: flex-start;
    margin-bottom: 25rpx;
}

.coach-avatar {
    position: relative;
    margin-right: 25rpx;
}

.avatar-img {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
}

.available-badge {
    position: absolute;
    bottom: -5rpx;
    left: 50%;
    transform: translateX(-50%);
    background: #4caf50;
    color: white;
    font-size: 20rpx;
    padding: 5rpx 12rpx;
    border-radius: 15rpx;
}

.coach-info {
    flex: 1;
}

.coach-name {
    font-size: 32rpx;
    font-weight: 600;
    color: #333;
    margin-bottom: 8rpx;
}

.coach-sport {
    font-size: 28rpx;
    color: #667eea;
    margin-bottom: 8rpx;
}

.coach-location {
    font-size: 24rpx;
    color: #666;
    margin-bottom: 8rpx;
}

.coach-rate {
    display: flex;
    align-items: center;
}

.rate-label {
    font-size: 24rpx;
    color: #666;
}

.rate-value {
    font-size: 28rpx;
    color: #ff6b6b;
    font-weight: 600;
}

.coach-actions {
    display: flex;
    flex-direction: column;
    gap: 10rpx;
}

.book-btn {
    background: #667eea;
    color: white;
    padding: 15rpx 25rpx;
    border-radius: 25rpx;
    font-size: 24rpx;
    text-align: center;
    min-width: 100rpx;
}

.unavailable-btn {
    background: #ccc;
    color: #666;
    padding: 15rpx 25rpx;
    border-radius: 25rpx;
    font-size: 24rpx;
    text-align: center;
    min-width: 100rpx;
}

.coach-description {
    margin: 20rpx 0;
    padding: 20rpx;
    background: #f8f9fa;
    border-radius: 10rpx;
}

.description-text {
    font-size: 28rpx;
    color: #666;
    line-height: 1.5;
}

.coach-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20rpx;
    padding-top: 20rpx;
    border-top: 1rpx solid #f0f0f0;
}

.coach-id {
    font-size: 24rpx;
    color: #999;
}

.join-date {
    font-size: 24rpx;
    color: #999;
}

.empty-state {
    text-align: center;
    padding: 100rpx 40rpx;
    background: white;
    border-radius: 20rpx;
    margin-top: 20rpx;
}

.empty-icon {
    font-size: 80rpx;
    display: block;
    margin-bottom: 30rpx;
}

.empty-text {
    font-size: 32rpx;
    color: #333;
    font-weight: 500;
    display: block;
    margin-bottom: 15rpx;
}

.empty-subtext {
    font-size: 28rpx;
    color: #666;
}

/* 预约弹窗样式 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.booking-modal {
    background: white;
    border-radius: 20rpx;
    margin: 40rpx;
    max-height: 90vh;
    overflow-y: auto;
    width: calc(100vw - 80rpx);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx;
    border-bottom: 1rpx solid #f0f0f0;
}

.modal-title {
    font-size: 32rpx;
    font-weight: 600;
    color: #333;
}

.modal-close {
    font-size: 40rpx;
    color: #999;
    padding: 10rpx;
}

.selected-coach {
    padding: 30rpx;
    background: #f8f9fa;
    margin: 0 30rpx 30rpx;
    border-radius: 15rpx;
}

.selected-coach .coach-name {
    font-size: 30rpx;
    font-weight: 600;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.selected-coach .coach-details {
    font-size: 26rpx;
    color: #667eea;
    display: block;
    margin-bottom: 8rpx;
}

.selected-coach .hourly-rate {
    font-size: 28rpx;
    color: #ff6b6b;
    font-weight: 600;
}

.booking-form {
    padding: 0 30rpx 30rpx;
}

.form-section {
    margin-bottom: 30rpx;
}

.form-label {
    font-size: 28rpx;
    color: #333;
    font-weight: 500;
    display: block;
    margin-bottom: 15rpx;
}

.form-picker {
    background: #f8f9fa;
    border: 2rpx solid #e9ecef;
    border-radius: 15rpx;
    padding: 25rpx;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15rpx;
}

.picker-text {
    font-size: 28rpx;
    color: #333;
}

.picker-arrow {
    font-size: 20rpx;
    color: #999;
}

.cost-calculation {
    background: #e3f2fd;
    padding: 20rpx;
    border-radius: 15rpx;
    text-align: center;
    margin: 20rpx 0;
}

.calc-text {
    font-size: 28rpx;
    color: #1976d2;
    font-weight: 500;
}

.booking-actions {
    display: flex;
    gap: 20rpx;
    padding: 30rpx;
    border-top: 1rpx solid #f0f0f0;
}

.cancel-btn {
    flex: 1;
    background: #f5f5f5;
    color: #666;
    padding: 25rpx;
    border-radius: 15rpx;
    text-align: center;
    font-size: 28rpx;
}

.confirm-btn {
    flex: 1;
    background: #667eea;
    color: white;
    padding: 25rpx;
    border-radius: 15rpx;
    text-align: center;
    font-size: 28rpx;
}
</style>
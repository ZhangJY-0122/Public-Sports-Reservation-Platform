<template>
  <view class="demo-page">
    <!-- 页面标题 -->
    <view class="header">
      <text class="title">场馆图片展示</text>
      <text class="subtitle">使用您上传的场馆图片</text>
    </view>
    
    <!-- 单个场馆图片卡片 -->
    <view class="section">
      <text class="section-title">主要场馆展示</text>
	  <button type="primary" @click="subbooking">提交预约</button>
      <venue-image-card
        :venue-name="detail.name"
        :venue-image="detail.image"
        :location="detail.location"
        :category="detail.category.name"
        :price="detail.price"
        :rating="4.9"
        :features="['免费停车', '24小时营业', '专业教练', '器材齐全']"
      />
    </view>
    
    <!-- 场馆详情展示 -->
    <view class="section">
      <text class="section-title">场馆详细信息</text>
      <view class="venue-detail">
        <!-- 主要图片展示 -->
        <view class="main-image-container">
          <image 
            :src="venueDetail.mainImage" 
            mode="aspectFill"
            class="main-image"
            @click="previewImage(venueDetail.mainImage)"
          />
          <view class="image-indicator">
            <text class="indicator-text">1 / {{ venueDetail.images.length }}</text>
          </view>
        </view>
        
        <!-- 缩略图列表 -->
    <!--    <view class="thumbnail-list">
          <view 
            v-for="(thumb, index) in venueDetail.images" 
            :key="index"
            class="thumbnail"
            :class="{ active: currentImageIndex === index }"
            @click="selectImage(index)"
          >
            <image :src="thumb" mode="aspectFill" />
          </view>
        </view> -->
        
        <!-- 场馆信息 -->
        <view class="venue-intro">
          <view class="intro-header">
            <text class="intro-title">{{ detail.name }}</text>
            <view class="intro-rating">
              <text class="star">⭐</text>
			
              <text class="score">{{ venueDetail.rating }}</text><br/>
			    <text >价格:{{detail.price}}</text>
              <text class="review-count">({{ venueDetail.reviewCount }}条评价)</text>
            </view>
          </view>
          
          <view class="intro-tags">
            <text 
              v-for="tag in venueDetail.tags" 
              :key="tag"
              class="tag"
            >{{ tag }}</text>
          </view>
          
          <view class="intro-description">
            <text>{{ venueDetail.description }}</text>
          </view>
          
          <view class="intro-facilities">
            <text class="facilities-title">设施服务:</text>
            <view class="facilities-list">
              <text 
                v-for="facility in venueDetail.facilities" 
                :key="facility"
                class="facility-item"
              >{{ facility }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 新增评论区域 -->
    <view class="section">
      <text class="section-title">用户评价 ({{ venueDetail.reviewCount }})</text>
      
      <!-- 评分概览 -->
      <view class="rating-overview">
        <view class="overall-rating">
          <text class="rating-score">{{ venueDetail.rating }}</text>
          <text class="rating-text">综合评分</text>
          <view class="rating-stars">
            <text class="star">⭐</text>
            <text class="star">⭐</text>
            <text class="star">⭐</text>
            <text class="star">⭐</text>
            <text class="star">⭐</text>
          </view>
        </view>
        <view class="rating-details">
          <view class="rating-item" v-for="(item, index) in ratingDetails" :key="index">
            <text class="rating-label">{{ item.label }}</text>
            <view class="rating-bar">
              <view class="rating-progress" :style="{ width: item.percentage + '%' }"></view>
            </view>
            <text class="rating-percentage">{{ item.percentage }}%</text>
          </view>
        </view>
      </view>
      
      <!-- 评论列表 -->
      <view class="comments-list">
        <view 
          v-for="(comment, index) in comments" 
          :key="index"
          class="comment-item"
        >
          <view class="comment-header">
            <view class="user-info">
              <image src="/static/images/avatar1.jpg" class="user-avatar" />
              <view class="user-details">
                <text class="user-name">{{ comment.user.username }}</text>
                <view class="comment-rating">
                  <text class="star">⭐</text>
                  <text class="rating-value">{{ comment.rating }}</text>
                </view>
              </view>
            </view>
            <text class="comment-time">{{ comment.time }}</text>
          </view>
          
          <view class="comment-content">
            <text>{{ comment.content }}</text>
          </view>
          
          <view class="comment-images" v-if="comment.images && comment.images.length > 0">
            <view 
              v-for="(img, imgIndex) in comment.images" 
              :key="imgIndex"
              class="comment-image"
              @click="previewImage(img)"
            >
              <image :src="img" mode="aspectFill" />
            </view>
          </view>
          
          <view class="comment-actions">
            <view class="action-item">
              <text class="iconfont icon-like">👍</text>
              <text class="action-count">{{ comment.likes }}</text>
            </view>
            <view class="action-item" @click="replyComment(comment)">
              <text class="iconfont icon-comment">💬</text>
              <text class="action-count">回复</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 加载更多 -->
   <!--   <view class="load-more" v-if="hasMoreComments" @click="loadMoreComments">
        <text>加载更多评价</text>
      </view> -->
    </view>

    <!-- 发表评论区域 -->
    <view class="comment-form-section">
      <view class="comment-form">
        <view class="form-title">发表评价</view>
        
        <!-- 评分选择 -->
        <view class="rating-select">
          <text class="rating-label">评分:</text>
          <view class="stars-select">
            <text 
              v-for="n in 5" 
              :key="n"
              class="star-select"
              :class="{ active: n <= newComment.rating }"
              @click="setRating(n)"
            >⭐</text>
          </view>
          <text class="rating-value-text">{{ newComment.rating }}分</text>
        </view>
        
        <!-- 评论内容 -->
        <view class="comment-input-wrapper">
          <textarea 
            v-model="newComment.content"
            class="comment-input"
            placeholder="请写下您的评价..."
            maxlength="500"
          ></textarea>
          <text class="char-count">{{ newComment.content.length }}/500</text>
        </view>
        
        <!-- 图片上传 -->
      <!--  <view class="image-upload">
          <text class="upload-label">上传图片 (可选)</text>
          <view class="uploaded-images">
            <view 
              v-for="(img, index) in newComment.images" 
              :key="index"
              class="uploaded-image"
            >
              <image :src="img" mode="aspectFill" />
              <view class="remove-image" @click="removeImage(index)">×</view>
            </view>
            <view 
              class="upload-btn"
              @click="chooseImage"
              v-if="newComment.images.length < 3"
            >
              <text class="iconfont icon-add">+</text>
              <text class="upload-text">添加图片</text>
            </view>
          </view>
        </view> -->
        
        <!-- 提交按钮 -->
        <button 
          class="submit-btn"
          :class="{ disabled: !canSubmit }"
          @click="submitComment"
          :disabled="!canSubmit"
        >
          提交评价
        </button>
      </view>
    </view>
  </view>
</template>

<script setup>
import {onShow,onLoad,onReady} from '@dcloudio/uni-app'

import { ref, reactive,computed } from 'vue'
import { http } from '@/utils/http.js'


// 画廊图片数据
const galleryImages = ref([
  {
    src: '/static/images/场馆2.png',
    title: '市民健身中心',
    description: '现代化综合体育设施'
  },
  {
    src: '/static/images/场馆2.png',
    title: '室内篮球场',
    description: '专业标准篮球场地'
  },
  {
    src: '/static/images/场馆2.png',
    title: '健身区域',
    description: '高端健身器械设备'
  }
])


const detail=ref({
	
})

// 场馆详情数据
const venueDetail = ref({
  mainImage: '/static/images/场馆2.png',
  images: [
    '/static/images/场馆2.png',
    '/static/images/场馆2.png',
    '/static/images/场馆2.png',
    '/static/images/场馆2.png'
  ],
  name: '市民健身中心',
  rating: 4.8,
  reviewCount: 256,
  tags: ['热门推荐', '交通便利', '设施完善'],
  description: '位于市中心的现代化综合体育中心，配备国际标准场馆设施，为市民提供优质的体育运动环境。拥有完善的配套设施和专业的服务团队。',
  facilities: [
    '🏀 室内篮球场',
    '🏃 跑步机区域', 
    '💪 力量训练区',
    '🧘 瑜伽室',
    '🛗 电梯直达',
    '🅿️ 免费停车场',
    '📶 免费WiFi',
    '🛡️ 24小时安保'
  ]
})

const currentImageIndex = ref(0)

// 评分详情
const ratingDetails = ref([
  { label: '环境', percentage: 95 },
  { label: '设施', percentage: 92 },
  { label: '服务', percentage: 88 },
  { label: '性价比', percentage: 85 }
])

// 评论数据
const comments = ref([
  {
    id: 1,
    userName: '运动达人小王',
    avatar: '/static/images/avatar1.jpg',
    rating: 5,
    content: '这个场馆设施非常齐全，环境也很干净整洁。教练很专业，指导很到位。强烈推荐！',
    time: '2023-10-15',
    likes: 24,
    images: ['/static/images/场馆2.png', '/static/images/场馆2.png']
  },
  {
    id: 2,
    userName: '健身爱好者小李',
    avatar: '/static/images/avatar2.jpg',
    rating: 4,
    content: '场馆位置很方便，停车位充足。器材都很新，维护得很好。就是周末人有点多。',
    time: '2023-10-10',
    likes: 18,
    images: ['/static/images/场馆2.png']
  },
  {
    id: 3,
    userName: '篮球爱好者小张',
    avatar: '/static/images/avatar3.jpg',
    rating: 5,
    content: '篮球场地板很棒，灯光也很专业。每周都会和朋友来这里打球，体验很好！',
    time: '2023-10-05',
    likes: 32,
    images: []
  }
])

// 新评论数据
const newComment = ref({
  rating: 5,
  content: '',
  images: []
})

// 分页相关
const hasMoreComments = ref(true)

// 计算属性
const canSubmit = computed(() => {
  return newComment.value.content.trim().length > 0
})

// 方法
const previewImage = (imageSrc) => {
  uni.previewImage({
    urls: [imageSrc],
    current: imageSrc
  })
}

const selectImage = (index) => {
  currentImageIndex.value = index
  venueDetail.value.mainImage = venueDetail.value.images[index]
}

const setRating = (rating) => {
  newComment.value.rating = rating
}

const chooseImage = () => {
  uni.chooseImage({
    count: 3 - newComment.value.images.length,
    sizeType: ['compressed'],
    sourceType: ['album'],
    success: (res) => {
      newComment.value.images = [...newComment.value.images, ...res.tempFilePaths]
    }
  })
}

const removeImage = (index) => {
  newComment.value.images.splice(index, 1)
}

const submitComment = () => {
  if (!canSubmit.value) return
  let user=uni.getStorageSync("user")
  // 模拟提交评论
  const comment = {

    user_id: user.user_id,
    rating: newComment.value.rating,
    content: newComment.value.content,

    // likes: 0,
    // images: [...newComment.value.images]
  }
  http.post(`venue/${cg_id.value}/reviews`,comment).then(res=>{
	  
  })
  comments.value.unshift(comment)
  venueDetail.value.reviewCount++
  
  // 重置表单
  newComment.value = {
    rating: 5,
    content: '',
    images: []
  }
  
  uni.showToast({
    title: '评价提交成功',
    icon: 'success'
  })
}

const loadMoreComments = () => {
  // 模拟加载更多评论
  setTimeout(() => {
    const moreComments = [
      {
        id: comments.value.length + 1,
        userName: '瑜伽爱好者小刘',
        avatar: '/static/images/avatar4.jpg',
        rating: 4,
        content: '瑜伽室环境很好，很安静。教练很专业，课程安排合理。',
        time: '2023-09-28',
        likes: 15,
        images: []
      },
      {
        id: comments.value.length + 2,
        userName: '跑步爱好者小陈',
        avatar: '/static/images/avatar5.jpg',
        rating: 5,
        content: '跑步机很新，维护得很好。空调温度适中，跑步很舒服。',
        time: '2023-09-25',
        likes: 21,
        images: ['/static/images/场馆2.png']
      }
    ]
    
    comments.value = [...comments.value, ...moreComments]
    hasMoreComments.value = false // 模拟没有更多数据
  }, 1000)
}

const replyComment = (comment) => {
  uni.showToast({
    title: `回复 ${comment.userName} 的评论`,
    icon: 'none'
  })
}

const loaddetail=(id)=>{
	http.get("venue/"+id).then(res=>{
		detail.value=res
	})
}

const comment_list=ref([])

const loadcomment=(id)=>{
	http.get(`venue/${id}/reviews `).then(res=>{
		comment_list.value=res
		comments.value=res.reviews
	})
}
const cg_id=ref(0)
onLoad((option)=>{
	//获取url的参数
	let id=option.id
	console.log(id,"接收到的id");
	cg_id.value=id
	loaddetail(id)
	loadcomment(id)
	
	
})


const subbooking=()=>{
	
	uni.navigateTo({
		url:"/pages/cgbookin/booking?id="+cg_id.value
	})
}
</script>

<style scoped>
.demo-page {
  background: #f5f7fa;
  min-height: 100vh;
  padding-bottom: 40rpx;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60rpx 32rpx 40rpx;
  text-align: center;
  color: white;
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 16rpx;
}

.subtitle {
  font-size: 28rpx;
  opacity: 0.9;
}

.section {
  margin: 32rpx;
}

.section-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 24rpx;
  display: block;
}

.venue-detail {
  background: white;
  border-radius: 20rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.main-image-container {
  position: relative;
  width: 100%;
  height: 500rpx;
}

.main-image {
  width: 100%;
  height: 100%;
}

.image-indicator {
  position: absolute;
  bottom: 20rpx;
  right: 20rpx;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
}

.indicator-text {
  font-size: 24rpx;
}

.thumbnail-list {
  display: flex;
  gap: 16rpx;
  padding: 24rpx;
  overflow-x: auto;
}

.thumbnail {
  width: 120rpx;
  height: 80rpx;
  border-radius: 12rpx;
  overflow: hidden;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.thumbnail.active {
  opacity: 1;
  border: 4rpx solid #667eea;
}

.thumbnail image {
  width: 100%;
  height: 100%;
}

.venue-intro {
  padding: 32rpx;
}

.intro-header {
  margin-bottom: 24rpx;
}

.intro-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #2c3e50;
  display: block;
  margin-bottom: 12rpx;
}

.intro-rating {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.star {
  font-size: 28rpx;
}

.score {
  font-size: 28rpx;
  font-weight: bold;
  color: #ff6b6b;
}

.review-count {
  font-size: 24rpx;
  color: #666;
}

.intro-tags {
  display: flex;
  gap: 12rpx;
  margin-bottom: 24rpx;
  flex-wrap: wrap;
}

.tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
}

.intro-description {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 32rpx;
}

.intro-facilities {
  border-top: 2rpx solid #f0f0f0;
  padding-top: 32rpx;
}

.facilities-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2c3e50;
  display: block;
  margin-bottom: 20rpx;
}

.facilities-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.facility-item {
  background: #f8f9fa;
  padding: 12rpx 20rpx;
  border-radius: 24rpx;
  font-size: 26rpx;
  color: #666;
  border: 2rpx solid #e9ecef;
}

/* 评论区域样式 */
.rating-overview {
  background: white;
  border-radius: 20rpx;
  padding: 32rpx;
  display: flex;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.overall-rating {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 60rpx;
}

.rating-score {
  font-size: 48rpx;
  font-weight: bold;
  color: #ff6b6b;
  margin-bottom: 8rpx;
}

.rating-text {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 16rpx;
}

.rating-stars {
  display: flex;
  gap: 4rpx;
}

.rating-details {
  flex: 1;
}

.rating-item {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.rating-label {
  font-size: 26rpx;
  color: #666;
  width: 120rpx;
}

.rating-bar {
  flex: 1;
  height: 12rpx;
  background: #f0f0f0;
  border-radius: 6rpx;
  margin: 0 16rpx;
  overflow: hidden;
}

.rating-progress {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 6rpx;
  transition: width 0.5s ease;
}

.rating-percentage {
  font-size: 24rpx;
  color: #666;
  width: 60rpx;
  text-align: right;
}

.comments-list {
  margin-bottom: 24rpx;
}

.comment-item {
  background: white;
  border-radius: 20rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20rpx;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  margin-right: 20rpx;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 8rpx;
}

.comment-rating {
  display: flex;
  align-items: center;
  gap: 4rpx;
}

.rating-value {
  font-size: 24rpx;
  color: #ff6b6b;
}

.comment-time {
  font-size: 24rpx;
  color: #999;
}

.comment-content {
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
  margin-bottom: 20rpx;
}

.comment-images {
  display: flex;
  gap: 16rpx;
  margin-bottom: 20rpx;
  overflow-x: auto;
}

.comment-image {
  width: 200rpx;
  height: 150rpx;
  border-radius: 12rpx;
  overflow: hidden;
  flex-shrink: 0;
}

.comment-image image {
  width: 100%;
  height: 100%;
}

.comment-actions {
  display: flex;
  gap: 40rpx;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  font-size: 24rpx;
  color: #666;
}

.load-more {
  text-align: center;
  padding: 24rpx;
  background: white;
  border-radius: 20rpx;
  color: #667eea;
  font-size: 28rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

/* 评论表单样式 */
.comment-form-section {
  margin: 32rpx;
}

.comment-form {
  background: white;
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.form-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 24rpx;
}

.rating-select {
  display: flex;
  align-items: center;
  margin-bottom: 32rpx;
}

.rating-label {
  font-size: 28rpx;
  color: #333;
  margin-right: 20rpx;
}

.stars-select {
  display: flex;
  gap: 8rpx;
  margin-right: 20rpx;
}

.star-select {
  font-size: 40rpx;
  opacity: 0.3;
  transition: opacity 0.3s ease;
}

.star-select.active {
  opacity: 1;
}

.rating-value-text {
  font-size: 24rpx;
  color: #ff6b6b;
  font-weight: bold;
}

.comment-input-wrapper {
  position: relative;
  margin-bottom: 32rpx;
}

.comment-input {
  width: 100%;
  height: 200rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #333;
  box-sizing: border-box;
  border: 2rpx solid #e9ecef;
}

.char-count {
  position: absolute;
  bottom: 10rpx;
  right: 10rpx;
  font-size: 22rpx;
  color: #999;
}

.image-upload {
  margin-bottom: 32rpx;
}

.upload-label {
  font-size: 28rpx;
  color: #333;
  display: block;
  margin-bottom: 16rpx;
}

.uploaded-images {
  display: flex;
  gap: 16rpx;
  flex-wrap: wrap;
}

.uploaded-image {
  position: relative;
  width: 160rpx;
  height: 120rpx;
  border-radius: 12rpx;
  overflow: hidden;
}

.uploaded-image image {
  width: 100%;
  height: 100%;
}

.remove-image {
  position: absolute;
  top: 4rpx;
  right: 4rpx;
  width: 32rpx;
  height: 32rpx;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20rpx;
}

.upload-btn {
  width: 160rpx;
  height: 120rpx;
  border: 2rpx dashed #ddd;
  border-radius: 12rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.upload-text {
  font-size: 22rpx;
  margin-top: 8rpx;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50rpx;
  padding: 24rpx;
  font-size: 30rpx;
  font-weight: bold;
}

.submit-btn.disabled {
  background: #ccc;
  color: #999;
}
</style>
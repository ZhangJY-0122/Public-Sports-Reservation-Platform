<template>
  <el-container class="layout-container" style="height: 100vh">
    <!-- 侧边栏 -->
    <el-aside width="220px" class="sidebar">
      <div class="logo-container">
        <h2 class="logo-text">{{ systemSettings.title }}</h2>
      </div>
      <div class="sidebar-menu-container">
        <el-menu
          class="sidebar-menu"
          :default-active="$route.path"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
          router
          unique-opened
        >
          <!-- 首页 -->
          <el-menu-item index="/common/index">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>

          <!-- 数据分析 -->
          <el-sub-menu index="analysis">
            <template #title>
              <el-icon><TrendCharts /></el-icon>
              <span>数据分析</span>
            </template>
            <el-menu-item index="/common/business-analysis">场馆营业分析</el-menu-item>
          </el-sub-menu>
          
          <!-- 基础资料 -->
          <el-sub-menu index="basic">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>基础资料</span>
            </template>
 
            <el-menu-item index="/venues/list">场馆管理</el-menu-item>
            <el-menu-item index="/venue/categories">场馆分类管理</el-menu-item>
            <el-menu-item index="/coach/list">教练管理</el-menu-item>
            <el-menu-item index="/activities/list">活动管理</el-menu-item>
            <el-menu-item index="/bookings/list">预约管理</el-menu-item>
            <!-- <el-menu-item index="/booking_shares/list">预约分摊管理</el-menu-item> -->
            <el-menu-item index="/coach_bookings/list">教练预约管理</el-menu-item>
            <el-menu-item index="/events/list">赛事管理</el-menu-item>
            <!-- <el-menu-item index="/event_registrations/list">赛事报名管理</el-menu-item> -->
            <!-- <el-menu-item index="/friends/list">朋友关系管理</el-menu-item>
            <el-menu-item index="/friendships/list">好友关系管理</el-menu-item> -->
            <el-menu-item index="/venue_reviews/list">场馆评价管理</el-menu-item>

          </el-sub-menu>

          <!-- 权限管理 -->
          <el-sub-menu index="permission">
            <template #title>
              <el-icon><Lock /></el-icon>
              <span>权限管理</span>
            </template>
            <el-menu-item index="/user/list">用户管理</el-menu-item>
            <el-menu-item index="/user/rolelist">角色管理</el-menu-item>
            <el-menu-item index="/user/menulist">菜单管理</el-menu-item>
          </el-sub-menu>

  
</el-menu>
    
      </div>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-left">
          <span class="system-name">{{ systemSettings.title }}</span>
        </div>
        <div class="header-right">
          <div class="user-info">
            <el-icon class="user-icon"><User /></el-icon>
            <span class="user-name">{{ userStore.userInfo.name || '未知用户' }}</span>
          </div>
          <el-dropdown @command="handleCommand" class="dropdown">
            <span class="dropdown-link">
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 主内容区域 -->
      <el-main class="main-content">
        <div class="content-wrapper">
          <router-view />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores'
import { systemSettings } from '@/config/settings'
import { 
  House, 
  Document, 
  Lock, 
  Setting, 
  InfoFilled, 
  Box, 
  User, 
  ArrowDown,
  TrendCharts
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

// 下拉菜单命令处理
const handleCommand = (command) => {
  if (command === 'logout') {
    logout()
  } else if (command === 'profile') {
    // 跳转到个人中心页面
    // router.push('/profile')
    ElMessage.info('个人中心功能开发中...')
  }
}

// 退出登录
const logout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.clearUserInfo()
    ElMessage.success('退出成功')
    router.push('/login')
  }).catch(() => {
    // 用户取消操作
  })
}

onMounted(() => {
  console.log('登录用户信息:', userStore.userInfo)
})
</script>

<style scoped>
.layout-container {
  overflow: hidden;
}

/* 侧边栏样式 */
.sidebar {
  background-color: #304156;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
  display: flex;
  flex-direction: column;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}

.logo-text {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.sidebar-menu-container {
  flex: 1;
  overflow: hidden;
}

.sidebar-menu {
  border: none;
  height: 100%;
  overflow-y: auto;
}

/* 隐藏滚动条但保留滚动功能 */
.sidebar-menu::-webkit-scrollbar {
  display: none;
}

.sidebar-menu {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
  margin: 2px 0;
}

.sidebar-menu .el-menu-item.is-active {
  background-color: #5431d2 !important;
}

.sidebar-menu .el-sub-menu .el-menu-item {
  height: 45px;
  line-height: 45px;
  min-width: auto;
}

/* 顶部导航栏样式 */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  z-index: 1;
}

.header-left {
  display: flex;
  align-items: center;
}

.system-name {
  font-size: 20px;
  font-weight: bold;
  color: #1890ff;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  margin-right: 15px;
}

.user-icon {
  margin-right: 8px;
  color: #1890ff;
}

.user-name {
  font-weight: 500;
  color: #333;
}

.dropdown-link {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #666;
  transition: color 0.3s;
}

.dropdown-link:hover {
  color: #2206c5;
}

/* 主内容区域样式 */
.main-container {
  overflow: hidden;
}

.main-content {
  padding: 0;
  background-color: #f0f2f5;
  overflow: auto;
}

/* 隐藏主内容区域的滚动条 */
.main-content::-webkit-scrollbar {
  display: none;
}

.main-content {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.content-wrapper {
  min-height: calc(100vh - 60px);
  padding: 20px;
  background-color: #fff;
  margin: 20px;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .sidebar {
    width: 64px !important;
  }
  
  .logo-text {
    display: none;
  }
  
  .system-name {
    display: none;
  }
  
  .user-name {
    display: none;
  }
  
  .content-wrapper {
    margin: 10px;
    padding: 15px;
  }
}

/* 菜单项悬停效果优化 */
.sidebar-menu .el-menu-item:hover,
.sidebar-menu .el-sub-menu__title:hover {
  background-color: #263445 !important;
}

/* 子菜单背景色优化 */
.sidebar-menu .el-menu--inline {
  background-color: #1f2d3d !important;
}
</style>
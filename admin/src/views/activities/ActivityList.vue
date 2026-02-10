<template>
  <div class="activity-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>活动管理</h2>
      <el-button type="primary" @click="handleAdd">发布活动</el-button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-form :model="searchForm" inline>
        <el-form-item label="活动标题">
          <el-input v-model="searchForm.title" placeholder="请输入活动标题" clearable style="width: 200px"></el-input>
        </el-form-item>
        <el-form-item label="活动类型">
          <el-select v-model="searchForm.activity_type" placeholder="请选择活动类型" clearable style="width: 150px">
            <el-option label="训练营" value="training"></el-option>
            <el-option label="比赛" value="competition"></el-option>
            <el-option label="讲座" value="lecture"></el-option>
            <el-option label="体验课" value="trial"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 120px">
            <el-option label="未开始" value="upcoming"></el-option>
            <el-option label="进行中" value="ongoing"></el-option>
            <el-option label="已结束" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch" :loading="loading">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 活动列表 -->
    <div class="activity-list-container">
      <div v-if="loading" class="loading-container">
        <el-icon class="loading-icon" :size="32">
          <Loading />
        </el-icon>
        <p>加载中...</p>
      </div>

      <div v-else-if="activities.length === 0" class="empty-state">
        <el-empty description="暂无活动数据"></el-empty>
      </div>

      <div v-else class="activity-grid">
        <div v-for="activity in activities" :key="activity.id" class="activity-card" @click="handleView(activity)">
          <div class="card-image">
            <img :src="activity.image || '/static/default-activity.png'" :alt="activity.title" />
            <div class="status-badge" :class="`status-${activity.status}`">
              {{ getStatusText(activity.status) }}
            </div>
          </div>

          <div class="card-content">
            <h3 class="activity-title">{{ activity.title }}</h3>
            <div class="activity-meta">
              <div class="meta-item">
                <el-icon>
                  <Calendar />
                </el-icon>
                <span>{{ formatDate(activity.start_date) }}</span>
              </div>
              <div class="meta-item">
                <el-icon>
                  <Clock />
                </el-icon>
                <span>{{ activity.start_time }}-{{ activity.end_time }}</span>
              </div>
              <div class="meta-item">
                <el-icon>
                  <Location />
                </el-icon>
                <span>{{ activity.location }}</span>
              </div>
            </div>

            <div class="activity-info">
              <div class="info-item">
                <span class="label">类型：</span>
                <span>{{ getActivityTypeText(activity.activity_type) }}</span>
              </div>
              <div class="info-item">
                <span class="label">参与：</span>
                <span>{{ activity.current_participants }}/{{ activity.max_participants }}</span>
              </div>
              <div class="info-item" v-if="activity.registration_fee && activity.registration_fee !== '0'">
                <span class="label">费用：</span>
                <span>¥{{ activity.registration_fee }}</span>
              </div>
            </div>

            <div class="card-actions">
              <el-button size="small" @click.stop="handleEdit(activity)">编辑</el-button>
              <el-button size="small" type="danger" @click.stop="handleDelete(activity)">删除</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 调试信息 -->
    <div class="debug-info" v-if="showDebug">
      <h4>调试信息：</h4>
      <p>数据数组长度: {{ activities.length }}</p>
      <p>总记录数: {{ pagination.total }}</p>
      <p>加载状态: {{ loading ? '加载中...' : '已完成' }}</p>
      <p>分页参数: page={{ pagination.current_page }}, size={{ pagination.page_size }}</p>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="pagination.total > 0">
      <el-pagination v-model:current-page="pagination.current_page" v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]" :total="pagination.total" layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange" @current-change="handleCurrentChange" />
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog :title="dialogMode === 'add' ? '发布活动' : '编辑活动'" v-model="dialogVisible" width="700px" @close="resetForm">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="活动标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入活动标题"></el-input>
        </el-form-item>

        <el-form-item label="活动描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入活动描述"></el-input>
        </el-form-item>

        <el-form-item label="活动类型" prop="activity_type">
          <el-select v-model="form.activity_type" placeholder="请选择活动类型" style="width: 100%">
            <el-option label="训练营" value="training"></el-option>
            <el-option label="比赛" value="competition"></el-option>
            <el-option label="讲座" value="lecture"></el-option>
            <el-option label="体验课" value="trial"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>

        <!-- 修改后的活动图片字段 -->
        <el-form-item label="活动图片" prop="image">
          <div class="image-upload-container">
            <div class="upload-section">
              <el-input v-model="form.image" placeholder="请输入图片URL或上传图片" style="margin-bottom: 10px" />
              <el-upload class="upload-demo" :action="baseURL + '/api/upload'" :show-file-list="false"
                :before-upload="beforeUpload" :on-success="handleUploadSuccess" :on-error="handleUploadError"
                accept=".jpg,.jpeg,.png,.gif,.webp">
                <el-button type="primary">上传图片</el-button>
                <template #tip>
                  <div class="el-upload__tip">
                    支持 jpg、png、gif、webp 格式，大小不超过 2MB
                  </div>
                </template>
              </el-upload>
            </div>

            <!-- 图片预览 -->
            <div class="image-preview" v-if="form.image">
              <div class="preview-container">
                <img :src="form.image" alt="活动图片预览" class="preview-image" />
                <div class="preview-actions">
                  <el-button type="danger" size="small" @click="clearImage" :icon="Delete">
                    清除
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </el-form-item>

        <el-form-item label="活动时间" required>
          <div class="time-group">
            <el-form-item prop="start_date" style="margin-right: 10px">
              <el-date-picker v-model="form.start_date" type="date" placeholder="开始日期" format="YYYY-MM-DD"
                value-format="YYYY-MM-DD" style="width: 140px" />
            </el-form-item>
            <el-form-item prop="end_date" style="margin-right: 10px">
              <el-date-picker v-model="form.end_date" type="date" placeholder="结束日期" format="YYYY-MM-DD"
                value-format="YYYY-MM-DD" style="width: 140px" />
            </el-form-item>
          </div>
        </el-form-item>

        <el-form-item label="具体时间" required>
          <div class="time-group">
            <el-form-item prop="start_time" style="margin-right: 10px">
              <el-time-picker v-model="form.start_time" placeholder="开始时间" format="HH:mm" value-format="HH:mm"
                style="width: 140px" />
            </el-form-item>
            <el-form-item prop="end_time">
              <el-time-picker v-model="form.end_time" placeholder="结束时间" format="HH:mm" value-format="HH:mm"
                style="width: 140px" />
            </el-form-item>
          </div>
        </el-form-item>

        <el-form-item label="活动地点" prop="location">
          <el-input v-model="form.location" placeholder="请输入活动地点"></el-input>
        </el-form-item>

        <el-form-item label="参与人数" required>
          <div class="participants-group">
            <el-form-item prop="max_participants">
              <el-input-number v-model="form.max_participants" :min="1" placeholder="最大参与人数" />
            </el-form-item>
          </div>
        </el-form-item>

        <el-form-item label="报名费用" prop="registration_fee">
          <el-input-number v-model="form.registration_fee" :min="0" :precision="2" placeholder="报名费用（元）" />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="未开始" value="upcoming"></el-option>
            <el-option label="进行中" value="ongoing"></el-option>
            <el-option label="已结束" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="form.is_active"></el-switch>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看活动详情对话框 -->
    <el-dialog title="活动详情" v-model="viewDialogVisible" width="700px">
      <div v-if="currentActivity" class="activity-detail">
        <div class="detail-header">
          <img :src="currentActivity.image || '/static/default-activity.png'" :alt="currentActivity.title"
            class="detail-image" />
          <div class="detail-title">
            <h2>{{ currentActivity.title }}</h2>
            <div class="detail-status">
              <el-tag :type="getStatusTagType(currentActivity.status)">
                {{ getStatusText(currentActivity.status) }}
              </el-tag>
              <el-tag>{{ getActivityTypeText(currentActivity.activity_type) }}</el-tag>
            </div>
          </div>
        </div>

        <el-descriptions :column="2" border class="detail-descriptions">
          <el-descriptions-item label="活动ID">{{ currentActivity.id }}</el-descriptions-item>
          <el-descriptions-item label="创建者">{{ currentActivity.organizer || '系统' }}</el-descriptions-item>
          <el-descriptions-item label="开始日期">{{ formatDate(currentActivity.start_date) }}</el-descriptions-item>
          <el-descriptions-item label="结束日期">{{ formatDate(currentActivity.end_date) }}</el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ currentActivity.start_time }}</el-descriptions-item>
          <el-descriptions-item label="结束时间">{{ currentActivity.end_time }}</el-descriptions-item>
          <el-descriptions-item label="活动地点">{{ currentActivity.location }}</el-descriptions-item>
          <el-descriptions-item label="最大参与人数">{{ currentActivity.max_participants }}人</el-descriptions-item>
          <el-descriptions-item label="当前参与人数">
            <span
              :class="{ 'full-capacity': currentActivity.current_participants >= currentActivity.max_participants }">
              {{ currentActivity.current_participants }}人
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="报名费用">
            {{ currentActivity.registration_fee && currentActivity.registration_fee !== '0' ? '¥' +
              currentActivity.registration_fee : '免费' }}
          </el-descriptions-item>
          <el-descriptions-item label="是否启用">
            <el-tag :type="currentActivity.is_active ? 'success' : 'danger'">
              {{ currentActivity.is_active ? '已启用' : '已禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDateTime(currentActivity.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="活动描述" :span="2">
            <div class="description-content">{{ currentActivity.description || '暂无描述' }}</div>
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleEdit(currentActivity)">编辑</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Calendar,
  Clock,
  Location,
  Loading,
  Delete
} from '@element-plus/icons-vue'

// API基础配置
const API_BASE = '/api/activity'

import { activityApi } from '@/api/activity'
import request, { baseURL } from '@/utils/request'
// 响应式数据
const loading = ref(false)
const submitLoading = ref(false)
const showDebug = ref(true)
const dialogVisible = ref(false)
const viewDialogVisible = ref(false)
const dialogMode = ref('add')
const currentActivity = ref(null)
const formRef = ref(null)

// 活动数据
const activities = ref([])
const pagination = reactive({
  current_page: 1,
  page_size: 20,
  total: 0,
  total_pages: 0
})

// 搜索表单
const searchForm = reactive({
  title: '',
  activity_type: '',
  status: ''
})

// 表单数据
const form = reactive({
  id: null,
  title: '',
  description: '',
  activity_type: '',
  image: '',
  start_date: '',
  end_date: '',
  start_time: '',
  end_time: '',
  location: '',
  max_participants: 1,
  registration_fee: 0,
  status: 'upcoming',
  is_active: true
})

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入活动标题', trigger: 'blur' },
    { min: 2, max: 100, message: '活动标题长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  activity_type: [
    { required: true, message: '请选择活动类型', trigger: 'change' }
  ],
  start_date: [
    { required: true, message: '请选择开始日期', trigger: 'change' }
  ],
  end_date: [
    { required: true, message: '请选择结束日期', trigger: 'change' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ],
  location: [
    { required: true, message: '请输入活动地点', trigger: 'blur' }
  ],
  max_participants: [
    { required: true, message: '请输入最大参与人数', trigger: 'blur' },
    { type: 'number', min: 1, message: '最大参与人数至少为1', trigger: 'blur' }
  ]
}

// 方法定义
const getActivityTypeText = (type) => {
  const typeMap = {
    'training': '训练营',
    'competition': '比赛',
    'lecture': '讲座',
    'trial': '体验课',
    'other': '其他'
  }
  return typeMap[type] || type
}

const getStatusText = (status) => {
  const statusMap = {
    'upcoming': '未开始',
    'ongoing': '进行中',
    'completed': '已结束',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

const getStatusTagType = (status) => {
  const typeMap = {
    'upcoming': 'primary',
    'ongoing': 'success',
    'completed': 'info',
    'cancelled': 'danger'
  }
  return typeMap[status] || 'info'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return ''
  return new Date(dateTimeStr).toLocaleString('zh-CN')
}

// 上传相关方法
const beforeUpload = (file) => {
  const isImage = /\.(jpg|jpeg|png|gif|webp)$/i.test(file.name)
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片格式文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

const handleUploadSuccess = (response, file) => {
  if (response.code === 0) {
    // 假设后端返回的数据结构为 { code: 0, data: { url: '图片路径' } }
    form.image = response.data.url || response.data
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error(response.message || '图片上传失败')
  }
}

const handleUploadError = (error) => {
  console.error('上传失败:', error)
  ElMessage.error('图片上传失败，请重试')
}

const clearImage = () => {
  form.image = ''
}

// 获取活动列表
const fetchActivities = async () => {
  try {
    loading.value = true

    const params = new URLSearchParams({
      page: pagination.current_page,
      page_size: pagination.page_size
    })

    // 添加搜索参数
    if (searchForm.title.trim()) {
      params.append('title', searchForm.title.trim())
    }
    if (searchForm.activity_type) {
      params.append('activity_type', searchForm.activity_type)
    }
    if (searchForm.status) {
      params.append('status', searchForm.status)
    }

    const response = await activityApi.getActivityList(params)
    const result = await response

    if (result.code === 0) {
      activities.value = result.data.activities || []
      pagination.total = result.data.pagination?.total || 0
      pagination.total_pages = result.data.pagination?.total_pages || 0
    } else {
      ElMessage.error(result.message || '获取活动列表失败')
    }
  } catch (error) {
    console.error('获取活动列表失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current_page = 1
  fetchActivities()
}

// 重置搜索
const resetSearch = () => {
  searchForm.title = ''
  searchForm.activity_type = ''
  searchForm.status = ''
  pagination.current_page = 1
  fetchActivities()
}

// 分页处理
const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.current_page = 1
  fetchActivities()
}

const handleCurrentChange = (page) => {
  pagination.current_page = page
  fetchActivities()
}

// 新增活动
const handleAdd = () => {
  dialogMode.value = 'add'
  resetForm()
  dialogVisible.value = true
}

// 查看活动
const handleView = (activity) => {
  currentActivity.value = { ...activity }
  viewDialogVisible.value = true
}

// 编辑活动
const handleEdit = (activity) => {
  dialogMode.value = 'edit'
  Object.assign(form, {
    id: activity.id,
    title: activity.title,
    description: activity.description || '',
    activity_type: activity.activity_type,
    image: activity.image || '',
    start_date: activity.start_date,
    end_date: activity.end_date,
    start_time: activity.start_time,
    end_time: activity.end_time,
    location: activity.location,
    max_participants: activity.max_participants,
    registration_fee: parseFloat(activity.registration_fee) || 0,
    status: activity.status,
    is_active: activity.is_active
  })
  dialogVisible.value = true
  viewDialogVisible.value = false
}

// 删除活动
const handleDelete = async (activity) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除活动 "${activity.title}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await fetch(`${API_BASE}/delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ ids: [activity.id] })
    })

    const result = await response.json()

    if (result.code === 0) {
      ElMessage.success('删除成功')
      fetchActivities()
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除活动失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    submitLoading.value = true

    const submitData = {
      title: form.title,
      description: form.description,
      activity_type: form.activity_type,
      image: form.image,
      start_date: form.start_date,
      end_date: form.end_date,
      start_time: form.start_time,
      end_time: form.end_time,
      location: form.location,
      max_participants: form.max_participants,
      registration_fee: form.registration_fee,
      status: form.status,
      is_active: form.is_active
    }

    let url = `${API_BASE}/create`
    let method = 'POST'

    if (dialogMode.value === 'edit') {
      url = `${API_BASE}/${form.id}/update`
      method = 'PUT'
    }

    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(submitData)
    })

    const result = await response.json()

    if (result.code === 0) {
      ElMessage.success(dialogMode.value === 'add' ? '创建成功' : '更新成功')
      dialogVisible.value = false
      fetchActivities()
    } else {
      ElMessage.error(result.message || (dialogMode.value === 'add' ? '创建失败' : '更新失败'))
    }
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }

  Object.assign(form, {
    id: null,
    title: '',
    description: '',
    activity_type: '',
    image: '',
    start_date: '',
    end_date: '',
    start_time: '',
    end_time: '',
    location: '',
    max_participants: 1,
    registration_fee: 0,
    status: 'upcoming',
    is_active: true
  })
}

// 页面加载时获取数据
onMounted(() => {
  fetchActivities()
})
</script>

<style scoped>
.activity-list {
  padding: 20px;
  background: #f5f5f5;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.page-header h2 {
  margin: 0;
  color: #333;
  font-weight: 600;
}

.search-bar {
  margin-bottom: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.activity-list-container {
  margin-bottom: 20px;
}

.loading-container,
.empty-state {
  padding: 60px 20px;
  text-align: center;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.activity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.activity-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.activity-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.card-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.status-upcoming {
  background: #409eff;
}

.status-ongoing {
  background: #67c23a;
}

.status-completed {
  background: #909399;
}

.status-cancelled {
  background: #f56c6c;
}

.card-content {
  padding: 20px;
}

.activity-title {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  line-height: 1.4;
}

.activity-meta {
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.meta-item .el-icon {
  margin-right: 8px;
  color: #409eff;
}

.activity-info {
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  margin-bottom: 6px;
  font-size: 14px;
}

.info-item .label {
  color: #666;
  min-width: 60px;
}

.card-actions {
  display: flex;
  gap: 12px;
}

.debug-info {
  margin: 20px 0;
  padding: 16px;
  background: #f0f9ff;
  border: 1px solid #b3d8ff;
  border-radius: 6px;
  font-size: 14px;
}

.debug-info h4 {
  margin: 0 0 12px 0;
  color: #409eff;
}

.debug-info p {
  margin: 4px 0;
  color: #666;
}

.pagination {
  display: flex;
  justify-content: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.time-group,
.participants-group {
  display: flex;
  align-items: center;
  width: 100%;
}

/* 图片上传容器样式 */
.image-upload-container {
  width: 100%;
}

.upload-section {
  margin-bottom: 16px;
}

.upload-demo {
  width: 100%;
}

.image-preview {
  margin-top: 12px;
}

.preview-container {
  position: relative;
  display: inline-block;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 8px;
  background: #fafafa;
}

.preview-image {
  max-width: 200px;
  max-height: 150px;
  border-radius: 4px;
  display: block;
}

.preview-actions {
  margin-top: 8px;
  text-align: center;
}

:deep(.el-upload) {
  width: 100%;
}

:deep(.el-upload .el-button) {
  width: 100%;
}

:deep(.el-upload__tip) {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

.activity-detail {
  max-height: 70vh;
  overflow-y: auto;
}

.detail-header {
  display: flex;
  margin-bottom: 24px;
  gap: 20px;
}

.detail-image {
  width: 200px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.detail-title {
  flex: 1;
}

.detail-title h2 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 24px;
}

.detail-status {
  display: flex;
  gap: 8px;
}

.detail-descriptions {
  margin-top: 20px;
}

.description-content {
  line-height: 1.6;
  color: #666;
}

.full-capacity {
  color: #f56c6c;
  font-weight: 500;
}

:deep(.el-descriptions__label) {
  font-weight: 600;
  color: #333;
}

:deep(.el-descriptions__content) {
  color: #666;
}

@media (max-width: 768px) {
  .activity-grid {
    grid-template-columns: 1fr;
  }

  .detail-header {
    flex-direction: column;
  }

  .detail-image {
    width: 100%;
    height: 200px;
  }

  .preview-image {
    max-width: 100%;
  }
}
</style>
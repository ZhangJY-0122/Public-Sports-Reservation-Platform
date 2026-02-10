<template>
  <div class="event-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>赛事管理</h2>
      <el-button type="primary" @click="handleAdd">发布赛事</el-button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-form :model="searchForm" inline>
        <el-form-item label="赛事名称">
          <el-input v-model="searchForm.name" placeholder="请输入赛事名称" clearable style="width: 200px"></el-input>
        </el-form-item>
        <el-form-item label="赛事类型">
          <el-select v-model="searchForm.event_type" placeholder="请选择赛事类型" clearable style="width: 150px">
            <el-option label="训练营" value="training"></el-option>
            <el-option label="比赛" value="competition"></el-option>
            <el-option label="锦标赛" value="championship"></el-option>
            <el-option label="联赛" value="league"></el-option>
            <el-option label="友谊赛" value="friendly"></el-option>
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

    <!-- 赛事列表 -->
    <div class="event-list-container">
      <div v-if="loading" class="loading-container">
        <el-icon class="loading-icon" :size="32">
          <Loading />
        </el-icon>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="events.length === 0" class="empty-state">
        <el-empty description="暂无赛事数据"></el-empty>
      </div>

      <div v-else class="event-grid">
        <div 
          v-for="event in events" 
          :key="event.id" 
          class="event-card"
          @click="handleView(event)"
        >
          <div class="card-image">
            <img :src="event.image || '/static/default-event.png'" :alt="event.name" />
            <div class="status-badge" :class="getStatusBadgeClass(event.status)">
              {{ getStatusText(event.status) }}
            </div>
          </div>
          
          <div class="card-content">
            <h3 class="event-title">{{ event.name }}</h3>
            <div class="event-meta">
              <div class="meta-item">
                <el-icon><Calendar /></el-icon>
                <span>{{ formatDate(event.event_date) }}</span>
              </div>
              <div class="meta-item">
                <el-icon><Clock /></el-icon>
                <span>报名截止: {{ formatDate(event.registration_deadline) }}</span>
              </div>
              <div class="meta-item">
                <el-icon><Location /></el-icon>
                <span>{{ event.location }}</span>
              </div>
            </div>
            
            <div class="event-info">
              <div class="info-item">
                <span class="label">类型：</span>
                <span>{{ getEventTypeText(event.event_type) }}</span>
              </div>
              <div class="info-item">
                <span class="label">参赛：</span>
                <span>{{ event.current_participants }}/{{ event.max_participants }}</span>
              </div>
              <div class="info-item" v-if="event.registration_fee && event.registration_fee !== '0'">
                <span class="label">费用：</span>
                <span>¥{{ event.registration_fee }}</span>
              </div>
            </div>

            <div class="card-actions">
              <el-button size="small" @click.stop="handleEdit(event)">编辑</el-button>
              <el-button size="small" type="danger" @click.stop="handleDelete(event)">删除</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="pagination.total > 0">
      <el-pagination
        :current-page="pagination.current_page"
        :page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      ></el-pagination>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog 
      :title="dialogMode === 'add' ? '发布赛事' : '编辑赛事'" 
      v-model="dialogVisible"
      width="700px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="赛事名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入赛事名称"></el-input>
        </el-form-item>
        
        <el-form-item label="赛事描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入赛事描述"></el-input>
        </el-form-item>
        
        <el-form-item label="赛事类型" prop="event_type">
          <el-select v-model="form.event_type" placeholder="请选择赛事类型" style="width: 100%">
            <el-option label="训练营" value="training"></el-option>
            <el-option label="比赛" value="competition"></el-option>
            <el-option label="锦标赛" value="championship"></el-option>
            <el-option label="联赛" value="league"></el-option>
            <el-option label="友谊赛" value="friendly"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>
        
        <!-- 赛事图片字段 -->
        <el-form-item label="赛事图片" prop="image">
          <div class="image-upload-container">
            <div class="upload-section">
              <el-input 
                v-model="form.image" 
                placeholder="请输入图片URL或上传图片" 
                style="margin-bottom: 10px"
              ></el-input>
              <el-upload
                class="upload-demo"
                :action="baseURL + '/api/upload'"
                :show-file-list="false"
                :before-upload="beforeUpload"
                :on-success="handleUploadSuccess"
                :on-error="handleUploadError"
                accept=".jpg,.jpeg,.png,.gif,.webp"
              >
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
                <img :src="form.image" alt="赛事图片预览" class="preview-image" />
                <div class="preview-actions">
                  <el-button 
                    type="danger" 
                    size="small" 
                    @click="clearImage"
                    :icon="Delete"
                  >
                    清除
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </el-form-item>
        
        <el-form-item label="赛事日期" prop="event_date">
          <el-date-picker 
            v-model="form.event_date" 
            type="date" 
            placeholder="选择赛事日期" 
            format="YYYY-MM-DD" 
            value-format="YYYY-MM-DD"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        
        <el-form-item label="报名截止" prop="registration_deadline">
          <el-date-picker 
            v-model="form.registration_deadline" 
            type="date" 
            placeholder="选择报名截止日期" 
            format="YYYY-MM-DD" 
            value-format="YYYY-MM-DD"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        
        <el-form-item label="赛事地点" prop="location">
          <el-input v-model="form.location" placeholder="请输入赛事地点"></el-input>
        </el-form-item>
        
        <el-form-item label="最大参赛人数" prop="max_participants">
          <el-input-number v-model="form.max_participants" :min="1" placeholder="最大参赛人数"></el-input-number>
        </el-form-item>
        
        <el-form-item label="报名费用" prop="registration_fee">
          <el-input-number 
            v-model="form.registration_fee" 
            :min="0" 
            :precision="2" 
            placeholder="报名费用（元）"
          ></el-input-number>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="未开始" value="upcoming"></el-option>
            <el-option label="进行中" value="ongoing"></el-option>
            <el-option label="已结束" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看赛事详情对话框 -->
    <el-dialog title="赛事详情" v-model="viewDialogVisible" width="700px">
      <div v-if="currentEvent" class="event-detail">
        <div class="detail-header">
          <img :src="currentEvent.image || '/static/default-event.png'" :alt="currentEvent.name" class="detail-image" />
          <div class="detail-title">
            <h2>{{ currentEvent.name }}</h2>
            <div class="detail-status">
              <el-tag :type="getStatusTagType(currentEvent.status)">
                {{ getStatusText(currentEvent.status) }}
              </el-tag>
              <el-tag>{{ getEventTypeText(currentEvent.event_type) }}</el-tag>
            </div>
          </div>
        </div>
        
        <el-descriptions :column="2" border class="detail-descriptions">
          <el-descriptions-item label="赛事ID">{{ currentEvent.id }}</el-descriptions-item>
          <el-descriptions-item label="赛事日期">{{ formatDate(currentEvent.event_date) }}</el-descriptions-item>
          <el-descriptions-item label="报名截止">{{ formatDate(currentEvent.registration_deadline) }}</el-descriptions-item>
          <el-descriptions-item label="赛事地点">{{ currentEvent.location }}</el-descriptions-item>
          <el-descriptions-item label="最大参赛人数">{{ currentEvent.max_participants }}人</el-descriptions-item>
          <el-descriptions-item label="当前参赛人数">
            <span :class="{ 'full-capacity': currentEvent.current_participants >= currentEvent.max_participants }">
              {{ currentEvent.current_participants }}人
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="报名费用">
            {{ currentEvent.registration_fee && currentEvent.registration_fee !== '0' ? '¥' + currentEvent.registration_fee : '免费' }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDateTime(currentEvent.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="赛事描述" :span="2">
            <div class="description-content">{{ currentEvent.description || '暂无描述' }}</div>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      
      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleEdit(currentEvent)">编辑</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Calendar, 
  Clock, 
  Location,
  Loading,
  Delete
} from '@element-plus/icons-vue'


import { baseURL } from '@/utils/request'

// 导入赛事API
import { 
  getEventsList, 
  getEventDetail, 
  createEvent, 
  updateEvent, 
  deleteEvent 
} from '@/api/events'

export default {
  name: 'EventList',
  setup() {
    // 响应式数据
    const loading = ref(false)
    const submitLoading = ref(false)
    const dialogVisible = ref(false)
    const viewDialogVisible = ref(false)
    const dialogMode = ref('add')
    const currentEvent = ref(null)
    const formRef = ref(null)

    // 赛事数据
    const events = ref([])
    const pagination = reactive({
      current_page: 1,
      page_size: 20,
      total: 0,
      total_pages: 0
    })

    // 搜索表单
    const searchForm = reactive({
      name: '',
      event_type: '',
      status: ''
    })

    // 表单数据
    const form = reactive({
      id: null,
      name: '',
      description: '',
      event_type: '',
      image: '',
      event_date: '',
      registration_deadline: '',
      location: '',
      max_participants: 100,
      registration_fee: 0,
      status: 'upcoming'
    })

    // 表单验证规则
    const rules = {
      name: [
        { required: true, message: '请输入赛事名称', trigger: 'blur' },
        { min: 2, max: 100, message: '赛事名称长度在 2 到 100 个字符', trigger: 'blur' }
      ],
      event_type: [
        { required: true, message: '请选择赛事类型', trigger: 'change' }
      ],
      event_date: [
        { required: true, message: '请选择赛事日期', trigger: 'change' }
      ],
      registration_deadline: [
        { required: true, message: '请选择报名截止日期', trigger: 'change' }
      ],
      location: [
        { required: true, message: '请输入赛事地点', trigger: 'blur' }
      ],
      max_participants: [
        { required: true, message: '请输入最大参赛人数', trigger: 'blur' },
        { type: 'number', min: 1, message: '最大参赛人数至少为1', trigger: 'blur' }
      ]
    }

    // 方法定义
    const getEventTypeText = (type) => {
      const typeMap = {
        'training': '训练营',
        'competition': '比赛',
        'championship': '锦标赛',
        'league': '联赛',
        'friendly': '友谊赛',
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

    const getStatusBadgeClass = (status) => {
      const classMap = {
        'upcoming': 'status-upcoming',
        'ongoing': 'status-ongoing',
        'completed': 'status-completed',
        'cancelled': 'status-cancelled'
      }
      return classMap[status] || 'status-upcoming'
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

    // 获取赛事列表
    const fetchEvents = async () => {
      try {
        loading.value = true
        
        const params = {
          page: pagination.current_page,
          page_size: pagination.page_size
        }
        
        // 添加搜索参数
        if (searchForm.name.trim()) {
          params.name = searchForm.name.trim()
        }
        if (searchForm.event_type) {
          params.event_type = searchForm.event_type
        }
        if (searchForm.status) {
          params.status = searchForm.status
        }

        console.log('请求参数:', params)
        
        const response = await getEventsList(params)
        
        if (response.code === 0) {
          events.value = response.data.events || []
          pagination.total = response.data.pagination?.total || 0
          pagination.total_pages = response.data.pagination?.total_pages || 0
        } else {
          ElMessage.error(response.message || '获取赛事列表失败')
        }
      } catch (error) {
        console.error('获取赛事列表失败:', error)
        ElMessage.error('网络错误，请稍后重试')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current_page = 1
      fetchEvents()
    }

    // 重置搜索
    const resetSearch = () => {
      searchForm.name = ''
      searchForm.event_type = ''
      searchForm.status = ''
      pagination.current_page = 1
      fetchEvents()
    }

    // 分页处理
    const handleSizeChange = (size) => {
      pagination.page_size = size
      pagination.current_page = 1
      fetchEvents()
    }

    const handleCurrentChange = (page) => {
      pagination.current_page = page
      fetchEvents()
    }

    // 新增赛事
    const handleAdd = () => {
      dialogMode.value = 'add'
      resetForm()
      dialogVisible.value = true
    }

    // 查看赛事
    const handleView = (event) => {
      currentEvent.value = { ...event }
      viewDialogVisible.value = true
    }

    // 编辑赛事
    const handleEdit = (event) => {
      dialogMode.value = 'edit'
      Object.assign(form, {
        id: event.id,
        name: event.name,
        description: event.description || '',
        event_type: event.event_type,
        image: event.image || '',
        event_date: event.event_date,
        registration_deadline: event.registration_deadline,
        location: event.location,
        max_participants: event.max_participants,
        registration_fee: parseFloat(event.registration_fee) || 0,
        status: event.status
      })
      dialogVisible.value = true
      viewDialogVisible.value = false
    }

    // 删除赛事
    const handleDelete = async (event) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除赛事 "${event.name}" 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定删除',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const response = await deleteEvent(event.id)
        
        if (response.code === 0) {
          ElMessage.success('删除成功')
          fetchEvents()
        } else {
          ElMessage.error(response.message || '删除失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除赛事失败:', error)
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
          name: form.name,
          description: form.description,
          event_type: form.event_type,
          image: form.image,
          event_date: form.event_date,
          registration_deadline: form.registration_deadline,
          location: form.location,
          max_participants: form.max_participants,
          registration_fee: form.registration_fee,
          status: form.status
        }
        
        let response
        
        if (dialogMode.value === 'add') {
          response = await createEvent(submitData)
        } else {
          response = await updateEvent(form.id, submitData)
        }
        
        if (response.code === 0) {
          ElMessage.success(dialogMode.value === 'add' ? '创建成功' : '更新成功')
          dialogVisible.value = false
          fetchEvents()
        } else {
          ElMessage.error(response.message || (dialogMode.value === 'add' ? '创建失败' : '更新失败'))
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
        name: '',
        description: '',
        event_type: '',
        image: '',
        event_date: '',
        registration_deadline: '',
        location: '',
        max_participants: 100,
        registration_fee: 0,
        status: 'upcoming'
      })
    }

    // 页面加载时获取数据
    onMounted(() => {
      fetchEvents()
    })

    return {
      loading,
      submitLoading,
      dialogVisible,
      viewDialogVisible,
      dialogMode,
      currentEvent,
      formRef,
      events,
      pagination,
      searchForm,
      form,
      rules,
      getEventTypeText,
      getStatusText,
      getStatusTagType,
      getStatusBadgeClass,
      formatDate,
      formatDateTime,
      beforeUpload,
      handleUploadSuccess,
      handleUploadError,
      clearImage,
      fetchEvents,
      handleSearch,
      resetSearch,
      handleSizeChange,
      handleCurrentChange,
      handleAdd,
      handleView,
      handleEdit,
      handleDelete,
      handleSubmit,
      resetForm,
      baseURL

    }
  }
}
</script>

<style scoped>
.event-list {
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
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.event-list-container {
  margin-bottom: 20px;
}

.loading-container,
.empty-state {
  padding: 60px 20px;
  text-align: center;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.event-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.event-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.event-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
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

.status-upcoming { background: #409eff; }
.status-ongoing { background: #67c23a; }
.status-completed { background: #909399; }
.status-cancelled { background: #f56c6c; }

.card-content {
  padding: 20px;
}

.event-title {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  line-height: 1.4;
}

.event-meta {
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

.event-info {
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

.pagination {
  display: flex;
  justify-content: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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

.event-detail {
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
  .event-grid {
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
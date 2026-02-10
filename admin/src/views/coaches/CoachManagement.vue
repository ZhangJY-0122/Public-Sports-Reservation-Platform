<template>
  <div class="coach-management">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <div class="header-left">
        <h2>教练管理</h2>
        <div class="stats">
          <el-tag type="primary">总数: {{ stats.total_coaches }}</el-tag>
          <el-tag type="success">启用: {{ stats.active_coaches }}</el-tag>
          <el-tag type="info">禁用: {{ stats.inactive_coaches }}</el-tag>
        </div>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="openCreateDialog">
          <el-icon><Plus /></el-icon>
          新增教练
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-input
            v-model="searchForm.search"
            placeholder="搜索教练姓名、专业领域"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-input
            v-model="searchForm.specialization"
            placeholder="专业筛选"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.is_active" placeholder="状态" clearable>
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.sort_field" placeholder="排序字段">
            <el-option label="评分" value="rating" />
            <el-option label="授课次数" value="total_sessions" />
            <el-option label="从业年限" value="experience_years" />
            <el-option label="创建时间" value="created_at" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.sort_order" placeholder="排序方向">
            <el-option label="降序" value="desc" />
            <el-option label="升序" value="asc" />
          </el-select>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 数据表格 -->
    <div class="table-section">
      <el-table
        :data="coachList"
        v-loading="loading"
        style="width: 100%"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="id" label="ID" width="80" sortable="custom" />
        <el-table-column label="教练信息" min-width="200">
          <template #default="{ row }">
            <div class="coach-info">
              <div class="coach-avatar" v-if="row.avatar">
                <img :src="row.avatar" :alt="row.name" />
              </div>
              <div class="coach-avatar placeholder" v-else>
                <el-icon><UserFilled /></el-icon>
              </div>
              <div class="coach-details">
                <div class="coach-name">{{ row.name }}</div>
                <div class="coach-specialization">{{ row.specialization }}</div>
                <div class="coach-experience">
                  从业{{ row.experience_years }}年
                </div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="hourly_rate" label="价格(元/小时)" width="120">
          <template #default="{ row }">
            <span class="price">¥{{ row.hourly_rate }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="rating" label="评分" width="80">
          <template #default="{ row }">
            <el-rate v-model="row.rating" disabled show-score />
          </template>
        </el-table-column>
        <el-table-column prop="total_sessions" label="授课次数" width="100" />
        <el-table-column prop="phone" label="联系电话" width="120" />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" sortable="custom">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openEditDialog(row)">
              编辑
            </el-button>
            <el-button 
              :type="row.is_active ? 'warning' : 'success'" 
              size="small" 
              @click="toggleStatus(row)"
            >
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
            <el-popconfirm
              title="确认删除该教练？"
              @confirm="handleDelete(row)"
              confirm-button-text="确认"
              cancel-button-text="取消"
            >
              <template #reference>
                <el-button type="danger" size="small">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页 -->
    <div class="pagination-section">
      <el-pagination
        v-model:current-page="pagination.current_page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? '新增教练' : '编辑教练'"
      width="800px"
      :before-close="handleDialogClose"
    >
      <el-form
        ref="coachFormRef"
        :model="coachForm"
        :rules="coachRules"
        label-width="120px"
        class="coach-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="教练姓名" prop="name">
              <el-input v-model="coachForm.name" placeholder="请输入教练姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="专业领域" prop="specialization">
              <el-input v-model="coachForm.specialization" placeholder="请输入专业领域" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="从业年限" prop="experience_years">
              <el-input-number 
                v-model="coachForm.experience_years" 
                :min="0" 
                :max="50"
                placeholder="请输入从业年限"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="每小时费用" prop="hourly_rate">
              <el-input-number 
                v-model="coachForm.hourly_rate" 
                :min="0" 
                :precision="2"
                placeholder="请输入每小时费用"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="coachForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="当前状态" prop="is_active">
              <el-switch 
                v-model="coachForm.is_active"
                active-text="启用"
                inactive-text="禁用"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="教练头像" prop="avatar">
          <div class="avatar-upload">
            <div class="avatar-preview" v-if="coachForm.avatar || avatarPreview">
              <img :src="avatarPreview || coachForm.avatar" alt="头像预览" />
            </div>
            <div class="avatar-placeholder" v-else>
              <el-icon><UserFilled /></el-icon>
              <span>头像预览</span>
            </div>
            <div class="upload-controls">
              <el-upload
                ref="uploadRef"
                :show-file-list="false"
                :before-upload="beforeAvatarUpload"
                :http-request="handleAvatarUpload"
                accept="image/png,image/jpeg,image/jpg"
              >
                <el-button type="primary" size="small">
                  <el-icon><Upload /></el-icon>
                  {{ coachForm.avatar ? '更换头像' : '上传头像' }}
                </el-button>
              </el-upload>
              <el-button 
                v-if="coachForm.avatar || avatarPreview"
                type="danger" 
                size="small" 
                @click="removeAvatar"
              >
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </div>
          </div>
        </el-form-item>

        <el-form-item label="教练介绍" prop="introduction">
          <el-input
            v-model="coachForm.introduction"
            type="textarea"
            :rows="4"
            placeholder="请输入教练详细介绍"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleDialogClose">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ dialogMode === 'create' ? '创建' : '更新' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Plus, 
  Search, 
  UserFilled, 
  Upload, 
  Delete,
  Edit,
  Switch
} from '@element-plus/icons-vue'
import { 
  getCoachesList, 
  createCoach, 
  updateCoach, 
  deleteCoach, 
  uploadImage
} from '@/api/coach'

import { formatDate } from '@/utils/formatDate'
import  request from '@/utils/request'

// 数据响应式引用
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref('create') // 'create' | 'edit'
const coachFormRef = ref()
const uploadRef = ref()

// 数据列表
const coachList = ref([])

// 分页信息
const pagination = reactive({
  current_page: 1,
  page_size: 20,
  total: 0,
  total_pages: 0
})

// 搜索表单
const searchForm = reactive({
  search: '',
  specialization: '',
  is_active: '',
  sort_field: 'rating',
  sort_order: 'desc'
})

// 表单数据
const coachForm = reactive({

  name: '',
  specialization: '',
  experience_years: 0,
  hourly_rate: 0,
  introduction: '',
  avatar: '',
  phone: '',
  is_active: true
})

// 头像预览
const avatarPreview = ref('')

// 统计数据
const stats = reactive({
  total_coaches: 0,
  active_coaches: 0,
  inactive_coaches: 0
})

// 表单验证规则
const coachRules = {
  name: [
    { required: true, message: '请输入教练姓名', trigger: 'blur' },
    { min: 2, max: 50, message: '姓名长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  specialization: [
    { required: true, message: '请输入专业领域', trigger: 'blur' }
  ],
  experience_years: [
    { required: true, message: '请输入从业年限', trigger: 'blur' }
  ],
  hourly_rate: [
    { required: true, message: '请输入每小时费用', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

// 初始化
onMounted(() => {
  fetchCoachesList()
})

// 获取教练列表
const fetchCoachesList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current_page,
      page_size: pagination.page_size,
      ...searchForm
    }
    
    // 清理空值参数
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key]
      }
    })
    
    const response = await getCoachesList(params)
    
    if (response.code === 0) {
      coachList.value = response.data.coaches
      pagination.total = response.data.pagination.total
      pagination.total_pages = response.data.pagination.total_pages
      
      // 更新统计数据
      stats.total_coaches = response.data.pagination.total
      stats.active_coaches = coachList.value.filter(coach => coach.is_active).length
      stats.inactive_coaches = stats.total_coaches - stats.active_coaches
    } else {
      ElMessage.error(response.message || '获取教练列表失败')
    }
  } catch (error) {
    ElMessage.error('获取教练列表失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current_page = 1
  fetchCoachesList()
}

// 排序
const handleSortChange = ({ prop, order }) => {
  searchForm.sort_field = prop
  searchForm.sort_order = order === 'ascending' ? 'asc' : 'desc'
  fetchCoachesList()
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.current_page = 1
  fetchCoachesList()
}

// 页码变化
const handleCurrentChange = (page) => {
  pagination.current_page = page
  fetchCoachesList()
}

// 打开新增对话框
const openCreateDialog = () => {
  dialogMode.value = 'create'
  resetForm()
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (coach) => {
  dialogMode.value = 'edit'
  Object.assign(coachForm, {
    id: coach.id,
    name: coach.name,
    specialization: coach.specialization,
    experience_years: coach.experience_years,
    hourly_rate: parseFloat(coach.hourly_rate),
    introduction: coach.introduction || '',
    avatar: coach.avatar || '',
    phone: coach.phone || '',
    is_active: coach.is_active
  })
  avatarPreview.value = coach.avatar || ''
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  Object.assign(coachForm, {
    name: '',
    specialization: '',
    experience_years: 0,
    hourly_rate: 0,
    introduction: '',
    avatar: '',
    phone: '',
    is_active: true
  })
  avatarPreview.value = ''
  coachFormRef.value?.clearValidate()
}

// 关闭对话框
const handleDialogClose = () => {
  dialogVisible.value = false
  resetForm()
}

// 图片上传前验证
const beforeAvatarUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB!')
    return false
  }
  return true
}

// 处理头像上传
const handleAvatarUpload = async (options) => {
  const { file } = options
  
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await uploadImage(formData)
    
    if (response.code === 0) {
      coachForm.avatar = response.data.url
      avatarPreview.value = response.data.url
      
      ElMessage.success('头像上传成功')
    } else {
      ElMessage.error(response.message || '头像上传失败')
    }
  } catch (error) {
    ElMessage.error('头像上传失败: ' + error.message)
  }
}

// 删除头像
const removeAvatar = () => {
  coachForm.avatar = ''
  avatarPreview.value = ''
}

// 切换状态
const toggleStatus = async (coach) => {
  try {
    const action = coach.is_active ? '禁用' : '启用'
    await ElMessageBox.confirm(`确认${action}该教练？`, '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await updateCoach(coach.id, { is_active: !coach.is_active })
    
    if (response.code === 0) {
      coach.is_active = !coach.is_active
      ElMessage.success(`${action}成功`)
      
      // 更新统计数据
      if (coach.is_active) {
        stats.active_coaches++
        stats.inactive_coaches--
      } else {
        stats.active_coaches--
        stats.inactive_coaches++
      }
    } else {
      ElMessage.error(response.message || `${action}失败`)
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败: ' + error.message)
    }
  }
}

// 删除
const handleDelete = async (coach) => {
  try {
    const response = await deleteCoach(coach.id)
    
    if (response.code === 0) {
      ElMessage.success('删除成功')
      fetchCoachesList()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    ElMessage.error('删除失败: ' + error.message)
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    await coachFormRef.value.validate()
    submitting.value = true
    
    const response = dialogMode.value === 'create' 
      ? await createCoach(coachForm)
      : await updateCoach(coachForm.id, coachForm)
    
    ElMessage.success(dialogMode.value === 'create' ? '创建成功' : '更新成功')
    dialogVisible.value = false
    fetchCoachesList()
  } catch (error) {
    ElMessage.error('操作失败: ' + error.message)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.coach-management {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-left h2 {
  margin: 0;
  color: #303133;
}

.stats {
  display: flex;
  gap: 10px;
}

.search-section {
  background: #fff;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.table-section {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 16px;
}

.pagination-section {
  display: flex;
  justify-content: flex-end;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 教练信息样式 */
.coach-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.coach-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background: #f5f7fa;
}

.coach-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.coach-avatar.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 20px;
}

.coach-details {
  flex: 1;
  min-width: 0;
}

.coach-name {
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.coach-specialization {
  color: #606266;
  font-size: 14px;
  margin-bottom: 2px;
}

.coach-experience {
  color: #909399;
  font-size: 12px;
}

/* 价格样式 */
.price {
  font-weight: 600;
  color: #e6a23c;
}

/* 头像上传样式 */
.avatar-upload {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.avatar-preview {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #dcdfe6;
}

.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 2px dashed #dcdfe6;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  background: #f5f7fa;
}

.avatar-placeholder .el-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.upload-controls {
  display: flex;
  gap: 12px;
}

.dialog-footer {
  text-align: right;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-left {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .search-section .el-row {
    gap: 8px;
  }
  
  .coach-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .avatar-upload {
    align-items: center;
  }
  
  .upload-controls {
    flex-direction: column;
    width: 100%;
  }
}
</style>
<template>
  <div class="venue-management">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <div class="header-left">
        <h2>场馆管理22</h2>
        <div class="stats">
          <el-tag type="primary">总数: {{ stats.total_venues }}</el-tag>
          <el-tag type="success">启用: {{ stats.active_venues }}</el-tag>
          <el-tag type="info">禁用: {{ stats.inactive_venues }}</el-tag>
        </div>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="openCreateDialog">
          <el-icon><Plus /></el-icon>
          新增场馆
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-input
            v-model="searchForm.search"
            placeholder="搜索场馆名称、地址、类型"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.category_id" placeholder="选择分类" clearable>
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.is_active" placeholder="状态" clearable>
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.sort_field" placeholder="排序字段">
            <el-option label="ID" value="id" />
            <el-option label="名称" value="name" />
            <el-option label="创建时间" value="created_at" />
            <el-option label="价格" value="price" />
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
        :data="venueList"
        v-loading="loading"
        style="width: 100%"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="id" label="ID" width="80" sortable="custom" />
        <el-table-column label="场馆信息" min-width="200">
          <template #default="{ row }">
            <div class="venue-info">
              <div class="venue-image" v-if="row.image">
                <img :src="row.image" :alt="row.name" />
              </div>
              <div class="venue-details">
                <div class="venue-name">{{ row.name }}</div>
                <div class="venue-type">{{ row.type }}</div>
                <div class="venue-location">
                  <el-icon><Location /></el-icon>
                  {{ row.location }}
                </div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="category.name" label="分类" width="120" />
        <el-table-column prop="price" label="价格(元/小时)" width="120">
          <template #default="{ row }">
            <span class="price">¥{{ row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="capacity" label="容量" width="80" />
        <el-table-column prop="contact_phone" label="联系电话" width="120" />
        <el-table-column prop="business_hours" label="营业时间" width="120" />
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
              title="确认删除该场馆？"
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
        v-model:page-size="pagination.per_page"
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
      :title="dialogMode === 'create' ? '新增场馆' : '编辑场馆'"
      width="800px"
      :before-close="handleDialogClose"
    >
      <el-form
        ref="venueFormRef"
        :model="venueForm"
        :rules="venueRules"
        label-width="120px"
        class="venue-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="场馆名称" prop="name">
              <el-input v-model="venueForm.name" placeholder="请输入场馆名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="场馆类型" prop="type">
              <el-input v-model="venueForm.type" placeholder="请输入场馆类型" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="场馆分类" prop="category_id">
              <el-select v-model="venueForm.category_id" placeholder="选择分类" style="width: 100%">
                <el-option
                  v-for="category in categories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="价格(元/小时)" prop="price_per_hour">
              <el-input-number
                v-model="venueForm.price_per_hour"
                :min="0"
                :precision="2"
                :step="10"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="场馆地址" prop="location">
          <el-input v-model="venueForm.location" placeholder="请输入场馆地址" />
        </el-form-item>

        <el-form-item label="场馆描述" prop="description">
          <el-input
            v-model="venueForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入场馆描述"
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="容量/人数" prop="capacity">
              <el-input-number
                v-model="venueForm.capacity"
                :min="1"
                :max="1000"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="contact_phone">
              <el-input v-model="venueForm.contact_phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="营业时间" prop="business_hours">
              <el-input v-model="venueForm.business_hours" placeholder="如：08:00-22:00" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="is_active">
              <el-switch
                v-model="venueForm.is_active"
                active-text="启用"
                inactive-text="禁用"
              />
            </el-form-item>
          </el-col>
        </el-row>

      <!-- 替换原来的 “场馆图片” el-form-item -->
<el-form-item label="场馆图片" prop="image">
  <!-- 上传按钮 -->
  <el-upload
    :action="baseURL + '/api/upload'"        
    :on-success="handleUploadSuccess"
    :before-upload="beforeUpload"
  >
    <el-button type="primary" plain>
      <el-icon><Picture /></el-icon>
      上传图片
    </el-button>
  </el-upload>

  <!-- 图片预览 -->
  <div v-if="venueForm.image" class="img-preview">
    <img :src="venueForm.image" alt="场馆图片" />
  </div>

  <!-- 原来的输入框，简单隐藏即可（也可保留显示） -->
  <el-input
    v-model="venueForm.image"
    style="display:none"
  />
</el-form-item>

        <el-form-item label="设施描述" prop="facilities">
          <el-input
            v-model="venueForm.facilities"
            type="textarea"
            :rows="2"
            placeholder="请输入设施描述"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
            {{ dialogMode === 'create' ? '创建' : '更新' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Location } from '@element-plus/icons-vue'
import  request,{baseURL} from '@/utils/request.js'
import { Picture } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref('create') // 'create' | 'edit'
const venueFormRef = ref()

const venueList = ref([])
const categories = ref([])

const stats = reactive({
  total_venues: 0,
  active_venues: 0,
  inactive_venues: 0,
  category_stats: []
})

const pagination = reactive({
  current_page: 1,
  per_page: 10,
  total: 0,
  total_pages: 0,
  has_next: false,
  has_prev: false
})

const searchForm = reactive({
  search: '',
  category_id: null,
  is_active: null,
  sort_field: 'id',
  sort_order: 'desc'
})

const venueForm = reactive({
  id: null,
  name: '',
  type: '',
  location: '',
  description: '',
  image: '',
  price_per_hour: 0,
  capacity: 1,
  facilities: '',
  contact_phone: '',
  business_hours: '',
  category_id: null,
  is_active: true
})

// 表单验证规则
const venueRules = {
  name: [
    { required: true, message: '请输入场馆名称', trigger: 'blur' },
    { min: 2, max: 100, message: '场馆名称长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请输入场馆类型', trigger: 'blur' },
    { min: 2, max: 50, message: '场馆类型长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  location: [
    { required: true, message: '请输入场馆地址', trigger: 'blur' },
    { min: 5, max: 200, message: '场馆地址长度在 5 到 200 个字符', trigger: 'blur' }
  ],
  category_id: [
    { required: true, message: '请选择场馆分类', trigger: 'change' }
  ],
  price_per_hour: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { type: 'number', min: 0, message: '价格必须大于等于0', trigger: 'blur' }
  ],
  capacity: [
    { required: true, message: '请输入容量', trigger: 'blur' },
    { type: 'number', min: 1, message: '容量必须大于等于1', trigger: 'blur' }
  ]
}

// 方法
const fetchVenueList = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.current_page,
      limit: pagination.per_page,
      ...searchForm
    }
    
    // 移除空值参数
    Object.keys(params).forEach(key => {
      if (params[key] === null || params[key] === '') {
        delete params[key]
      }
    })

    const response = await request.get('/api/venue/list', params)
    venueList.value = response.data.venues
    Object.assign(pagination, response.data.pagination)
  } catch (error) {
    console.error('获取场馆列表失败:', error)
    ElMessage.error('获取场馆列表失败')
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await request.get('/api/venue/categories')
    categories.value = response.data
  } catch (error) {
    console.error('获取分类失败:', error)
    ElMessage.error('获取分类失败')
  }
}

const fetchStats = async () => {
  try {
    const response = await request.get('/api/venues/stats')
    Object.assign(stats, response.data)
  } catch (error) {
    console.error('获取统计信息失败:', error)
  }
}

const handleSearch = () => {
  pagination.current_page = 1
  fetchVenueList()
}

const handleSortChange = ({ prop, order }) => {
  searchForm.sort_field = prop
  searchForm.sort_order = order === 'ascending' ? 'asc' : 'desc'
  fetchVenueList()
}

const handleSizeChange = (size) => {
  pagination.per_page = size
  pagination.current_page = 1
  fetchVenueList()
}

const handleCurrentChange = (page) => {
  pagination.current_page = page
  fetchVenueList()
}

const openCreateDialog = () => {
  dialogMode.value = 'create'
  dialogVisible.value = true
  nextTick(() => {
    resetForm()
  })
}

const openEditDialog = (row) => {
  dialogMode.value = 'edit'
  dialogVisible.value = true
  nextTick(() => {
    Object.assign(venueForm, {
      id: row.id,
      name: row.name,
      type: row.type,
      location: row.location,
      description: row.description || '',
      image: row.image || '',
      price_per_hour: parseFloat(row.price),
      capacity: row.capacity,
      facilities: row.facilities || '',
      contact_phone: row.contact_phone || '',
      business_hours: row.business_hours || '',
      category_id: row.category?.id,
      is_active: row.is_active
    })
  })
}

const handleDialogClose = () => {
  resetForm()
  dialogVisible.value = false
}

const resetForm = () => {
  if (venueFormRef.value) {
    venueFormRef.value.resetFields()
  }
  Object.assign(venueForm, {
    id: null,
    name: '',
    type: '',
    location: '',
    description: '',
    image: '',
    price_per_hour: 0,
    capacity: 1,
    facilities: '',
    contact_phone: '',
    business_hours: '',
    category_id: null,
    is_active: true
  })
}

const handleSubmit = async () => {
  if (!venueFormRef.value) return
  
  try {
    await venueFormRef.value.validate()
    submitLoading.value = true
    
    if (dialogMode.value === 'create') {
      await request.post('/api/venues', venueForm)
      ElMessage.success('创建成功')
    } else {
      await request.put(`/api/venues/${venueForm.id}`, venueForm)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    resetForm()
    fetchVenueList()
    fetchStats()
  } catch (error) {
    if (error.message) {
      ElMessage.error(error.message)
    }
  } finally {
    submitLoading.value = false
  }
}

const handleDelete = async (row) => {
  try {
    await request.delete(`/api/venues/${row.id}`)
    ElMessage.success('删除成功')
    fetchVenueList()
    fetchStats()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const toggleStatus = async (row) => {
  try {
    await request.patch(`/api/venues/toggle-status/${row.id}`)
    ElMessage.success('状态切换成功')
    fetchVenueList()
    fetchStats()
  } catch (error) {
    ElMessage.error('状态切换失败')
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 生命周期
onMounted(() => {
  fetchVenueList()
  fetchCategories()
  fetchStats()
})


/* 上传前检查：大小 / 类型 自己再补 */
const beforeUpload = (rawFile) => {
  const isImg = rawFile.type.startsWith('image/')
  if (!isImg) {
    ElMessage.error('只能上传图片')
    return false
  }
  return true
}

/* 上传成功：后端返回 { path: 'http://xxx/yyy.jpg' } */
const handleUploadSuccess = (res) => {
  // 后端返回格式：{ path: 'xxx' }
console.log('上传成功:', res.data.url)

  venueForm.image = res.data.url
  ElMessage.success('图片上传成功')
}
</script>

<style scoped>
.venue-management {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left h2 {
  margin: 0 0 10px 0;
  color: #303133;
}

.stats {
  display: flex;
  gap: 10px;
}

.search-section {
  margin-bottom: 20px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 4px;
}

.table-section {
  margin-bottom: 20px;
}

.pagination-section {
  display: flex;
  justify-content: center;
}

.venue-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.venue-image {
  width: 50px;
  height: 50px;
  border-radius: 4px;
  overflow: hidden;
  flex-shrink: 0;
}

.venue-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.venue-details {
  flex: 1;
  min-width: 0;
}

.venue-name {
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.venue-type {
  color: #606266;
  font-size: 14px;
  margin-bottom: 2px;
}

.venue-location {
  color: #909399;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.price {
  font-weight: bold;
  color: #e6a23c;
}

.venue-form {
  margin-top: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 简单预览样式，放在 <style scoped> 里即可 */
.img-preview {
  margin-top: 8px;
  width: 120px;
  height: 120px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}
.img-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
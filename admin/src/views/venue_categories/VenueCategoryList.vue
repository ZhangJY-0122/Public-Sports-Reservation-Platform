<template>
  <div class="venue-category-list">
    <div class="page-header">
      <h2>场馆分类管理</h2>
    </div>

    <!-- 操作工具栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">新增分类</el-button>
      <el-button type="danger" @click="handleBatchDelete" :disabled="selectedItems.length === 0">批量删除</el-button>
      
      <!-- 搜索表单 -->
      <el-form :model="searchForm" class="search-form" inline>
        <el-form-item label="分类名称">
          <el-input v-model="searchForm.name" placeholder="请输入分类名称"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 数据表格 -->
    <el-table 
      :data="tableData" 
      style="width: 100%"
      @selection-change="handleSelectionChange"
      empty-text="暂无数据"
    >
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="name" label="分类名称" width="150"></el-table-column>
      <el-table-column prop="description" label="描述" width="250" show-overflow-tooltip></el-table-column>
      <el-table-column prop="icon" label="图标" width="120" show-overflow-tooltip>
        <template #default="{ row }">
          <span v-if="row.icon">{{ row.icon }}</span>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="sort_order" label="排序" width="100"></el-table-column>
      <el-table-column label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button type="text" @click="handleView(row)">查看</el-button>
          <el-button type="text" @click="handleEdit(row)">编辑</el-button>
          <el-button type="text" @click="handleDelete(row)" style="color: #f56c6c">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 调试信息 -->
    <div class="debug-info" v-if="showDebug">
      <h4>调试信息：</h4>
      <p>数据数组长度: {{ tableData.length }}</p>
      <p>总记录数: {{ pagination.total }}</p>
      <p>加载状态: {{ loading ? '加载中...' : '已完成' }}</p>
      <p>分页参数: page={{ pagination.page }}, size={{ pagination.size }}</p>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog 
      :title="dialogMode === 'add' ? '新增场馆分类' : '编辑场馆分类'" 
      v-model="dialogVisible"
      width="500px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称"></el-input>
        </el-form-item>
        <el-form-item label="分类描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入分类描述"></el-input>
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-input v-model="form.icon" placeholder="请输入图标名称"></el-input>
        </el-form-item>
        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="form.is_active" :active-text="'启用'" :inactive-text="'禁用'"></el-switch>
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" placeholder="排序顺序"></el-input-number>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看对话框 -->
    <el-dialog title="分类详情" v-model="viewDialogVisible" width="500px">
      <div v-if="currentItem" class="view-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="分类名称">{{ currentItem.name }}</el-descriptions-item>
          <el-descriptions-item label="分类描述" :span="2">{{ currentItem.description || '-' }}</el-descriptions-item>
          <el-descriptions-item label="图标" :span="2">
            <span v-if="currentItem.icon">{{ currentItem.icon }}</span>
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="currentItem.is_active ? 'success' : 'danger'">
              {{ currentItem.is_active ? '启用' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="图标URL" :span="2">
            <el-link v-if="currentItem.icon_url" :href="currentItem.icon_url" target="_blank" type="primary">
              {{ currentItem.icon_url }}
            </el-link>
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="排序">{{ currentItem.sort_order }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(currentItem.created_at) }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { venueApi } from '@/api/venue'

// 数据响应式定义
const loading = ref(false)
const showDebug = ref(false)
const tableData = ref([])
const selectedItems = ref([])
const dialogVisible = ref(false)
const viewDialogVisible = ref(false)
const dialogMode = ref('add')
const currentItem = ref(null)
const formRef = ref(null)

// 搜索表单
const searchForm = reactive({
  name: ''
})

// 分页配置
const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

// 表单数据
const form = reactive({
  name: '',
  description: '',
  icon: '',
  sort_order: 0,
  is_active: true
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入分类名称', trigger: 'blur' },
    { min: 2, max: 50, message: '分类名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { max: 200, message: '描述长度不能超过200个字符', trigger: 'blur' }
  ],
  icon: [
    { max: 100, message: '图标名称不能超过100个字符', trigger: 'blur' }
  ],
  sort_order: [
    { type: 'number', min: 0, message: '排序值必须大于等于0', trigger: 'blur' }
  ],
  is_active: [
    { type: 'boolean', message: '状态值无效', trigger: 'change' }
  ]
}

// 模拟数据
const mockData = [
  {
    id: 1,
    name: '篮球',
    description: '篮球场馆和设施',
    icon_url: 'basketball.png',
    sort_order: 1,
    created_at: '2024-01-01 10:00:00'
  },
  {
    id: 2,
    name: '足球',
    description: '足球场地和设施',
    icon_url: 'football.png',
    sort_order: 2,
    created_at: '2024-01-01 10:00:00'
  },
  {
    id: 3,
    name: '羽毛球',
    description: '羽毛球场地和设施',
    icon_url: 'badminton.png',
    sort_order: 3,
    created_at: '2024-01-01 10:00:00'
  },
  {
    id: 4,
    name: '网球',
    description: '网球场和设施',
    icon_url: 'tennis.png',
    sort_order: 4,
    created_at: '2024-01-01 10:00:00'
  },
  {
    id: 5,
    name: '游泳',
    description: '游泳池和水上设施',
    icon_url: 'swimming.png',
    sort_order: 5,
    created_at: '2024-01-01 10:00:00'
  },
  {
    id: 6,
    name: '健身',
    description: '健身房和健身器材',
    icon_url: 'gym.png',
    sort_order: 6,
    created_at: '2024-01-01 10:00:00'
  }
]

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 调用真实API，使用正确的API方法名
    const response = await venueApi.getVenueCategories({
      name: searchForm.name.trim() || undefined
    })
    console.log('API响应数据:', response)
    
    // 提取数据数组
    const allCategories = response.data || []
    console.log('原始分类数据:', allCategories)
    
    // 前端分页处理
    let filteredCategories = allCategories
    
    // 如果有搜索关键词，在前端进行过滤
    if (searchForm.name.trim()) {
      filteredCategories = allCategories.filter(category =>
        category.name.toLowerCase().includes(searchForm.name.toLowerCase()) ||
        (category.description && category.description.toLowerCase().includes(searchForm.name.toLowerCase()))
      )
    }
    
    // 计算总记录数
    pagination.total = filteredCategories.length
    
    // 计算分页数据
    const start = (pagination.page - 1) * pagination.size
    const end = Math.min(start + pagination.size, filteredCategories.length)
    const pageCategories = filteredCategories.slice(start, end)
    
    tableData.value = pageCategories
    
    console.log(`显示第 ${start + 1}-${end} 条，共 ${pagination.total} 条记录`)
    console.log('场馆分类数据加载成功:', tableData.value)
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.warning('加载真实数据失败，显示模拟数据')
    
    // 使用模拟数据作为后备
    let filteredData = [...mockData]
    
    // 前端搜索过滤
    if (searchForm.name.trim()) {
      filteredData = filteredData.filter(item => 
        item.name.toLowerCase().includes(searchForm.name.toLowerCase())
      )
    }
    
    // 前端分页
    const start = (pagination.page - 1) * pagination.size
    const end = Math.min(start + pagination.size, filteredData.length)
    
    pagination.total = filteredData.length
    tableData.value = filteredData.slice(start, end)
    
    console.log(`使用模拟数据: 显示第 ${start + 1}-${end} 条，共 ${pagination.total} 条记录`)
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  pagination.page = 1
  loadData()
}

// 重置搜索
const resetSearch = () => {
  searchForm.name = ''
  pagination.page = 1
  loadData()
}

// 分页处理
const handleSizeChange = (size) => {
  pagination.size = size
  pagination.page = 1
  loadData()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadData()
}

// 选择变化处理
const handleSelectionChange = (selection) => {
  selectedItems.value = selection
}

// 新增处理
const handleAdd = () => {
  dialogMode.value = 'add'
  dialogVisible.value = true
}

// 编辑处理
const handleEdit = (row) => {
  dialogMode.value = 'edit'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 查看处理
const handleView = (row) => {
  currentItem.value = row
  viewDialogVisible.value = true
}

// 删除处理
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该分类吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 调用删除API
    await venueApi.deleteCategory(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    } else {
      ElMessage.info('已取消删除')
    }
  }
}

// 批量删除处理
const handleBatchDelete = async () => {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('请选择要删除的数据')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedItems.value.length} 条数据吗？`, 
      '提示', 
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 逐个删除选中的分类
    const deletePromises = selectedItems.value.map(item => 
      venueApi.deleteCategory(item.id)
    )
    
    await Promise.all(deletePromises)
    
    ElMessage.success(`成功删除 ${selectedItems.value.length} 条数据`)
    selectedItems.value = []
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    } else {
      ElMessage.info('已取消删除')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogMode.value === 'add') {
          // 新增分类
          await venueApi.createCategory({
            name: form.name,
            description: form.description,
            icon: form.icon,
            sort_order: form.sort_order,
            is_active: form.is_active
          })
          ElMessage.success('新增成功')
        } else {
          // 编辑分类
          await venueApi.updateCategory(form.id, {
            name: form.name,
            description: form.description,
            icon: form.icon,
            sort_order: form.sort_order,
            is_active: form.is_active
          })
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        resetForm()
        loadData()
      } catch (error) {
        console.error('操作失败:', error)
        ElMessage.error(dialogMode.value === 'add' ? '新增失败' : '更新失败')
      }
    } else {
      ElMessage.error('请检查表单填写是否正确')
    }
  })
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  Object.assign(form, {
    name: '',
    description: '',
    icon: '',
    sort_order: 0,
    is_active: true
  })
}

// 组件挂载时加载数据
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.venue-category-list {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
  font-weight: 600;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-form {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 16px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.debug-info {
  margin: 20px 0;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.debug-info h4 {
  margin: 0 0 10px 0;
  color: #409eff;
}

.debug-info p {
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
}

.view-content {
  max-height: 400px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-form {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
<template>
  <div class="venue-list">
    <div class="page-header">
      <h2>场馆管理</h2>
    </div>

    <!-- 操作工具栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">新增场馆</el-button>
      <el-button type="danger" @click="handleBatchDelete" :disabled="selectedItems.length === 0">批量删除</el-button>
      
      <!-- 搜索表单 -->
      <el-form :model="searchForm" class="search-form" inline>
        <el-form-item label="场馆名称">
          <el-input v-model="searchForm.name" placeholder="请输入场馆名称"></el-input>
        </el-form-item>
        <el-form-item label="场馆类型">
          <el-select v-model="searchForm.category_id" placeholder="请选择场馆类型" clearable>
            <el-option label="足球场" value="1"></el-option>
            <el-option label="篮球场" value="2"></el-option>
            <el-option label="羽毛球场" value="3"></el-option>
            <el-option label="网球场" value="4"></el-option>
            <el-option label="游泳池" value="5"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="searchForm.address" placeholder="请输入地址"></el-input>
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
      <el-table-column prop="name" label="场馆名称" width="180"></el-table-column>
      <el-table-column prop="category_id" label="场馆类型" width="120">
        <template #default="{ row }">
          {{ row.category.name }}
        </template>
      </el-table-column>
      <el-table-column prop="location" label="地址" width="200"></el-table-column>
      <el-table-column prop="price" label="每小时价格" width="120">
        <template #default="{ row }">
          ¥{{ row.price }}
        </template>
      </el-table-column>
      <el-table-column prop="capacity" label="容量" width="100"></el-table-column>
      <!-- <el-table-column prop="rating" label="评分" width="100">
        <template #default="{ row }">
          <el-rate v-model="row.rating" disabled show-score></el-rate>
        </template>
      </el-table-column> -->
      <!-- <el-table-column prop="total_reviews" label="总评数" width="100"></el-table-column> -->
      <el-table-column prop="is_active" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">
            {{ row.is_active ? '活跃' : '非活跃' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="text" @click="handleView(row)">查看</el-button>
          <el-button type="text" @click="handleEdit(row)">编辑</el-button>
          <el-button type="text" @click="handleDelete(row)" style="color: #f56c6c">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 调试信息 -->
    <!-- <div class="debug-info" v-if="showDebug">
      <h4>调试信息：</h4>
      <p>数据数组长度: {{ tableData.length }}</p>
      <p>总记录数: {{ pagination.total }}</p>
      <p>加载状态: {{ loading ? '加载中...' : '已完成' }}</p>
      <p>分页参数: page={{ pagination.page }}, size={{ pagination.size }}</p>
    </div> -->

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
      :title="dialogMode === 'add' ? '新增场馆' : '编辑场馆'" 
      v-model="dialogVisible"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="场馆名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入场馆名称"></el-input>
        </el-form-item>
        <el-form-item label="场馆类型" prop="category_id">
          <el-select v-model="form.category_id" placeholder="请选择场馆类型">
            <el-option label="足球场" :value="1"></el-option>
            <el-option label="篮球场" :value="2"></el-option>
            <el-option label="羽毛球场" :value="3"></el-option>
            <el-option label="网球场" :value="4"></el-option>
            <el-option label="游泳池" :value="5"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入地址"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述"></el-input>
        </el-form-item>
        <el-form-item label="图片" prop="image">
          <el-input v-model="form.image" placeholder="请输入图片URL"></el-input>
        </el-form-item>
        <el-form-item label="每小时价格" prop="hourly_rate">
          <el-input-number v-model="form.hourly_rate" :min="0" :precision="2"></el-input-number>
        </el-form-item>
        <el-form-item label="容量" prop="capacity">
          <el-input-number v-model="form.capacity" :min="1"></el-input-number>
        </el-form-item>
        <el-form-item label="评分" prop="rating">
          <el-rate v-model="form.rating" :max="5"></el-rate>
        </el-form-item>
        <el-form-item label="总评数" prop="total_reviews">
          <el-input-number v-model="form.total_reviews" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="设施" prop="facilities">
          <el-input v-model="form.facilities" placeholder="请输入设施信息"></el-input>
        </el-form-item>
        <el-form-item label="营业时间" prop="opening_hours">
          <el-input v-model="form.opening_hours" placeholder="请输入营业时间"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active" active-text="活跃" inactive-text="非活跃"></el-switch>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看对话框 -->
    <el-dialog title="场馆详情" v-model="viewDialogVisible" width="800px">
      <div v-if="currentItem" class="view-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="场馆名称">{{ currentItem.name }}</el-descriptions-item>
          <el-descriptions-item label="场馆类型">{{ currentItem.category.name }}</el-descriptions-item>
          <el-descriptions-item label="地址">{{ currentItem.address }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentItem.phone }}</el-descriptions-item>
          <el-descriptions-item label="每小时价格">¥{{ currentItem.hourly_rate }}</el-descriptions-item>
          <el-descriptions-item label="容量">{{ currentItem.capacity }}</el-descriptions-item>
          <el-descriptions-item label="评分">
            <el-rate v-model="currentItem.rating" disabled show-score></el-rate>
          </el-descriptions-item>
          <el-descriptions-item label="总评数">{{ currentItem.total_reviews }}</el-descriptions-item>
          <el-descriptions-item label="设施">{{ currentItem.facilities }}</el-descriptions-item>
          <el-descriptions-item label="营业时间">{{ currentItem.opening_hours }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="currentItem.is_active ? 'success' : 'info'">
              {{ currentItem.is_active ? '活跃' : '非活跃' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentItem.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ currentItem.updated_at }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ currentItem.description }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { nextTick } from 'vue'
import { venueApi } from '@/api/venue'
import VenueCategoryList from '../venue_categories/VenueCategoryList.vue';


// 数据响应式定义
const loading = ref(false)
const showDebug = ref(true)
const tableData = ref([])
const selectedItems = ref([])
const dialogVisible = ref(false)
const viewDialogVisible = ref(false)
const dialogMode = ref('add')
const currentItem = ref(null)
const formRef = ref(null)

const searchForm = reactive({
  name: '',
  category_id: '',
  address: ''
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const form = reactive({
  name: '',
  category_id: '',
  address: '',
  phone: '',
  description: '',
  image: '',
  hourly_rate: 0,
  capacity: 50,
  rating: 5,
  total_reviews: 0,
  facilities: '',
  opening_hours: '',
  is_active: true
})

const rules = {
  name: [
    { required: true, message: '请输入场馆名称', trigger: 'blur' }
  ],
  category_id: [
    { required: true, message: '请选择场馆类型', trigger: 'change' }
  ],
  address: [
    { required: true, message: '请输入地址', trigger: 'blur' }
  ],
  hourly_rate: [
    { required: true, message: '请输入每小时价格', trigger: 'blur' }
  ]
}

// 方法定义
const getCategoryText = (categoryId) => {
  const map = {
    1: '足球场',
    2: '篮球场',
    3: '羽毛球场',
    4: '网球场',
    5: '游泳池'
  }
  return map[categoryId] || `类型${categoryId}`
}

const fetchData = async () => {
  loading.value = true
  try {
    console.log('请求参数:', { ...searchForm, ...pagination })
    const params = {
      page: pagination.page,
      size: pagination.size,
      ...searchForm
    }
    
    // 过滤掉空值
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key]
      }
    })
    
    const response = await venueApi.getVenueList(params)
    
    const result = await response
    console.log('API响应:', result)
    tableData.value = result.data.venues || []
      pagination.total = result.data.pagination?.total || 0
      console.log('数据解析结果:', tableData.value)
  } catch (error) {
    console.error('请求错误:', error)
    ElMessage.error('网络请求失败')
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  pagination.page = 1
  fetchData()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  fetchData()
}

const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

const resetSearch = () => {
  searchForm.name = ''
  searchForm.category_id = ''
  searchForm.address = ''
  pagination.page = 1
  fetchData()
}

const handleSelectionChange = (selection) => {
  selectedItems.value = selection
}

const handleAdd = () => {
  dialogMode.value = 'add'
  dialogVisible.value = true
  nextTick(() => {
    resetForm()
  })
}

const handleEdit = (row) => {
  dialogMode.value = 'edit'
  dialogVisible.value = true
  nextTick(() => {
    Object.assign(form, row)
  })
}

const handleView = (row) => {
  currentItem.value = row
  viewDialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这个场馆吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await fetch(`/api/venues/${row.id}`, {
      method: 'DELETE'
    })
    
    const result = await response.json()
    if (result.code === 200) {
      ElMessage.success('删除成功')
      fetchData()
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    console.error('删除错误:', error)
  }
}

const handleBatchDelete = async () => {
  if (selectedItems.value.length === 0) return
  
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedItems.value.length} 个场馆吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const ids = selectedItems.value.map(item => item.id)
    const response = await fetch('/api/venues/batch_delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ ids })
    })
    
    const result = await response.json()
    if (result.code === 200) {
      ElMessage.success('批量删除成功')
      selectedItems.value = []
      fetchData()
    } else {
      ElMessage.error(result.message || '批量删除失败')
    }
  } catch (error) {
    console.error('批量删除错误:', error)
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    const url = dialogMode.value === 'add' ? '/api/venues' : `/api/venues/${form.id}`
    const method = dialogMode.value === 'add' ? 'POST' : 'PUT'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form)
    })
    
    const result = await response.json()
    if (result.code === 200) {
      ElMessage.success(dialogMode.value === 'add' ? '添加成功' : '更新成功')
      dialogVisible.value = false
      fetchData()
    } else {
      ElMessage.error(result.message || '操作失败')
    }
  } catch (error) {
    console.error('提交错误:', error)
  }
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  Object.assign(form, {
    name: '',
    category_id: '',
    address: '',
    phone: '',
    description: '',
    image: '',
    hourly_rate: 0,
    capacity: 50,
    rating: 5,
    total_reviews: 0,
    facilities: '',
    opening_hours: '',
    is_active: true
  })
}

/* 字段映射表：{ 目标参数名: 源字段名 或 转换函数 } */
const mapping = {
  name: 'name',
  venue_type: () => 'unknown',          // 原始对象里没有，给个默认值
  location: r => r.address,             // 把 address 映射成 location
  price_per_hour: 'hourly_rate',
  capacity: 'capacity',
  contact_phone: 'phone',
  business_hours: 'opening_hours',
  description: 'description',
  facilities: 'facilities',
  is_active: 'is_active',
  category: r => ({ id: r.category_id }) // 需要嵌套对象
};

/* 通用映射函数 */
function mapObject(src, map) {
  return Object.keys(map).reduce((tar, key) => {
    const rule = map[key];
    tar[key] = typeof rule === 'function' ? rule(src) : src[rule];
    return tar;
  }, {});
}

// 生命周期
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.venue-list {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  color: #333;
  margin: 0;
}

.toolbar {
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 5px;
}

.search-form {
  margin-left: 20px;
}

.search-form .el-form-item {
  margin-bottom: 0;
}

.debug-info {
  margin: 20px 0;
  padding: 15px;
  background: #f0f9ff;
  border: 1px solid #e1f5fe;
  border-radius: 5px;
  font-size: 12px;
}

.debug-info h4 {
  margin: 0 0 10px 0;
  color: #1976d2;
}

.debug-info p {
  margin: 5px 0;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.view-content {
  max-height: 400px;
  overflow-y: auto;
}
</style>
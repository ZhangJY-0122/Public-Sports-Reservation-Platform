<template>
  <div class="booking-list">
    <div class="page-header">
      <h2>预约管理</h2>
    </div>

    <!-- 操作工具栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">新增预约</el-button>
      <el-button type="danger" @click="handleBatchDelete" :disabled="selectedItems.length === 0">批量删除</el-button>
      
      <!-- 搜索表单 -->
      <el-form :model="searchForm" class="search-form" inline>
        <el-form-item label="预约编号">
          <el-input v-model="searchForm.booking_no" placeholder="请输入预约编号"></el-input>
        </el-form-item>
        <el-form-item label="用户ID">
          <el-input v-model="searchForm.user_id" placeholder="请输入用户ID"></el-input>
        </el-form-item>
        <el-form-item label="场馆ID">
          <el-input v-model="searchForm.venue_id" placeholder="请输入场馆ID"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="待确认" value="pending"></el-option>
            <el-option label="已确认" value="confirmed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="爽约" value="no_show"></el-option>
          </el-select>
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
      <el-table-column prop="booking_no" label="预约编号" width="150"></el-table-column>
      <el-table-column prop="user_name" label="用户ID" width="100"></el-table-column>
      <el-table-column prop="venue_name" label="场馆ID" width="100"></el-table-column>
      <el-table-column prop="date" label="预约日期" width="120"></el-table-column>
      <!-- <el-table-column prop="start_time" label="开始时间" width="100"></el-table-column>
      <el-table-column prop="end_time" label="结束时间" width="100"></el-table-column> -->
      <el-table-column prop="duration" label="时长(小时)" width="100"></el-table-column>
      <el-table-column prop="price" label="总价" width="100">
        <template #default="{ row }">
          ¥{{ row.price }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          {{ getStatusText(row.status) }}
        </template>
      </el-table-column>
      <!-- <el-table-column prop="is_paid" label="是否支付" width="100">
        <template #default="{ row }">
          {{ row.is_paid ? '已支付' : '未支付' }}
        </template>
      </el-table-column> -->
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="text" @click="handleView(row)">查看</el-button>
          <!-- <el-button type="text" @click="handleEdit(row)">编辑</el-button>
          <el-button type="text" @click="handleDelete(row)" style="color: #f56c6c">删除</el-button> -->
        </template>
      </el-table-column>
    </el-table>



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
      :title="dialogMode === 'add' ? '新增预约' : '编辑预约'" 
      v-model="dialogVisible"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="预约编号" prop="booking_no">
          <el-input v-model="form.booking_no" placeholder="请输入预约编号"></el-input>
        </el-form-item>
        <el-form-item label="用户ID" prop="user_id">
          <el-input-number v-model="form.user_id" :min="1"></el-input-number>
        </el-form-item>
        <el-form-item label="场馆ID" prop="venue_id">
          <el-input-number v-model="form.venue_id" :min="1"></el-input-number>
        </el-form-item>
        <el-form-item label="预约日期" prop="booking_date">
          <el-date-picker v-model="form.booking_date" type="date" placeholder="请选择预约日期" format="YYYY-MM-DD" value-format="YYYY-MM-DD"></el-date-picker>
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-time-picker v-model="form.start_time" placeholder="请选择开始时间" format="HH:mm" value-format="HH:mm"></el-time-picker>
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-time-picker v-model="form.end_time" placeholder="请选择结束时间" format="HH:mm" value-format="HH:mm"></el-time-picker>
        </el-form-item>
        <el-form-item label="时长(小时)" prop="duration_hours">
          <el-input-number v-model="form.duration_hours" :min="0.5" :step="0.5"></el-input-number>
        </el-form-item>
        <el-form-item label="单价" prop="hourly_rate">
          <el-input-number v-model="form.hourly_rate" :min="0" :precision="2"></el-input-number>
        </el-form-item>
        <el-form-item label="总价" prop="total_price">
          <el-input-number v-model="form.total_price" :min="0" :precision="2"></el-input-number>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option label="待确认" value="pending"></el-option>
            <el-option label="已确认" value="confirmed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="爽约" value="no_show"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="是否支付" prop="is_paid">
          <el-switch v-model="form.is_paid"></el-switch>
        </el-form-item>
        <el-form-item label="备注说明" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入备注说明"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看对话框 -->
    <el-dialog title="预约详情" v-model="viewDialogVisible" width="600px">
      <div v-if="currentItem" class="view-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="预约编号">{{ currentItem.booking_no }}</el-descriptions-item>
          <el-descriptions-item label="用户ID">{{ currentItem.user_id }}</el-descriptions-item>
          <el-descriptions-item label="场馆ID">{{ currentItem.venue_id }}</el-descriptions-item>
          <el-descriptions-item label="预约日期">{{ currentItem.booking_date }}</el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ currentItem.start_time }}</el-descriptions-item>
          <el-descriptions-item label="结束时间">{{ currentItem.end_time }}</el-descriptions-item>
          <el-descriptions-item label="时长(小时)">{{ currentItem.duration_hours }}</el-descriptions-item>
          <el-descriptions-item label="单价">¥{{ currentItem.hourly_rate }}</el-descriptions-item>
          <el-descriptions-item label="总价">¥{{ currentItem.total_price }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusText(currentItem.status) }}</el-descriptions-item>
          <el-descriptions-item label="是否支付">{{ currentItem.is_paid ? '已支付' : '未支付' }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentItem.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ currentItem.updated_at }}</el-descriptions-item>
          <el-descriptions-item label="备注说明" :span="2">{{ currentItem.description }}</el-descriptions-item>
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
import  request, { baseURL } from '@/utils/request'

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
  booking_no: '',
  user_id: '',
  venue_id: '',
  status: ''
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const form = reactive({
  booking_no: '',
  user_id: null,
  venue_id: null,
  booking_date: '',
  start_time: '',
  end_time: '',
  duration_hours: 1,
  hourly_rate: 0,
  total_price: 0,
  status: 'pending',
  is_paid: false,
  description: ''
})

const rules = {
  booking_no: [
    { required: true, message: '请输入预约编号', trigger: 'blur' }
  ],
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' }
  ],
  venue_id: [
    { required: true, message: '请输入场馆ID', trigger: 'blur' }
  ],
  booking_date: [
    { required: true, message: '请选择预约日期', trigger: 'change' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ]
}

// 方法定义
const getStatusText = (status) => {
  const map = {
    pending: '待确认',
    confirmed: '已确认',
    cancelled: '已取消',
    completed: '已完成',
    no_show: '爽约'
  }
  return map[status] || status
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
    
    const response = await request.get('/api/booking/list',params)

    console.log('API响应:', response)
    
    const result = await response
    console.log('API响应:', result)

    tableData.value = result.data.bookings || []
    pagination.total = result.data.pagination?.total || 0
    
 
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
  searchForm.booking_no = ''
  searchForm.user_id = ''
  searchForm.venue_id = ''
  searchForm.status = ''
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
    await ElMessageBox.confirm('确定要删除这个预约吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await fetch(`/api/bookings/${row.id}`, {
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
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedItems.value.length} 个预约吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const ids = selectedItems.value.map(item => item.id)
    const response = await fetch('/api/bookings/batch_delete', {
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
    
    const url = dialogMode.value === 'add' ? '/api/bookings' : `/api/bookings/${form.id}`
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
    booking_no: '',
    user_id: null,
    venue_id: null,
    booking_date: '',
    start_time: '',
    end_time: '',
    duration_hours: 1,
    hourly_rate: 0,
    total_price: 0,
    status: 'pending',
    is_paid: false,
    description: ''
  })
}

// 生命周期
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.booking-list {
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
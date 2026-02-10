<template>
  <div class="event-registration-list">
    <div class="page-header">
      <h2>赛事报名管理</h2>
    </div>

    <!-- 操作工具栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">新增报名</el-button>
      <el-button type="danger" @click="handleBatchDelete" :disabled="selectedItems.length === 0">批量删除</el-button>
      
      <!-- 搜索表单 -->
      <el-form :model="searchForm" class="search-form" inline>
        <el-form-item label="报名编号">
          <el-input v-model="searchForm.registration_no" placeholder="请输入报名编号"></el-input>
        </el-form-item>
        <el-form-item label="赛事ID">
          <el-input v-model="searchForm.event_id" placeholder="请输入赛事ID"></el-input>
        </el-form-item>
        <el-form-item label="用户ID">
          <el-input v-model="searchForm.user_id" placeholder="请输入用户ID"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="已报名" value="registered"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已退款" value="refunded"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="支付状态">
          <el-select v-model="searchForm.is_paid" placeholder="请选择支付状态" clearable>
            <el-option label="已支付" :value="true"></el-option>
            <el-option label="未支付" :value="false"></el-option>
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
      <el-table-column prop="registration_no" label="报名编号" width="150"></el-table-column>
      <el-table-column prop="event_id" label="赛事ID" width="100"></el-table-column>
      <el-table-column prop="user_id" label="用户ID" width="100"></el-table-column>
      <el-table-column prop="contact_info" label="联系信息" width="200"></el-table-column>
      <el-table-column prop="registration_fee_paid" label="报名费" width="100">
        <template #default="{ row }">
          ¥{{ row.registration_fee_paid }}
        </template>
      </el-table-column>
      <el-table-column prop="is_paid" label="支付状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_paid ? 'success' : 'warning'">
            {{ row.is_paid ? '已支付' : '未支付' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="报名状态" width="100">
        <template #default="{ row }">
          {{ getStatusText(row.status) }}
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
      :title="dialogMode === 'add' ? '新增赛事报名' : '编辑赛事报名'" 
      v-model="dialogVisible"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="赛事ID" prop="event_id">
          <el-input v-model="form.event_id" placeholder="请输入赛事ID"></el-input>
        </el-form-item>
        <el-form-item label="用户ID" prop="user_id">
          <el-input v-model="form.user_id" placeholder="请输入用户ID"></el-input>
        </el-form-item>
        <el-form-item label="报名编号" prop="registration_no">
          <el-input v-model="form.registration_no" placeholder="请输入报名编号"></el-input>
        </el-form-item>
        <el-form-item label="联系信息" prop="contact_info">
          <el-input v-model="form.contact_info" placeholder="请输入联系信息"></el-input>
        </el-form-item>
        <el-form-item label="附加信息" prop="additional_info">
          <el-input v-model="form.additional_info" type="textarea" :rows="3" placeholder="请输入附加信息"></el-input>
        </el-form-item>
        <el-form-item label="报名费" prop="registration_fee_paid">
          <el-input-number v-model="form.registration_fee_paid" :min="0" :precision="2"></el-input-number>
        </el-form-item>
        <el-form-item label="支付状态" prop="is_paid">
          <el-switch v-model="form.is_paid" active-text="已支付" inactive-text="未支付"></el-switch>
        </el-form-item>
        <el-form-item label="报名状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择报名状态">
            <el-option label="已报名" value="registered"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已退款" value="refunded"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看对话框 -->
    <el-dialog title="赛事报名详情" v-model="viewDialogVisible" width="600px">
      <div v-if="currentItem" class="view-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="报名编号">{{ currentItem.registration_no }}</el-descriptions-item>
          <el-descriptions-item label="赛事ID">{{ currentItem.event_id }}</el-descriptions-item>
          <el-descriptions-item label="用户ID">{{ currentItem.user_id }}</el-descriptions-item>
          <el-descriptions-item label="联系信息">{{ currentItem.contact_info }}</el-descriptions-item>
          <el-descriptions-item label="报名费">¥{{ currentItem.registration_fee_paid }}</el-descriptions-item>
          <el-descriptions-item label="支付状态">
            <el-tag :type="currentItem.is_paid ? 'success' : 'warning'">
              {{ currentItem.is_paid ? '已支付' : '未支付' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="报名状态">{{ getStatusText(currentItem.status) }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentItem.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ currentItem.updated_at }}</el-descriptions-item>
          <el-descriptions-item label="附加信息" :span="2">{{ currentItem.additional_info }}</el-descriptions-item>
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
  registration_no: '',
  event_id: '',
  user_id: '',
  status: '',
  is_paid: null
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const form = reactive({
  event_id: '',
  user_id: '',
  registration_no: '',
  contact_info: '',
  additional_info: '',
  registration_fee_paid: 0,
  is_paid: false,
  status: 'registered'
})

const rules = {
  event_id: [
    { required: true, message: '请输入赛事ID', trigger: 'blur' }
  ],
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' }
  ],
  registration_no: [
    { required: true, message: '请输入报名编号', trigger: 'blur' }
  ],
  contact_info: [
    { required: true, message: '请输入联系信息', trigger: 'blur' }
  ]
}

// 方法定义
const getStatusText = (status) => {
  const map = {
    registered: '已报名',
    cancelled: '已取消',
    completed: '已完成',
    refunded: '已退款'
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
    
    const response = await fetch('/api/event_registrations/list', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    const result = await response.json()
    console.log('API响应:', result)
    
    if (result.code === 200) {
      tableData.value = result.data.event_registrations || []
      pagination.total = result.data.pagination?.total || 0
      console.log('数据解析结果:', tableData.value)
    } else {
      console.error('API错误:', result.message)
      ElMessage.error(result.message || '获取数据失败')
    }
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
  searchForm.registration_no = ''
  searchForm.event_id = ''
  searchForm.user_id = ''
  searchForm.status = ''
  searchForm.is_paid = null
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
    await ElMessageBox.confirm('确定要删除这个赛事报名吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await fetch(`/api/event_registrations/${row.id}`, {
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
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedItems.value.length} 个赛事报名吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const ids = selectedItems.value.map(item => item.id)
    const response = await fetch('/api/event_registrations/batch_delete', {
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
    
    const url = dialogMode.value === 'add' ? '/api/event_registrations' : `/api/event_registrations/${form.id}`
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
    event_id: '',
    user_id: '',
    registration_no: '',
    contact_info: '',
    additional_info: '',
    registration_fee_paid: 0,
    is_paid: false,
    status: 'registered'
  })
}

// 生命周期
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.event-registration-list {
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
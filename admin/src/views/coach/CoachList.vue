<template>
  <div class="coach-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>教练管理</h1>
      <p>管理教练信息，支持新增、编辑、删除操作</p>
    </div>

    <!-- 操作工具栏 -->
    <el-card class="tool-card">
      <div class="toolbar">
        <div class="left-tools">
          <el-button type="primary" @click="handle_add">
            <el-icon><Plus /></el-icon>
            新增教练
          </el-button>
          <el-button type="danger" :disabled="selected_ids.length === 0" @click="handle_batch_delete">
            <el-icon><Delete /></el-icon>
            批量删除
          </el-button>
        </div>
        <div class="right-tools">
          <el-input
            v-model="search_form.name"
            placeholder="请输入教练姓名"
            clearable
            style="width: 200px"
            @keyup.enter="handle_search"
            @clear="handle_search"
          >
            <template #append>
              <el-button @click="handle_search">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
          <el-input
            v-model="search_form.specialization"
            placeholder="请输入专业领域"
            clearable
            style="width: 200px; margin-left: 10px;"
            @keyup.enter="handle_search"
            @clear="handle_search"
          >
            <template #append>
              <el-button @click="handle_search">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
          <el-button type="info" @click="handle_reset" style="margin-left: 10px;">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <div style="margin-bottom: 10px; padding: 10px; background: #f0f9ff; border: 1px solid #d0e8ff; border-radius: 4px;">
        <p><strong>调试信息:</strong></p>
        <p>数据数组长度: {{ items.length }}</p>
        <p>总记录数: {{ total }}</p>
        <p>加载状态: {{ loading ? '正在加载' : '加载完成' }}</p>
        <p>当前页: {{ current_page }}, 每页大小: {{ page_size }}</p>
      </div>
      
      <el-table
        :data="items"
        v-loading="loading"
        @selection-change="handle_selection_change"
        style="width: 100%"
        stripe
        empty-text="暂无数据"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" sortable />
        <el-table-column prop="name" label="教练姓名" width="120" show-overflow-tooltip />
        <el-table-column prop="specialization" label="专业领域" width="150" show-overflow-tooltip />
        <el-table-column prop="experience_years" label="从业年限" width="100" />
        <el-table-column prop="hourly_rate" label="时薪" width="80" />
        <el-table-column prop="rating" label="评分" width="80" />
        <el-table-column prop="total_sessions" label="授课次数" width="100" />
        <el-table-column prop="phone" label="联系电话" width="120" show-overflow-tooltip />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="scope">
            {{ scope.row.is_active ? '启用' : '禁用' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="200">
          <template #default="scope">
            <el-button size="small" @click="handle_edit(scope.row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button size="small" @click="handle_view(scope.row)">
              <el-icon><View /></el-icon>
              查看
            </el-button>
            <el-button size="small" type="danger" @click="handle_delete(scope.row.id)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="current_page"
          v-model:page-size="page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handle_size_change"
          @current-change="handle_current_change"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      :title="dialog_title"
      v-model="dialog_visible"
      width="700px"
      :close-on-click-modal="false"
      @closed="handle_dialog_closed"
    >
      <el-form
        ref="form_ref"
        :model="form_data"
        :rules="form_rules"
        label-width="100px"
        label-position="left"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="教练姓名" prop="name">
              <el-input 
                v-model="form_data.name" 
                placeholder="请输入教练姓名" 
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="专业领域" prop="specialization">
              <el-input 
                v-model="form_data.specialization" 
                placeholder="请输入专业领域" 
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="从业年限" prop="experience_years">
              <el-input-number 
                v-model="form_data.experience_years" 
                :min="0"
                placeholder="请输入从业年限"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input 
                v-model="form_data.phone" 
                placeholder="请输入联系电话" 
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="每小时费用" prop="hourly_rate">
              <el-input-number 
                v-model="form_data.hourly_rate" 
                :min="0"
                :precision="2"
                placeholder="请输入每小时费用"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="评分" prop="rating">
              <el-rate 
                v-model="form_data.rating" 
                :max="5"
                :allow-half="true"
                show-score
                text-color="#ff9900"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="教练介绍" prop="introduction">
          <el-input 
            v-model="form_data.introduction" 
            type="textarea" 
            :rows="3"
            placeholder="请输入教练介绍" 
          />
        </el-form-item>
        
        <el-form-item label="教练头像" prop="avatar">
          <el-input 
            v-model="form_data.avatar" 
            placeholder="请输入头像URL" 
          />
        </el-form-item>
        
        <el-form-item label="状态" prop="is_active">
          <el-switch 
            v-model="form_data.is_active" 
            active-text="启用" 
            inactive-text="禁用" 
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialog_visible = false">取消</el-button>
          <el-button type="primary" @click="handle_submit" :loading="submitting">
            {{ submit_button_text }}
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 查看对话框 -->
    <el-dialog
      title="查看教练详情"
      v-model="view_dialog_visible"
      width="600px"
    >
      <el-descriptions :column="2" border v-if="current_row">
        <el-descriptions-item label="ID">{{ current_row.id }}</el-descriptions-item>
        <el-descriptions-item label="教练姓名">{{ current_row.name }}</el-descriptions-item>
        <el-descriptions-item label="专业领域">{{ current_row.specialization }}</el-descriptions-item>
        <el-descriptions-item label="从业年限">{{ current_row.experience_years }}年</el-descriptions-item>
        <el-descriptions-item label="每小时费用">¥{{ current_row.hourly_rate }}</el-descriptions-item>
        <el-descriptions-item label="评分">{{ current_row.rating }}</el-descriptions-item>
        <el-descriptions-item label="授课次数">{{ current_row.total_sessions }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ current_row.phone }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="current_row.is_active ? 'success' : 'info'">
            {{ current_row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(current_row.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="更新时间" v-if="current_row.updated_at">{{ formatDate(current_row.updated_at) }}</el-descriptions-item>
        <el-descriptions-item label="教练介绍" :span="2">{{ current_row.introduction || '暂无介绍' }}</el-descriptions-item>
        <el-descriptions-item label="头像" :span="2" v-if="current_row.avatar">
          <el-image 
            :src="current_row.avatar" 
            style="width: 100px; height: 100px"
            :preview-src-list="[current_row.avatar]"
            fit="cover"
          />
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, Search, Refresh, Edit, View } from '@element-plus/icons-vue'
import { get_user_id_from_storage } from '../../utils/auth'

// 响应式数据
const items = ref([])
const total = ref(0)
const loading = ref(false)
const current_page = ref(1)
const page_size = ref(20)
const selected_ids = ref([])

// 搜索表单
const search_form = reactive({
  name: '',
  specialization: ''
})

// 表单数据
const form_data = reactive({
  id: null,
  name: '',
  specialization: '',
  experience_years: 0,
  introduction: '',
  avatar: '',
  phone: '',
  hourly_rate: 0,
  rating: 5.0,
  total_sessions: 0,
  is_active: true
})

// 表单验证规则
const form_rules = {
  name: [
    { required: true, message: '请输入教练姓名', trigger: 'blur' },
    { min: 1, max: 50, message: '教练姓名长度为1-50字符', trigger: 'blur' }
  ],
  specialization: [
    { required: true, message: '请输入专业领域', trigger: 'blur' },
    { min: 1, max: 100, message: '专业领域长度为1-100字符', trigger: 'blur' }
  ],
  experience_years: [
    { type: 'number', min: 0, message: '从业年限不能为负数', trigger: 'blur' }
  ],
  hourly_rate: [
    { type: 'number', min: 0, message: '每小时费用不能为负数', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

// 对话框控制
const dialog_visible = ref(false)
const view_dialog_visible = ref(false)
const current_row = ref(null)
const form_ref = ref(null)
const submitting = ref(false)

// 计算属性
const dialog_title = computed(() => {
  return form_data.id ? '编辑教练' : '新增教练'
})

const submit_button_text = computed(() => {
  return submitting.value ? '提交中...' : '确认提交'
})

// 获取数据
const get_items = async () => {
  try {
    console.log('开始获取教练数据...')
    loading.value = true
    
    // 构建查询参数
    const params = new URLSearchParams({
      page: current_page.value,
      page_size: page_size.value
    })
    
    // 添加搜索条件
    if (search_form.name.trim()) {
      params.append('name', search_form.name.trim())
    }
    if (search_form.specialization.trim()) {
      params.append('specialization', search_form.specialization.trim())
    }
    
    console.log('查询参数:', Object.fromEntries(params))
    
    const user_id = get_user_id_from_storage()
    const response = await fetch(`http://127.0.0.1:5000/api/coaches/list?${params}`, {
      headers: {
        'Content-Type': 'application/json',
        'User-Id': user_id || ''
      }
    })
    
    console.log('响应状态:', response.status)
    const res = await response.json()
    console.log('API响应:', res)
    
    if (res.code === 0) {
      // 数据处理
      const venues = res.data.coaches
      const pagination = res.data.pagination
      
      console.log('解析后的数据:', venues)
      console.log('分页信息:', pagination)
      
      // 强制响应式更新
      await nextTick()
      items.value = venues
      total.value = pagination.total
      
      console.log('赋值后的items长度:', items.value.length)
      console.log('当前items值:', items.value)
      
      await nextTick()
      console.log('nextTick后的items长度:', items.value.length)
      console.log('nextTick后的total值:', total.value)
    } else {
      console.error('API返回错误:', res.message)
      ElMessage.error(res.message || '获取数据失败')
    }
  } catch (error) {
    console.error('获取数据异常:', error)
    ElMessage.error('获取数据失败: ' + error.message)
  } finally {
    loading.value = false
    console.log('数据加载完成，loading设置为false')
  }
}

// 搜索处理
const handle_search = () => {
  current_page.value = 1
  get_items()
}

// 重置处理
const handle_reset = () => {
  search_form.name = ''
  search_form.specialization = ''
  current_page.value = 1
  get_items()
}

// 分页处理
const handle_size_change = (val) => {
  page_size.value = val
  current_page.value = 1
  get_items()
}

const handle_current_change = (val) => {
  current_page.value = val
  get_items()
}

// 选择处理
const handle_selection_change = (selection) => {
  selected_ids.value = selection.map(item => item.id)
}

// 新增处理
const handle_add = () => {
  Object.assign(form_data, {
    id: null,
    name: '',
    specialization: '',
    experience_years: 0,
    introduction: '',
    avatar: '',
    phone: '',
    hourly_rate: 0,
    rating: 5.0,
    total_sessions: 0,
    is_active: true
  })
  dialog_visible.value = true
}

// 编辑处理
const handle_edit = (row) => {
  Object.assign(form_data, row)
  dialog_visible.value = true
}

// 查看处理
const handle_view = (row) => {
  current_row.value = row
  view_dialog_visible.value = true
}

// 删除处理
const handle_delete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个教练吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const user_id = get_user_id_from_storage()
    const response = await fetch(`http://127.0.0.1:5000/api/coaches/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'User-Id': user_id || ''
      }
    })
    
    const res = await response.json()
    
    if (res.code === 0) {
      ElMessage.success('删除成功')
      get_items()
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + error.message)
    }
  }
}

// 批量删除处理
const handle_batch_delete = async () => {
  if (selected_ids.value.length === 0) {
    ElMessage.warning('请选择要删除的教练')
    return
  }
  
  try {
    await ElMessageBox.confirm(`确定要删除选中的${selected_ids.value.length}个教练吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const user_id = get_user_id_from_storage()
    const response = await fetch('http://127.0.0.1:5000/api/coaches/batch-delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Id': user_id || ''
      },
      body: JSON.stringify({ ids: selected_ids.value })
    })
    
    const res = await response.json()
    
    if (res.code === 0) {
      ElMessage.success('批量删除成功')
      selected_ids.value = []
      get_items()
    } else {
      ElMessage.error(res.message || '批量删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败: ' + error.message)
    }
  }
}

// 表单提交处理
const handle_submit = async () => {
  try {
    await form_ref.value.validate()
    
    submitting.value = true
    const user_id = get_user_id_from_storage()
    
    const url = form_data.id 
      ? `http://127.0.0.1:5000/api/coaches/${form_data.id}`
      : 'http://127.0.0.1:5000/api/coaches'
    
    const method = form_data.id ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'User-Id': user_id || ''
      },
      body: JSON.stringify(form_data)
    })
    
    const res = await response.json()
    
    if (res.code === 0) {
      ElMessage.success(form_data.id ? '更新成功' : '新增成功')
      dialog_visible.value = false
      get_items()
    } else {
      ElMessage.error(res.message || '操作失败')
    }
  } catch (error) {
    ElMessage.error('操作失败: ' + error.message)
  } finally {
    submitting.value = false
  }
}

// 对话框关闭处理
const handle_dialog_closed = () => {
  form_ref.value?.resetFields()
}

// 工具函数
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 页面加载时获取数据
onMounted(() => {
  get_items()
})
</script>

<style scoped>
.coach-management {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.page-header p {
  margin: 8px 0 0 0;
  color: #606266;
  font-size: 14px;
}

.tool-card {
  margin-bottom: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left-tools,
.right-tools {
  display: flex;
  align-items: center;
  gap: 10px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    gap: 10px;
  }
  
  .left-tools,
  .right-tools {
    width: 100%;
    justify-content: center;
  }
}
</style>
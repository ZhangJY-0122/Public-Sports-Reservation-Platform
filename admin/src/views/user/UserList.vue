<template>
    <div class="user-management">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1>用户管理</h1>
        <p>管理系统用户信息，支持新增、编辑、删除操作</p>
      </div>
  
      <!-- 操作工具栏 -->
      <el-card class="tool-card">
        <div class="toolbar">
          <div class="left-tools">
            <el-button type="primary" @click="handle_add">
              <el-icon><Plus /></el-icon>
              新增用户
            </el-button>
            <el-button type="danger" :disabled="selected_ids.length === 0" @click="handle_batch_delete">
              <el-icon><Delete /></el-icon>
              批量删除
            </el-button>
          </div>
          <div class="right-tools">
            <el-input
              v-model="search_form.username"
              placeholder="请输入用户名"
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
            <el-button type="info" @click="handle_reset">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </div>
        </div>
      </el-card>
  
      <!-- 数据表格 -->
      <el-card class="table-card">
        <el-table
          :data="items"
          v-loading="loading"
          @selection-change="handle_selection_change"
          style="width: 100%"
          stripe
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" sortable />
          <el-table-column prop="username" label="用户名" width="150" />
          <el-table-column prop="real_name" label="真实姓名" width="150" />
          <el-table-column prop="email" label="邮箱" width="200" />
          <el-table-column prop="phone" label="手机号" width="120" />
          <el-table-column prop="role" label="角色" width="120">
            <template #default="scope">
              <el-tag :type="get_role_type(scope.row.role)">
                {{ get_role_text(scope.row.role) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="is_active" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
                {{ scope.row.is_active ? '激活' : '停用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" fixed="right" width="200">
            <template #default="scope">
              <el-button size="small" @click="handle_edit(scope.row)">
                <el-icon><Edit /></el-icon>
                编辑
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
        width="500px"
        :close-on-click-modal="false"
        @closed="handle_dialog_closed"
      >
        <el-form
          ref="form_ref"
          :model="form_data"
          :rules="form_rules"
          label-width="80px"
          label-position="left"
        >
          <el-form-item label="用户名" prop="username">
            <el-input 
              v-model="form_data.username" 
              placeholder="请输入用户名" 
              :disabled="is_editing"
            />
          </el-form-item>
          
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="form_data.email" placeholder="请输入邮箱" />
          </el-form-item>
          
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="form_data.phone" placeholder="请输入手机号" />
          </el-form-item>
          
          <el-form-item label="真实姓名" prop="real_name">
            <el-input v-model="form_data.real_name" placeholder="请输入真实姓名" />
          </el-form-item>
          
          <el-form-item label="城市" prop="city">
            <el-input v-model="form_data.city" placeholder="请输入城市" />
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input 
              v-model="form_data.password" 
              type="password"
              :placeholder="is_editing ? '留空表示不修改密码' : '请输入密码'" 
              show-password
            />
          </el-form-item>
          
          <el-form-item label="角色" prop="role">
            <el-select v-model="form_data.role" placeholder="请选择角色" style="width: 100%">
              <el-option label="管理员" value="admin" />
              <el-option label="普通用户" value="user" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="状态" prop="is_active" v-if="is_editing">
            <el-switch 
              v-model="form_data.is_active" 
              active-text="激活" 
              inactive-text="停用"
            />
          </el-form-item>
        </el-form>
        
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialog_visible = false">取消</el-button>
            <el-button type="primary" @click="handle_submit" :loading="submitting">
              {{ submitting ? '提交中...' : '确定' }}
            </el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, computed } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { Plus, Delete, Search, Refresh, Edit } from '@element-plus/icons-vue'
  import request from '@/utils/request'
  
  // 响应式数据
  const items = ref([])
  const loading = ref(false)
  const total = ref(0)
  const current_page = ref(1)
  const page_size = ref(10)
  const selected_ids = ref([])
  const dialog_visible = ref(false)
  const submitting = ref(false)
  const form_ref = ref()
  const is_editing = ref(false)
  
  // 搜索表单
  const search_form = reactive({
    username: ''
  })
  
  // 表单数据
  const form_data = reactive({
    id: '',
    username: '',
    email: '',
    phone: '',
    real_name: '',
    city: '',
    password: '',
    role: 'user',
    is_active: true
  })
  
  // 表单验证规则
  const form_rules = {
    username: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 2, max: 50, message: '用户名长度在 2 到 50 个字符', trigger: 'blur' }
    ],
    email: [
      { required: true, message: '请输入邮箱', trigger: 'blur' },
      { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
    ],
    real_name: [
      { required: true, message: '请输入真实姓名', trigger: 'blur' },
      { min: 1, max: 50, message: '真实姓名长度在 1 到 50 个字符', trigger: 'blur' }
    ],
    password: [
      { 
        required: true, 
        message: '请输入密码', 
        trigger: 'blur',
        validator: (rule, value, callback) => {
          if (!is_editing.value && !value) {
            callback(new Error('请输入密码'))
          } else {
            callback()
          }
        }
      },
      { min: 4, max: 50, message: '密码长度在 4 到 50 个字符', trigger: 'blur' }
    ],
    role: [
      { required: true, message: '请选择角色', trigger: 'change' }
    ]
  }
  
  // 计算属性
  const dialog_title = computed(() => {
    return is_editing.value ? '编辑用户' : '新增用户'
  })
  
  // 角色类型颜色映射
  const get_role_type = (role) => {
    const typeMap = {
      'admin': 'danger',
      'user': 'primary'
    }
    return typeMap[role] || 'info'
  }
  
  // 角色文本映射
  const get_role_text = (role) => {
    const textMap = {
      'admin': '管理员',
      'user': '普通用户'
    }
    return textMap[role] || '未知'
  }
  
  // 获取数据
  const get_items = async () => {
    loading.value = true
    try {
      const params = {
        page: current_page.value,
        page_size: page_size.value,
        username: search_form.username
      }
      
      let res = await request.get('/api/user/list', params)
      items.value = res.data.data.users || res.data.data.list || []
      total.value = res.data.data.pagination?.total || res.data.data.total_records || 0
    } catch (error) {
      console.error('获取数据失败:', error)
      ElMessage.error('获取数据失败：' + (error.response?.data?.message || error.message))
    } finally {
      loading.value = false
    }
  }
  
  // 搜索
  const handle_search = () => {
    current_page.value = 1
    get_items()
  }
  
  // 重置
  const handle_reset = () => {
    search_form.username = ''
    current_page.value = 1
    get_items()
  }
  
  // 分页大小改变
  const handle_size_change = (val) => {
    page_size.value = val
    get_items()
  }
  
  // 当前页改变
  const handle_current_change = (val) => {
    current_page.value = val
    get_items()
  }
  
  // 表格选择变化
  const handle_selection_change = (selection) => {
    selected_ids.value = selection.map(item => item.id)
  }
  
  // 新增
  const handle_add = () => {
    is_editing.value = false
    Object.keys(form_data).forEach(key => {
      form_data[key] = ''
    })
    dialog_visible.value = true
  }
  
  // 编辑
  const handle_edit = (row) => {
    is_editing.value = true
    form_data.id = row.id
    form_data.username = row.username
    form_data.email = row.email || ''
    form_data.phone = row.phone || ''
    form_data.real_name = row.real_name || ''
    form_data.city = row.city || ''
    form_data.password = ''
    form_data.role = row.role || 'user'
    form_data.is_active = row.is_active !== false
    dialog_visible.value = true
  }
  
  // 删除
  const handle_delete = async (id) => {
    try {
      await ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      })
      
      await request.post('/api/user/delete', { id })
      ElMessage.success('删除成功')
      get_items()
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('删除失败：' + (error.response?.data?.message || error.message))
      }
    }
  }
  
  // 批量删除
  const handle_batch_delete = async () => {
    if (selected_ids.value.length === 0) {
      ElMessage.warning('请选择要删除的记录')
      return
    }
    
    try {
      await ElMessageBox.confirm(`确定要删除选中的 ${selected_ids.value.length} 条记录吗？`, '提示', {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      })
      
      // 逐个删除用户
      for (const id of selected_ids.value) {
        await request.post('/api/user/delete', { id })
      }
      
      ElMessage.success('批量删除成功')
      selected_ids.value = []
      get_items()
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('批量删除失败：' + (error.response?.data?.message || error.message))
      }
    }
  }
  
  // 对话框关闭
  const handle_dialog_closed = () => {
    form_ref.value?.resetFields()
  }
  
  // 提交表单
  const handle_submit = async () => {
    if (!form_ref.value) return
    
    try {
      await form_ref.value.validate()
      submitting.value = true
      
      const submit_data = { ...form_data }
      
      // 如果是编辑且密码为空，则不更新密码
      if (is_editing.value && !submit_data.password) {
        delete submit_data.password
      }
      
      const api = is_editing.value ? '/api/user/update' : '/api/user/create'
      await request.post(api, submit_data)
      
      ElMessage.success(is_editing.value ? '编辑成功' : '新增成功')
      dialog_visible.value = false
      get_items()
    } catch (error) {
      if (error.errors) {
        ElMessage.warning('请完善表单信息')
      } else {
        ElMessage.error('操作失败：' + (error.response?.data?.message || error.message))
      }
    } finally {
      submitting.value = false
    }
  }
  
  // 生命周期
  onMounted(() => {
    get_items()
  })
  </script>
  
  <style scoped>
  .user-management {
    padding: 20px;
    background-color: #f5f7fa;
    min-height: 100vh;
  }
  
  .page-header {
    margin-bottom: 20px;
  }
  
  .page-header h1 {
    color: #303133;
    margin-bottom: 8px;
    font-size: 24px;
    font-weight: 600;
  }
  
  .page-header p {
    color: #606266;
    margin: 0;
    font-size: 14px;
  }
  
  .tool-card {
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
  }
  
  .left-tools, .right-tools {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .table-card {
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .pagination-container {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
    padding: 10px 0;
  }
  
  /* 响应式设计 */
  @media (max-width: 768px) {
    .user-management {
      padding: 10px;
    }
    
    .toolbar {
      flex-direction: column;
      align-items: stretch;
    }
    
    .left-tools, .right-tools {
      justify-content: center;
    }
    
    .right-tools {
      margin-top: 10px;
    }
    
    .page-header h1 {
      font-size: 20px;
    }
  }
  
  /* 表格样式优化 */
  :deep(.el-table) {
    border-radius: 8px;
  }
  
  :deep(.el-table th) {
    background-color: #f8f9fa;
    font-weight: 600;
  }
  
  :deep(.el-table .el-button) {
    margin: 2px;
  }
  </style>
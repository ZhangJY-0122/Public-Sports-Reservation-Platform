<template>
  <div class="scenic-management">
    <!-- 页面头部 -->
    <div class="header">
      <h1>景点管理</h1>
      <el-button type="primary" @click="handleAdd">新增景点</el-button>
    </div>

    <!-- 查询表单 -->
    <div class="query-form">
      <el-form :model="query_form" label-width="80px">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="景点名称">
              <el-input v-model="query_form.name" placeholder="请输入景点名称" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="地址">
              <el-input v-model="query_form.address" placeholder="请输入地址" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="价格范围">
              <el-col :span="11">
                <el-input v-model="query_form.min_price" placeholder="最低价" type="number" />
              </el-col>
              <el-col :span="2" style="text-align: center">-</el-col>
              <el-col :span="11">
                <el-input v-model="query_form.max_price" placeholder="最高价" type="number" />
              </el-col>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="评分">
              <el-select v-model="query_form.rating" placeholder="请选择评分" clearable>
                <el-option label="1星及以上" value="1" />
                <el-option label="2星及以上" value="2" />
                <el-option label="3星及以上" value="3" />
                <el-option label="4星及以上" value="4" />
                <el-option label="5星" value="5" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24" style="text-align: right">
            <el-button type="primary" @click="handleQuery">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <!-- 数据表格 -->
    <div class="table-container">
      <el-table :data="items" stripe border v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="景点名称" min-width="200" />
        <el-table-column prop="address" label="地址" min-width="200" />
        <el-table-column label="价格" width="120">
          <template #default="slotProps">
            <span>¥{{ getSafeValue(slotProps, 'row.price', '--') }}</span>
          </template>
        </el-table-column>
        <el-table-column label="原价" width="120">
          <template #default="slotProps">
            <span>¥{{ getSafeValue(slotProps, 'row.original_price', '--') }}</span>
          </template>
        </el-table-column>
        <el-table-column label="评分" width="120">
          <template #default="slotProps">
            <el-rate 
              :model-value="Number(getSafeValue(slotProps, 'row.rating', 0))" 
              disabled 
              show-score 
              text-color="#ff9900" 
            />
          </template>
        </el-table-column>
        <el-table-column prop="open_time" label="开放时间" min-width="150" />
        <el-table-column label="图片" width="150">
          <template #default="slotProps">
            <div class="image-preview" v-if="getSafeValue(slotProps, 'row.images')">
              <img 
                v-for="(img, index) in getSafeValue(slotProps, 'row.images', '').split(',')" 
                :key="index" 
                :src="img" 
                alt="景点图片"
                @click="handleImagePreview(getSafeValue(slotProps, 'row.images', ''))"
              />
            </div>
            <span v-else>--</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="slotProps">
            <div class="action-buttons" v-if="slotProps && slotProps.row">
              <el-button size="small" @click="handleEdit(slotProps.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(slotProps.row)">删除</el-button>
            </div>
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
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog 
      :title="dialog_title" 
      v-model="dialog_visible" 
      width="800px"
      :before-close="handleCloseDialog"
    >
      <el-form 
        :model="form" 
        :rules="rules" 
        ref="form_ref" 
        label-width="100px"
      >
        <el-form-item label="景点名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入景点名称" />
        </el-form-item>
        <el-form-item label="景点描述" prop="description">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入景点描述" 
          />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入地址" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="价格" prop="price">
              <el-input v-model="form.price" type="number" placeholder="请输入价格">
                <template #prepend>¥</template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="原价" prop="original_price">
              <el-input v-model="form.original_price" type="number" placeholder="请输入原价">
                <template #prepend>¥</template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="评分" prop="rating">
          <el-rate v-model="form.rating" show-score text-color="#ff9900" />
        </el-form-item>
        <el-form-item label="图片" prop="images">
          <el-input 
            v-model="form.images" 
            type="textarea" 
            :rows="2" 
            placeholder="请输入图片URL，多个URL用逗号分隔" 
          />
          <div class="image-preview" v-if="form.images">
            <img 
              v-for="(img, index) in form.images.split(',')" 
              :key="index" 
              :src="img" 
              alt="预览图片"
            />
          </div>
        </el-form-item>
        <el-form-item label="开放时间" prop="open_time">
          <el-input v-model="form.open_time" placeholder="请输入开放时间" />
        </el-form-item>
        <el-form-item label="交通信息" prop="transport">
          <el-input 
            v-model="form.transport" 
            type="textarea" 
            :rows="2" 
            placeholder="请输入交通信息" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 图片预览对话框 -->
    <el-dialog v-model="image_preview_visible" title="图片预览">
      <el-carousel :interval="4000" type="card" height="300px" v-if="preview_images.length">
        <el-carousel-item v-for="(img, index) in preview_images" :key="index">
          <img :src="img" alt="景点图片" style="width: 100%; height: 100%; object-fit: cover;" />
        </el-carousel-item>
      </el-carousel>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const items = ref([])
const total = ref(0)
const current_page = ref(1)
const page_size = ref(10)
const loading = ref(false)
const dialog_visible = ref(false)
const dialog_title = ref('')
const form_ref = ref(null)
const image_preview_visible = ref(false)
const preview_images = ref([])

// 查询表单
const query_form = reactive({
  name: '',
  address: '',
  min_price: '',
  max_price: '',
  rating: ''
})

// 表单数据
const form = reactive({
  id: '',
  name: '',
  description: '',
  address: '',
  price: '',
  original_price: '',
  rating: 0,
  images: '',
  open_time: '',
  transport: ''
})

// 表单验证规则
const rules = reactive({
  name: [
    { required: true, message: '请输入景点名称', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入景点描述', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入地址', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (value === '' || isNaN(value)) {
          callback(new Error('价格必须为数字'))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ],
  original_price: [
    { 
      validator: (rule, value, callback) => {
        if (value && isNaN(value)) {
          callback(new Error('原价必须为数字'))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ],
  rating: [
    { required: true, message: '请选择评分', trigger: 'change' }
  ]
})

// 安全获取值的辅助函数
const getSafeValue = (obj, path, defaultValue = '') => {
  if (!obj) return defaultValue
  
  const keys = path.split('.')
  let result = obj
  
  for (const key of keys) {
    if (result === null || result === undefined) {
      return defaultValue
    }
    result = result[key]
  }
  
  return result === undefined || result === null ? defaultValue : result
}

// 获取景点列表
const get_items = async () => {
  loading.value = true
  try {
    const params = {
      page: current_page.value,
      page_size: page_size.value,
      ...query_form
    }
    
    // 过滤空值
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key]
      }
    })
    
    let res = await request.post('/getsceniclist', params)
    items.value = res.data.data.list || []
    total.value = res.data.data.total_records || 0
  } catch (error) {
    console.error('获取景点列表失败:', error)
    ElMessage.error('获取景点列表失败')
    items.value = []
  } finally {
    loading.value = false
  }
}

// 查询
const handleQuery = () => {
  current_page.value = 1
  get_items()
}

// 重置查询表单
const handleReset = () => {
  Object.keys(query_form).forEach(key => {
    query_form[key] = ''
  })
  current_page.value = 1
  get_items()
}

// 分页大小改变
const handleSizeChange = (val) => {
  page_size.value = val
  get_items()
}

// 当前页改变
const handleCurrentChange = (val) => {
  current_page.value = val
  get_items()
}

// 新增景点
const handleAdd = () => {
  dialog_title.value = '新增景点'
  
  // 重置表单
  Object.keys(form).forEach(key => {
    form[key] = ''
  })
  form.rating = 0
  
  dialog_visible.value = true
}

// 编辑景点
const handleEdit = (row) => {
  if (!row) return
  
  dialog_title.value = '编辑景点'
  
  // 填充表单数据
  Object.keys(form).forEach(key => {
    if (row[key] !== undefined && row[key] !== null) {
      form[key] = row[key]
    } else {
      form[key] = ''
    }
  })
  
  // 确保评分是数字类型
  form.rating = Number(form.rating) || 0
  
  dialog_visible.value = true
}

// 删除景点
const handleDelete = (row) => {
  if (!row) return
  
  ElMessageBox.confirm(
    `确定要删除景点"${row.name}"吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      await request.post('/deletescenic', { id: row.id })
      ElMessage.success('删除成功')
      get_items()
    } catch (error) {
      console.error('删除景点失败:', error)
      ElMessage.error('删除景点失败')
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 关闭对话框
const handleCloseDialog = () => {
  dialog_visible.value = false
  if (form_ref.value) {
    form_ref.value.resetFields()
  }
}

// 提交表单
const handleSubmit = () => {
  if (!form_ref.value) return
  
  form_ref.value.validate(async (valid) => {
    if (valid) {
      try {
        // 转换数字字段
        const submitData = {
          ...form,
          price: form.price ? Number(form.price) : 0,
          original_price: form.original_price ? Number(form.original_price) : 0,
          rating: Number(form.rating)
        }
        
        if (form.id) {
          // 编辑景点
          await request.post('/updatescenic', submitData)
          ElMessage.success('更新成功')
        } else {
          // 新增景点
          await request.post('/addscenic', submitData)
          ElMessage.success('新增成功')
        }
        dialog_visible.value = false
        get_items()
      } catch (error) {
        console.error('保存景点失败:', error)
        ElMessage.error('保存景点失败')
      }
    } else {
      ElMessage.error('请填写完整信息')
    }
  })
}

// 图片预览
const handleImagePreview = (images) => {
  if (!images) return
  preview_images.value = images.split(',')
  image_preview_visible.value = true
}

// 模拟请求类
const request = {
  post: async (url, data) => {
    // 这里应该替换为实际的API请求
    console.log('请求URL:', url, '数据:', data)
    
    // 模拟API响应延迟
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 模拟响应数据
    if (url === '/getsceniclist') {
      const page = data.page || 1
      const page_size = data.page_size || 10
      
      // 生成模拟数据
      const mockData = Array.from({length: page_size}, (_, index) => {
        const id = (page - 1) * page_size + index + 1
        return {
          id,
          name: `景点${id}`,
          description: `这是景点${id}的描述信息，非常美丽值得一游。`,
          address: `地址${id}`,
          price: Math.round(Math.random() * 200 + 50),
          original_price: Math.round(Math.random() * 300 + 100),
          rating: (Math.random() * 2 + 3).toFixed(1),
          images: 'https://picsum.photos/200/150?random=1,https://picsum.photos/200/150?random=2',
          open_time: '08:00-18:00',
          transport: '公交、地铁可达',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
      })
      
      return {
        data: {
          data: {
            list: mockData,
            total_records: 100
          }
        }
      }
    } else if (url === '/addscenic' || url === '/updatescenic') {
      return { data: { success: true } }
    } else if (url === '/deletescenic') {
      return { data: { success: true } }
    }
  }
}

// 初始化
onMounted(() => {
  get_items()
})
</script>

<style scoped>
.scenic-management {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  color: #303133;
  margin: 0;
}

.query-form {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.table-container {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.image-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.image-preview img {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.3s;
}

.image-preview img:hover {
  transform: scale(1.05);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
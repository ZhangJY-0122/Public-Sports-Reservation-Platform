<template>
  <div class="scenic-container">
    <!-- 查询表单 -->
    <el-card class="search-card">
      <el-form :model="search_form" inline>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="景点名称">
              <el-input v-model="search_form.name" placeholder="请输入景点名称" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="景点地址">
              <el-input v-model="search_form.address" placeholder="请输入景点地址" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="价格范围">
              <el-input-number v-model="search_form.min_price" :min="0" :precision="2" placeholder="最低价" style="width: 110px" />
              <span style="margin: 0 10px">-</span>
              <el-input-number v-model="search_form.max_price" :min="0" :precision="2" placeholder="最高价" style="width: 110px" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="评分">
              <el-rate v-model="search_form.rating" clearable allow-half style="margin-top: 8px" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24" style="text-align: center">
            <el-button type="primary" @click="handle_search" :icon="Search">查询</el-button>
            <el-button @click="handle_reset" :icon="Refresh">重置</el-button>
            <el-button type="success" @click="handle_add" :icon="Plus">新增</el-button>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 数据列表 -->
    <el-card class="table-card">
      <el-table :data="items" v-loading="loading" border stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center" fixed />
        <el-table-column prop="name" label="景点名称" width="200" show-overflow-tooltip fixed />
        <el-table-column prop="address" label="地址" width="250" show-overflow-tooltip />
        <el-table-column prop="price" label="价格" width="120" align="center">
          <template #default="{ row }">
            <span style="color: #f56c6c; font-weight: bold">¥{{ row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="original_price" label="原价" width="120" align="center">
          <template #default="{ row }">
            <span style="text-decoration: line-through; color: #909399">¥{{ row.original_price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="rating" label="评分" width="150" align="center">
          <template #default="{ row }">
            <el-rate v-model="row.rating" disabled show-score text-color="#ff9900" />
          </template>
        </el-table-column>
        <el-table-column prop="open_time" label="开放时间" width="150" align="center" />
        <el-table-column label="图片" width="100" align="center">
          <template #default="{ row }">
            <el-image v-if="row.images" :src="row.images.split(',')[0]" fit="cover" style="width: 60px; height: 60px; border-radius: 4px" />
            <span v-else style="color: #909399">暂无</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="transport" label="交通信息" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180" align="center" />
        <el-table-column prop="updated_at" label="更新时间" width="180" align="center" />
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handle_edit(row)" :icon="Edit" :loading="row.is_saving">编辑</el-button>
            <el-button type="danger" size="small" @click="handle_delete(row)" :icon="Delete" :loading="row.is_deleting">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          background
          @size-change="handle_size_change"
          @current-change="handle_current_change"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialog_visible" :title="dialog_title" width="800px" top="5vh" :close-on-click-modal="false" @close="reset_form">
      <el-form :model="form" :rules="rules" ref="form_ref" label-width="100px" label-suffix=":">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="景点名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入景点名称" maxlength="200" show-word-limit />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="开放时间" prop="open_time">
              <el-input v-model="form.open_time" placeholder="例：08:00-18:00" maxlength="100" show-word-limit />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="价格" prop="price">
              <el-input-number v-model="form.price" :min="0" :precision="2" style="width: 100%" placeholder="请输入价格" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="原价" prop="original_price">
              <el-input-number v-model="form.original_price" :min="0" :precision="2" style="width: 100%" placeholder="请输入原价" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="评分" prop="rating">
              <el-rate v-model="form.rating" allow-half show-text style="margin-top: 8px" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="图片地址" prop="images">
              <el-input v-model="form.images" placeholder="多个图片用逗号分隔" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="详细地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入详细地址" maxlength="300" show-word-limit />
        </el-form-item>

        <el-form-item label="交通信息" prop="transport">
          <el-input v-model="form.transport" type="textarea" :rows="2" placeholder="请输入交通信息" maxlength="300" show-word-limit />
        </el-form-item>

        <el-form-item label="景点描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请输入景点描述" maxlength="500" show-word-limit />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialog_visible = false">取消</el-button>
          <el-button type="primary" @click="handle_save" :loading="save_loading">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh, Plus, Edit, Delete } from '@element-plus/icons-vue'

// ==================== 模拟数据配置 ====================
const mock_scenic_data = [
  {
    id: 1,
    name: '西湖风景区',
    description: '杭州西湖是中国著名的风景名胜区，以秀丽的湖光山色和众多的名胜古迹闻名中外。',
    address: '浙江省杭州市西湖区龙井路1号',
    price: 0,
    original_price: 0,
    rating: 4.8,
    images: 'https://example.com/westlake1.jpg,https://example.com/westlake2.jpg',
    open_time: '全天开放',
    transport: '地铁1号线至龙翔桥站，公交7路、27路等',
    created_at: '2025-11-11 10:00:00',
    updated_at: '2025-11-11 10:00:00'
  },
  {
    id: 2,
    name: '黄山风景区',
    description: '黄山位于安徽省南部，是中国十大名山之一，以奇松、怪石、云海、温泉四绝著称。',
    address: '安徽省黄山市黄山区汤口镇',
    price: 190,
    original_price: 230,
    rating: 4.9,
    images: 'https://example.com/huangshan1.jpg',
    open_time: '06:00-17:30',
    transport: '可乘飞机至屯溪机场，或高铁至黄山北站，再转乘旅游专线',
    created_at: '2025-11-10 14:30:00',
    updated_at: '2025-11-10 14:30:00'
  },
  {
    id: 3,
    name: '张家界国家森林公园',
    description: '张家界是中国第一个国家森林公园，以独特的石英砂岩峰林地貌著称，是世界自然遗产。',
    address: '湖南省张家界市武陵源区',
    price: 225,
    original_price: 248,
    rating: 4.7,
    images: 'https://example.com/zjj1.jpg,https://example.com/zjj2.jpg,https://example.com/zjj3.jpg',
    open_time: '07:00-18:00',
    transport: '张家界荷花机场，或火车至张家界站，再转乘景区巴士',
    created_at: '2025-11-09 09:15:00',
    updated_at: '2025-11-09 09:15:00'
  },
  {
    id: 4,
    name: '九寨沟风景名胜区',
    description: '九寨沟位于四川省阿坝藏族羌族自治州，以翠海、叠瀑、彩林、雪峰、藏情、蓝冰六绝著称。',
    address: '四川省阿坝藏族羌族自治州九寨沟县',
    price: 169,
    original_price: 220,
    rating: 4.9,
    images: 'https://example.com/jiuzhaigou1.jpg',
    open_time: '08:00-17:00',
    transport: '可乘飞机至九黄机场，或从成都乘坐长途汽车',
    created_at: '2025-11-08 16:45:00',
    updated_at: '2025-11-08 16:45:00'
  },
  {
    id: 5,
    name: '故宫博物院',
    description: '北京故宫是中国明清两代的皇家宫殿，旧称紫禁城，位于北京中轴线的中心。',
    address: '北京市东城区景山前街4号',
    price: 60,
    original_price: 80,
    rating: 4.8,
    images: 'https://example.com/forbidden_city1.jpg,https://example.com/forbidden_city2.jpg',
    open_time: '08:30-17:00（周一闭馆）',
    transport: '地铁1号线天安门东或天安门西站，公交1、2、52路等',
    created_at: '2025-11-07 11:20:00',
    updated_at: '2025-11-07 11:20:00'
  }
]

// ==================== API 请求模拟 ====================
const request = {
  post: async (url, data) => {
    console.log('请求地址:', url, '请求参数:', data)
    await new Promise(resolve => setTimeout(resolve, 300)) // 模拟网络延迟

    // 统一响应结构
    const successResponse = (data) => ({
      data: {
        code: 200,
        msg: 'success',
        data: data
      }
    })

    const errorResponse = (msg) => ({
      data: {
        code: 500,
        msg: msg,
        data: null
      }
    })

    try {
      switch (url) {
        case '/get_scenic_list': {
          const { page, page_size, name, address, min_price, max_price, rating } = data
          
          // 模拟数据过滤
          let filtered = mock_scenic_data.filter(item => {
            const matchName = !name || item.name.toLowerCase().includes(name.toLowerCase())
            const matchAddress = !address || item.address.toLowerCase().includes(address.toLowerCase())
            const matchMinPrice = item.price >= (min_price || 0)
            const matchMaxPrice = item.price <= (max_price || 999999)
            const matchRating = item.rating >= (rating || 0)
            return matchName && matchAddress && matchMinPrice && matchMaxPrice && matchRating
          })

          const start = (page - 1) * page_size
          const end = start + page_size
          const list = filtered.slice(start, end)

          return successResponse({
            list: list,
            total_records: filtered.length
          })
        }

        case '/add_scenic': {
          const newItem = {
            ...data,
            id: mock_scenic_data.length + 1,
            created_at: new Date().toLocaleString('zh-CN'),
            updated_at: new Date().toLocaleString('zh-CN')
          }
          mock_scenic_data.push(newItem)
          return successResponse({ id: newItem.id })
        }

        case '/update_scenic': {
          const index = mock_scenic_data.findIndex(item => item.id === data.id)
          if (index !== -1) {
            mock_scenic_data[index] = {
              ...data,
              updated_at: new Date().toLocaleString('zh-CN')
            }
            return successResponse({})
          }
          return errorResponse('记录不存在')
        }

        case '/delete_scenic': {
          const index = mock_scenic_data.findIndex(item => item.id === data.id)
          if (index !== -1) {
            mock_scenic_data.splice(index, 1)
            return successResponse({})
          }
          return errorResponse('记录不存在')
        }

        default:
          return errorResponse('未知接口')
      }
    } catch (error) {
      console.error('模拟API错误:', error)
      return errorResponse('服务器错误: ' + error.message)
    }
  }
}

// ==================== 响应式数据 ====================
const loading = ref(false)
const save_loading = ref(false)
const delete_loading = ref(false)
const items = ref([])
const total = ref(0)
const page = ref(1)
const page_size = ref(10)
const dialog_visible = ref(false)
const dialog_title = ref('新增景点')
const form_ref = ref(null)

// 查询表单
const search_form = reactive({
  name: '',
  address: '',
  min_price: null,
  max_price: null,
  rating: null
})

// 表单数据
const form = reactive({
  id: null,
  name: '',
  description: '',
  address: '',
  price: 0,
  original_price: 0,
  rating: 0,
  images: '',
  open_time: '',
  transport: '',
  created_at: '',
  updated_at: ''
})

// 表单验证规则
const rules = {
  name: [{ required: true, message: '请输入景点名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  original_price: [{ required: true, message: '请输入原价', trigger: 'blur' }],
  address: [{ required: true, message: '请输入详细地址', trigger: 'blur' }]
}

// ==================== 业务逻辑 ====================
const load_data = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: page_size.value,
      name: search_form.name || '',
      address: search_form.address || '',
      min_price: search_form.min_price || 0,
      max_price: search_form.max_price || 999999,
      rating: search_form.rating || 0
    }
    const res = await request.post('/get_scenic_list', params)
    
    // 防御性解构，避免 undefined 错误
    const responseData = res?.data
    if (responseData?.code === 200 && responseData?.data) {
      items.value = responseData.data.list || []
      total.value = responseData.data.total_records || 0
    } else {
      items.value = []
      total.value = 0
      ElMessage.error(responseData?.msg || '加载数据失败')
    }
  } catch (error) {
    console.error('加载异常:', error)
    ElMessage.error('网络请求失败')
    items.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

const handle_search = () => {
  page.value = 1
  load_data()
}

const handle_reset = () => {
  search_form.name = ''
  search_form.address = ''
  search_form.min_price = null
  search_form.max_price = null
  search_form.rating = null
  handle_search()
}

const handle_add = () => {
  dialog_title.value = '新增景点'
  reset_form_data()
  dialog_visible.value = true
}

const handle_edit = (row) => {
  dialog_title.value = '编辑景点'
  // 深拷贝数据到表单
  Object.keys(form).forEach(key => {
    form[key] = row[key] !== null && row[key] !== undefined ? row[key] : ''
  })
  dialog_visible.value = true
}

const handle_delete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该景点信息吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    delete_loading.value = true
    const res = await request.post('/delete_scenic', { id: row.id })
    
    if (res?.data?.code === 200) {
      ElMessage.success('删除成功')
      // 如果删除的是当前页最后一条，返回上一页
      if (items.value.length === 1 && page.value > 1) {
        page.value--
      }
      load_data()
    } else {
      ElMessage.error(res?.data?.msg || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除异常')
      console.error(error)
    }
  } finally {
    delete_loading.value = false
  }
}

const handle_save = async () => {
  if (!form_ref.value) {
    ElMessage.error('表单未初始化')
    return
  }

  try {
    // 使用 Promise 验证，避免回调参数 undefined
    await form_ref.value.validate()
    
    save_loading.value = true
    const url = form.id ? '/update_scenic' : '/add_scenic'
    const res = await request.post(url, form)
    
    if (res?.data?.code === 200) {
      ElMessage.success(form.id ? '更新成功' : '新增成功')
      dialog_visible.value = false
      load_data()
    } else {
      ElMessage.error(res?.data?.msg || '操作失败')
    }
  } catch (error) {
    // 验证失败会走到这里
    if (error === false) {
      console.log('表单验证未通过')
    } else {
      ElMessage.error('操作异常')
      console.error(error)
    }
  } finally {
    save_loading.value = false
  }
}

// 重置表单数据
const reset_form_data = () => {
  Object.keys(form).forEach(key => {
    if (key === 'id') form[key] = null
    else if (key === 'price' || key === 'original_price') form[key] = 0
    else if (key === 'rating') form[key] = 3.5 // 给一个默认值
    else form[key] = ''
  })
}

// 重置表单验证
const reset_form = () => {
  if (form_ref.value) {
    form_ref.value.resetFields()
  }
  reset_form_data()
}

const handle_size_change = (val) => {
  page_size.value = val
  load_data()
}

const handle_current_change = (val) => {
  page.value = val
  load_data()
}

// 页面加载时获取数据
onMounted(() => {
  load_data()
})
</script>

<style scoped>
.scenic-container {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7f1 100%);
  min-height: calc(100vh - 40px);
}

.search-card {
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.table-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding: 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.el-form-item) {
  margin-bottom: 22px;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background-color: #f8f9fb;
  font-weight: 600;
  color: #303133;
}

:deep(.el-button--small) {
  padding: 5px 10px;
}
</style>
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import request from '@/utils/request'
import { ElMessageBox } from 'element-plus';
import { ElMessage } from 'element-plus';
import { useRoute, useRouter } from 'vue-router'

import { baseURL } from '@/utils/request'

import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const imageUrl = ref('')

const dialogVisible = ref(false)
const formModel = ref({

    registerid: "",
    feeid: "",
    feetype: "",
    feename: "",
    price: "",
    num: "",
    fee: "",

})

//定义请求参数
const params = ref({
    page: 1,
    pagesize: 30,
    registerid: "",
    


})
const total = ref(0)
const Edit = 'el-icon-edit'

const handleAdd = () => {
    console.log('handleAdd')
    formModel.value = {}

    dialogVisible.value = true
}

const items = ref([])

const getItmes = () => {


    params.value.registerid = register_id.value
    console.log('params', params.value)

    request.post('/register/chargeindex', params.value).then(res => {
        console.log('res', res.data.data.workers.data)
        items.value = res.data.data.workers.data
        total.value = res.data.data.workers.total
    })
}

const handleEdit = (row) => {
    console.log('handleEdit', row)
    formModel.value = row
    imageUrl.value = baseURL + "/" + row.doc_img
    dialogVisible.value = true
}

const handleDelete = (index) => {

    ElMessageBox.confirm('确认删除该条记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        console.log('confirm')

        console.log('handleDelete', index)
        const id = items.value[index].id
        request.post('/register/delcharge', { id: id }).then(res => {
            if (res.data.errorcode === 0) {
                items.value.splice(index, 1)
            }else
            {
                ElMessage.error('删除失败'+res.data.message)
            }
        })


    }).catch(() => {
        console.log('cancel')
    })


}

const handleSave = () => {
    console.log('handleSave')

    request.post('/register/edit', formModel.value).then(res => {
        if (res.data.errorcode === 0) {
            dialogVisible.value = false
            getItmes()
        }
    })

}




// 分页事件处理
const handleSizeChange = (size) => {
    params.value.page = 1
    params.value.pagesize = size
    getItmes()
}

const handleCurrentChange = (page) => {
    params.value.page = page
    getItmes()
}

const register_id = ref('')

onMounted(() => {

    const id = route.params.id;
    console.log(id, 'order_id')
    register_id.value = id
    getItmes()
    getCharges()

})




//查询 现在是添加收费
const onQuery = () => {

  if (formModel.value.num==0||formModel.value.num==''||formModel.value.num==null) {
      ElMessage.warning('请输入数量')
      return
  }
  formModel.value.registerid = register_id.value
  formModel.value.fee = formModel.value.num * formModel.value.price
  request.post('/register/charge', formModel.value).then(res => {
      if (res.data.errorcode === 0) {
          ElMessage.success('添加成功')
          searchText.value = ''
          formModel.value = {}
          getItmes()
      }
  })
}


//获取select的参数值
const type_zj = ref([])
const type_ys = ref([])
const type_ks = ref([])
const type_zflx = ref([])

const getZfSelect = () => {
    request.post('/index/dicttypelist', { 'type': '证件类型,科室,医生,支付类型' }).then(res => {
        if (res.data.errorcode === 0) {
            type_zj.value = res.data.data.filter(item => item.type === '证件类型')
            type_ys.value = res.data.data.filter(item => item.type === '医生')
            type_ks.value = res.data.data.filter(item => item.type === '科室')
            type_zflx.value = res.data.data.filter(item => item.type === '支付类型')
        }
    })
}

//门诊收费
const handle_Detail = (row) => {
    router.push({ path: '/register/detail', query: { id: row.id } })
}

//收费项目
const charges = ref([])
const getCharges = async () => {

    let res = await request.post('/register/getchageranddrugs')
    console.log(res.data.data, "收费项目")
    let drug = res.data.data.drugs
    let charge = res.data.data.charge
    charges.value = [...drug.map(item => ({ ...item, type: '药品' })),
    ...charge.map(item => ({ ...item, type: '收费项目' }))];
    console.log(charges.value, "收费项目")
}

//收费项目输入
const searchText = ref('');


const querySearch = (queryString, cb) => {
    const results = queryString
        ? charges.value.filter(createFilter(queryString))
        : charges.value;
    // 调用 callback 返回建议列表
    cb(results);
};

const createFilter = (queryString) => {
    return (candidate) => {
        return (

            candidate.pym.toLowerCase().includes(queryString.toLowerCase())
        );
    };
};

const currCharge = ref({})

const handleSelect = (item) => {
    console.log('选中项:', item.value);
    let ds = item.value.split('-')
    console.log(ds[1], "药品name")
    let rs = charges.value.filter(item => item.code == ds[1])
  
    currCharge.value = rs[0]

    //判断库存

    formModel.value.registerid= register_id.value
    formModel.value.feeid = currCharge.value.id 
    formModel.value.feename  = currCharge.value.name
    formModel.value.price = currCharge.value.price
    formModel.value.feetype = currCharge.value.type
      console.log(currCharge.value, "药品信息-价格")
      numInput.value?.focus()




};

const getStock= async(id,num) => {
     let results = await request.get("/register/getStockbyId?id=" + id+"&num="+num)
     if(results.data.errorcode !=0) {
         ElMessage.error("库存不足")
         return false
     }else
     {
         return true
     }
     
   
}


function getSummaries(param) {
  const { columns, data } = param;
  const sums = [];
  columns.forEach((column, index) => {
    if (index === 0) {
      sums[index] = '合计';
      return;
    }
    const values = data.map(item => Number(item[column.property]));
    // 只合计特定的列，例如这里我们只合计amount1和amount3
    if (column.property === 'num' || column.property === 'fee') {
      sums[index] = values.reduce((prev, curr) => {
        const value = Number(curr);
        if (!isNaN(value)) {
          return prev + value;
        } else {
          return prev;
        }
      }, 0).toFixed(2);
    } else {
      sums[index] = ''; // 不进行合计的列留空
    }
  });
  return sums;
}


const numInput = ref(null);

const handleEnter = (event) => {
 
  console.log(event, "数量")
  request.post("/register/getStockbyId", {'id':currCharge.value.id,'num':formModel.value.num}).then(res => {
    if(res.data.errorcode !=0) {
        if(res.data.data==null)
        {
          ElMessage.error("库存不足,库存数量是:0")
          return false
            }
      ElMessage.error("库存不足,库存数量是:"+res.data.data.num)
      return false
    }else{
     
      onQuery()
    }

  })






};

const saveall = async() => {
  console.log("保存全部")
   let res = await request.post("/register/saveall", {'id':register_id.value })
   if(res.data.errorcode==0){
     ElMessage.success("保存成功")
   }else{
     ElMessage.error("保存失败"+res.data.message)
   }
};



// 发票打印
const fpPrint = () => {
  console.log("发票打印")
  var fee=0;
  for (let i = 0; i < items.value.length; i++) {
    fee = fee + items.value[i].fee;
  }
  console.log(fee, "总金额")
  router.push({ path: '/register/fpprint/'+register_id.value });
//   router.push({ path: '/register/charge/'+row.id})
};







</script>

<template>
    <page-container :title="doc_header">
        <template #extra>
            <el-button type="primary" @click="handleAdd">添加</el-button>
        </template>
        <h2>门诊收费</h2>

        <div class="form-query">
            <el-form :inline="true" :model="params" class="demo-form-inline">
                <el-form-item label="收费项目/药品">
                    <el-autocomplete v-model="searchText" :fetch-suggestions="querySearch" placeholder="请输入内容"
                        @select="handleSelect"></el-autocomplete>
                </el-form-item>
                <el-form-item label="数量">
                    <el-input v-model="formModel.num" ref="numInput" placeholder="请输入数量"  @keyup.enter.native="handleEnter"></el-input>
                </el-form-item>



                <el-form-item>
                    <!-- <el-button type="primary" @click="onQuery">继续添加</el-button> -->
                    <el-button type="success" @click="saveall"  style="margin-left: 300px;">保存确认</el-button>
                    <el-button type="success"  @click="fpPrint"   style="margin-left: 300px;">发票打印</el-button>
                </el-form-item>
            </el-form>
        </div>


        <el-table :data="items" style="width: 100%"  border show-summary  sum-text="合计" :summary-method="getSummaries">
            <!-- <el-table-column prop="id" label="id"></el-table-column>
            <el-table-column prop="registerid" label="门诊id"></el-table-column> -->
            <el-table-column prop="feeid" label="费用id"></el-table-column>
            <el-table-column prop="feetype" label="费用类型"></el-table-column>
            <el-table-column prop="feename" label="费用名称"></el-table-column>
            <el-table-column prop="price" label="单价"></el-table-column>
            <el-table-column prop="num" label="数量"></el-table-column>
            <el-table-column prop="fee" label="费用"></el-table-column>
            <el-table-column label="操作" width="320">
                <template #default="scope">

                    <el-button :icon="Delete" type="danger" @click="handleDelete(scope.$index)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <!--分页-->
        <el-pagination v-model:current-page="params.page" v-model:page-size="params.pagesize"
            :page-sizes="[2, 20, 50, 100]" :background="true" layout="jumper,total, sizes, prev, pager, next"
            :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange"
            style="margin-top: 20px;justify-content: flex-end;" />
        <el-dialog v-model="dialogVisible" title="新增" width="30%">
            <el-form :model="formModel" ref="form" label-width="120px">

                <el-form-item label="姓名">
                    <el-input v-model="formModel.name"></el-input>
                </el-form-item>
                <el-form-item label="年龄">
                    <el-input v-model="formModel.age"></el-input>
                </el-form-item>
                <el-form-item label="性别">
                    <!-- <el-input v-model="formModel.sex"></el-input> -->
                    <el-select v-model="formModel.sex" placeholder="选择" size="large" style="width: 240px">
                        <el-option label="男" value="男" />
                        <el-option label="女" value="女" />

                    </el-select>
                </el-form-item>
                <el-form-item label="证件号">
                    <el-input v-model="formModel.cardid"></el-input>
                </el-form-item>
                <el-form-item label="证件类型">
                    <!-- <el-input v-model="formModel.cardtype"></el-input> -->
                    <el-select v-model="formModel.cardtype" placeholder="选择" size="large" style="width: 240px">
                        <el-option v-for="item in type_zj" :key="item.value" :label="item.value" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="医生">
                    <!-- <el-input v-model="formModel.doctor"></el-input> -->
                    <el-select v-model="formModel.doctor" placeholder="选择" size="large" style="width: 240px">
                        <el-option v-for="item in type_ys" :key="item.value" :label="item.value" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="状态">
                    <el-input v-model="formModel.status"></el-input>
                </el-form-item>
                <el-form-item label="就诊次数">
                    <el-input v-model="formModel.jzcs"></el-input>
                </el-form-item>
                <el-form-item label="手机号">
                    <el-input v-model="formModel.mobile"></el-input>
                </el-form-item>
                <el-form-item label="支付类型">
                    <!-- <el-input v-model="formModel.paytype"></el-input> -->
                    <el-select v-model="formModel.paytype" placeholder="选择" size="large" style="width: 240px">
                        <el-option v-for="item in type_zflx" :key="item.value" :label="item.value"
                            :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="地址">
                    <el-input v-model="formModel.address"></el-input>
                </el-form-item>
                <el-form-item label="科室">
                    <!-- <el-input v-model="formModel.ksname"></el-input> -->
                    <el-select v-model="formModel.ksname" placeholder="选择" size="large" style="width: 240px">
                        <el-option v-for="item in type_ks" :key="item.value" :label="item.value" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="病史">
                    <el-input v-model="formModel.bs"></el-input>
                </el-form-item>



            </el-form>
            <template #footer>

                <div class="dialog-footer">


                    <el-button type="primary" @click="handleSave">
                        保存
                    </el-button>
                    <el-button @click="dialogVisible = false" type="danger">取消</el-button>
                </div>
            </template>
        </el-dialog>
    </page-container>

</template>

<style scoped>
.avatar {
    width: 178px;
    height: 178px;
    display: block;
    margin-left: 120px;
}

.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
}
</style>

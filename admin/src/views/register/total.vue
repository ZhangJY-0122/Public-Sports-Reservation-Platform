<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import request from '@/utils/request'
import { ElMessageBox } from 'element-plus';
import { ElMessage } from 'element-plus';
import { useRoute, useRouter } from 'vue-router'

import { baseURL } from '@/utils/request'
import { changeDate } from '@/utils/helper'
import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const imageUrl = ref('')

const dialogVisible = ref(false)
const formModel = ref({
    id: "",
    name: "",
    age: "",
    sex: "",
    cardid: "",
    cardtype: "",
    doctor: "",
    status: "",
    jzcs: "",
    mobile: "",
    paytype: "",
    address: "",
    ksname: "",
    bs: "",

})

//定义请求参数
const params = ref({
    create_time: "",


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




    request.post('/register/total', params.value).then(res => {
        console.log('res', res.data)
        items.value = res.data.data
      
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
        request.post('/admin/worker_del', { id: id }).then(res => {
            if (res.data.code === 0) {
                items.value.splice(index, 1)
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


onMounted(() => {


    getItmes()
    getZfSelect()

})


const create_time = ref('')

//查询
const onQuery = () => {
    if (create_time.value) {
        params.value.create_time = changeDate(create_time.value[0]) + " | " + changeDate(create_time.value[1])
    }
    getItmes()

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
    router.push({ path: '/register/charge/' + row.id })
}













</script>

<template>
    <page-container :title="doc_header">
        <template #extra>
            <el-button type="primary" @click="handleAdd">添加</el-button>
        </template>
        <h2>收费统计</h2>
        <div class="form-query">
            <el-form :inline="true" :model="params" class="demo-form-inline">
                <el-form-item label="时间">
                    <!-- <el-input v-model="params.create_time"></el-input> -->
                    <el-date-picker v-model="create_time" type="daterange" range-separator="To"
                        start-placeholder="Start date" end-placeholder="End date" :size="size" />
                </el-form-item>
                


                <el-form-item>
                    <el-button type="primary" @click="onQuery">查询</el-button>
                </el-form-item>
            </el-form>
        </div>


        <el-table :data="items" border show-summary style="width: 100%" sum-text="合计" >
            <!-- <el-table-column prop="id" label="id"></el-table-column> -->
            <el-table-column prop="feetype" label="收费类型"></el-table-column>
            <el-table-column prop="zs" label="总数"></el-table-column>
            <el-table-column prop="money" label="总金额"></el-table-column>
    
           
        </el-table>
       
     
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

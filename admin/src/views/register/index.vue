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
    page: 1,
    pagesize: 10,
    name: "",
    pym: "",
    code: "",


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




    request.post('/register/index', params.value).then(res => {
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




//查询
const onQuery = () => {
 
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
    router.push({ path: '/register/charge/'+row.id})
}













</script>

<template>
    <page-container :title="doc_header">
        <template #extra>
            <el-button type="primary" @click="handleAdd">添加</el-button>
        </template>

        <div class="form-query">
            <el-form :inline="true" :model="params" class="demo-form-inline">
                <el-form-item label="姓名">
                    <el-input v-model="params.name"></el-input>
                </el-form-item>
                <el-form-item label="医生">
                    <el-input v-model="params.doctor"></el-input>
                </el-form-item>
                <el-form-item label="状态">
                    <el-input v-model="params.status"></el-input>
                </el-form-item>
                <el-form-item label="手机号">
                    <el-input v-model="params.mobile"></el-input>
                </el-form-item>
                <el-form-item label="科室">
                    <el-input v-model="params.ksname"></el-input>
                </el-form-item>


                <el-form-item>
                    <el-button type="primary" @click="onQuery">查询</el-button>
                </el-form-item>
            </el-form>
        </div>


        <el-table :data="items" style="width: 100%">
            <el-table-column prop="id" label="id"></el-table-column>
            <el-table-column prop="name" label="姓名"></el-table-column>
            <el-table-column prop="age" label="年龄"></el-table-column>
            <el-table-column prop="sex" label="性别"></el-table-column>
            <el-table-column prop="cardid" label="证件号"></el-table-column>
            <el-table-column prop="cardtype" label="证件类型"></el-table-column>
            <el-table-column prop="doctor" label="医生"></el-table-column>
            <el-table-column prop="status" label="状态"></el-table-column>
            <el-table-column prop="jzcs" label="就诊次数"></el-table-column>
            <el-table-column prop="mobile" label="手机号"></el-table-column>
            <el-table-column prop="paytype" label="支付类型"></el-table-column>
            <el-table-column prop="address" label="地址"></el-table-column>
            <el-table-column prop="ksname" label="科室"></el-table-column>
            <el-table-column prop="bs" label="病史"></el-table-column>
            <el-table-column label="操作" width="320">
                <template #default="scope">
                    <el-button :icon="Edit" type="primary" @click="handle_Detail(scope.row)">门诊收费</el-button>
                    <el-button :icon="Edit" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
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
                        <el-option v-for="item in type_zflx" :key="item.value" :label="item.value" :value="item.value" />
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

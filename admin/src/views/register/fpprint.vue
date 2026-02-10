<script setup>

import { ref, onMounted ,reactive} from 'vue'
import request from '@/utils/request'
import { convertToChineseCurrency } from '@/utils/helper'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const register_data = ref("")
const register_detail = ref([])
const currFee=ref(0)
const getRegister = (id) => {
    request.get('/register/printdata?id=' + id).then(res => {
        console.log(res.data.data, "register_data")
        register_data.value = res.data.data.reg_main
        let _ds = res.data.data.reg_det
        let _datas = []
        for (let i = 0; i < _ds.length; i++) {
            let _item = {
                feename: _ds[i].feename,
                ypgg: _ds[i].xsdw + "/" + _ds[i].ypgg,
                fee: _ds[i].fee
            }
            currFee.value += _ds[i].fee
            _datas.push(_item)
        }
        register_detail.value = _datas
        orderfee.cn=convertToChineseCurrency(currFee.value)
        orderfee.num=currFee.value.toFixed(2)

    })
}

const orderfee=reactive({
    cn:"",
    num:0
})

const currday=reactive({
    year: 0,
    month: 0,
    day: 0
})


const getCurrentDate = () => {
    const now = new Date();
    currday.year = now.getFullYear();
    currday.month = now.getMonth() + 1; // 月份从0开始，所以需要加1
    currday.day = now.getDate();
};

onMounted(() => {
    let id = route.params.id

    console.log(id, "id")


    

    getRegister(id)

    getCurrentDate();


})

const testDB = () => {
    register_data.value = {
        name: "张三",
        sex: "男"
    }

    let testlits = [
        {
            id: 1,
            feename: "挂号费",
            ypgg: "瓶/500ml*2",
            fee: 100.00
        },
        {
            id: 2,
            feename: "检查费",
            ypgg: "支/0.25mg*10",
            fee: 50.00
        },
        {
            id: 3,
            feename: "检查费",
            ypgg: "盒/1*10片",
            fee: 100.00
        },
        {
            id: 3,
            feename: "检查费",
            ypgg: "盒/1*10片",
            fee: 100.00
        },
        {
            id: 3,
            feename: "检查费",
            ypgg: "盒/1*10片",
            fee: 100.00
        },
        {
            id: 3,
            feename: "检查费",
            ypgg: "盒/1*10片",
            fee: 100.00
        },
        {
            id: 3,
            feename: "检查费",
            ypgg: "盒/1*10片",
            fee: 100.00
        },
        {
            id: 3,
            feename: "检查费",
            ypgg: "盒/1*10片",
            fee: 100.00
        },
        {
            id: 3,
            feename: "检查费",
            ypgg: "盒/1*10片",
            fee: 100.00
        },
        {
            id: 3,
            feename: "检查费",
            ypgg: "盒/1*10片",
            fee: 100.00
        },
        {
            id: 3,
            feename: "检查费",
            ypgg: "盒/1*10片",
            fee: 100.00
        },
    ]

    register_detail.value = testlits
}



</script>
<template>
    <div class="print-btns">
        <el-button type="primary" v-print="'#printArea'">打印</el-button>
        <el-button type="warning" @click="testDB">测试数据</el-button>
    </div>
    <div id="printArea">
        <div>
            <p> <span>{{ register_data.name }}</span><span>{{ register_data.sex }}</span></p>
        </div>
        <div class="table-container">
            <!-- <ul style="list-style: none;">
                <li v-for="item in register_detail" :key="item.id"><span>{{ item.feename }}</span><span>{{ item.ypgg }}</span><span>{{ item.fee.toFixed(2) }}</span></li>

            </ul> -->

            <table style="width: 600px;margin-left: 30px;margin-top: 20px;font-size: 12px;height:auto">

                <tr v-for="item in register_detail" :key="item.id">
                    <td style="width: 80px;">{{ item.feename }}</td>
                    <td style="width: 30px;">{{ item.ypgg }}</td>
                    <td style="width: 30px;">{{ item.fee.toFixed(2) }}</td>
                </tr>
            </table>

        </div>

        <div class="fee">
            <!-- <span class="zje">五百三十二员</span> <span class="zje-num">532</span> -->
            <p>{{ orderfee.cn }} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ orderfee.num}} </p>
        </div>
        <div class="date">
          <p>{{currday.year}}  {{currday.month}}  {{currday.day}}  </p>
        </div>


    </div>

</template>
<style scoped>
p span {
    display: inline-block;
    width: 100px;
    height: 30px;
    line-height: 30px;
    text-align: center;
    margin-right: 32px;
    font-size: 14px;
}

li span {
    display: inline-block;

    height: 30px;
    line-height: 30px;
    text-align: center;
    margin-right: 50px;

}

.print-btns {
    margin: 60px;
    margin-top: 200px;
}

.zje {
    margin-left: 30px;
    font-size: 14px;


}

.zje-num {
    margin-left: 400px;
    font-size: 14px;

}

.time {
    margin-left: 250px;
    font-size: 14px;
}

.fee {
    position: fixed;
    top: 47%;
    left: 57%;
    transform: translate(-120%, -200%);
    width: 300px;
    height: 100px;
    background-color: #f1f1f1;


    
}
.date{
    position: fixed;
    top: 36%;
    left: 59%;
    transform: translate(-20%, -50%);
    width: 200px;
    height: 100px;
    background-color: #f1f1f1;
}
</style>
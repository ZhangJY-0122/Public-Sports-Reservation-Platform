<script setup>
import { ref, onMounted } from 'vue'
import request from '@/utils/request'
import {baseURL} from '@/utils/request'
import * as echarts from 'echarts'
const workers = ref(0)
const bussiness = ref(0)
const checks = ref(0)

const chartContainer1 = ref(null);
const chartContainer2 = ref(null);




const getData = async () => {
  const res = await request.get('/admin/home')
  console.log(res.data,"res.data")
  workers.value = res.data.data.workers
  bussiness.value = res.data.data.bussiness
  checks.value = res.data.data.checks
 
}



onMounted(() => {

getData()


 



})

</script>
<template>
  <el-row>
    <el-col :span="8">


      <el-card shadow="never">
        <img src="/src/assets/1.png" alt="图片" style="width: 100px; height: 100px;">
        <span>用户数量：{{ workers }}</span>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card shadow="never">
        <img src="/src/assets/2.png" alt="图片" style="width: 100px; height: 100px;">
        <span>文章：{{ bussiness }}</span>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card shadow="never">
        <img src="/src/assets/3.png" alt="图片" style="width: 100px; height: 100px;">
        <span>货物数量：{{ checks }}</span>
      </el-card></el-col>
  </el-row>
<!-- 
  <el-row  v-if="false" <uni-search-bar
    v-model=""
    @confirm="" >
    <el-col :span="8">

      <div ref="chartContainer1" style="width: 600px;height:400px;"></div>
    </el-col>
    <el-col :span="8">

      <div ref="chartContainer2" style="width: 600px;height:400px;"></div>
    </el-col>

  </el-row> -->


  <el-row>
    <el-divider />

     服务器域名:{{ baseURL }}
  </el-row>

</template>
<style scoped>
.el-card {
  width: 300px;
  height: 180px;
  margin: 50px;

  text-align: center;
  line-height: 180px;
  font-size: 22px;
  color: #060000;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-row {
  margin-bottom: 20px;
}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #d3dce6;


}
</style>
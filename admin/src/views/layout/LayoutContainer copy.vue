<template>

  <!--el-menu 整个菜单组件
        :default-active="$route.path"
        router
        配置默认高亮的菜单项
        router选项开启，ellmenu-item的index就是点击跳转的路径
    -->
  <el-container class="layout-container-demo" style="height: 95vh">
    <el-aside width="200px" height="100vh">
      <el-scrollbar>
        <el-menu active-text-color="#ffd04b" background-color="#545c64" class="el-menu-vertical-demo" default-active="2"
          text-color="#fff" @open="handleOpen" @close="handleClose" router>
          <el-sub-menu index="1">
            <template #title>
              <el-icon>
                <House />
              </el-icon><router-link to="/common/index" style="color: #fff; font-size: 16px">首页</router-link>
            </template>

          </el-sub-menu>

          <el-sub-menu index="1">
            <template #title>
              <el-icon>
                <location />
              </el-icon>
              <span>基础资料</span>
            </template>

            <el-menu-item index="/register/index"  >门诊挂号</el-menu-item>
            <el-menu-item index="/register/chargedetail" >门诊收费明细</el-menu-item>
            <el-menu-item index="/register/total" >门诊汇总统计</el-menu-item>
 
          


          </el-sub-menu>
          <el-sub-menu index="2" >
            <template #title>
              <el-icon>
                <location />
              </el-icon>
              <span>权限管理</span>
            </template>
            <el-menu-item index="/user/list">用户管理</el-menu-item>
            <el-menu-item index="/user/rolelist">角色管理</el-menu-item>
            <el-menu-item index="/user/menulist">菜单管理</el-menu-item>
            <!-- <el-menu-item index="/docs/list/4">常见问题</el-menu-item> -->
            <!-- <el-menu-item index="/orders/list">订单明细表</el-menu-item> -->


          </el-sub-menu>
          <el-sub-menu index="3" v-if="userStore.userInfo.roleid == 1">
            <template #title>
              <el-icon>
                <location />
              </el-icon>
              <span>系统管理</span>
            </template>
            <el-menu-item index="/system/init">数据初始化</el-menu-item>
            <el-menu-item index="/dict/index">字典管理</el-menu-item>

            <!-- <el-menu-item index="/docs/list/4">常见问题</el-menu-item> -->
            <!-- <el-menu-item index="/orders/list">订单明细表</el-menu-item> -->


          </el-sub-menu>
          <el-sub-menu index="4" v-if="userStore.userInfo.roleid == 1">
            <template #title>
              <el-icon>
                <location />
              </el-icon>
              <span>基础信息</span>
            </template>
            <el-menu-item index="/drug/list">药品管理</el-menu-item>
            <el-menu-item index="/charge/list">收费项目</el-menu-item>
            <el-menu-item index="/drugtype/list">药品类型</el-menu-item>
            <el-menu-item index="/supplier/list">药品供应商</el-menu-item>

            <!-- <el-menu-item index="/docs/list/4">常见问题</el-menu-item> -->
            <!-- <el-menu-item index="/orders/list">订单明细表</el-menu-item> -->


          </el-sub-menu>
          <el-sub-menu index="5" v-if="userStore.userInfo.roleid == 1">
            <template #title>
              <el-icon>
                <location />
              </el-icon>
              <span>药品入库</span>
            </template>
            <el-menu-item index="/purchase/list">药品出入库</el-menu-item>
            <el-menu-item index="/drug/stockdetail">出入库明细</el-menu-item>
            <el-menu-item index="/drug/stockreport">药品进销存</el-menu-item>
            <el-menu-item index="/drug/stock">药品库存</el-menu-item>
   

            <!-- <el-menu-item index="/docs/list/4">常见问题</el-menu-item> -->
            <!-- <el-menu-item index="/orders/list">订单明细表</el-menu-item> -->


          </el-sub-menu>
        </el-menu>
      </el-scrollbar>
    </el-aside>

    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <div class="title">门诊管理</div>
        <div class="toolbar">
          <!-- <el-dropdown>
              <el-icon style="margin-right: 8px; margin-top: 1px">
                <setting />
              </el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout" >注销系统</el-dropdown-item>
               
                </el-dropdown-menu>
              </template>
            </el-dropdown> -->
          <span>当前登录: <span style="color: #ffd04b; font-weight: bold;"></span>{{ userStore.userInfo.name }}</span>
          <span @click="logout" style="margin-left: 20px; cursor: pointer">注销系统</span>
        </div>
      </el-header>

      <el-main class="layout-container-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>


import { ref,onMounted } from 'vue'
import request from '@/utils/request'
import { Menu as IconMenu, Message, Setting, House } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores'
import { useRouter } from 'vue-router'
const router = useRouter()
const userStore = useUserStore()
//   import { useRouter } from 'vue-router'
//    const router = useRouter()

const item = {
  date: '2016-05-02',
  name: 'Tom',
  address: 'No. 189, Grove St, Los Angeles',
}
const tableData = ref(Array.from({ length: 20 }).fill(item))

const logout = () => {
  console.log('logout')
  userStore.setToken('')
  router.push('/login')
}

const docType = ref([])

const getChannels = () => {
  request.get('/getdicttype?type=文档类型').then(res => {
        if (res.data.code === 0) {
            let _data = res.data.data
            _data.forEach((item: any) => {
              docType.value.push(item.dict_value)
            })
            //保存到本地存储
            localStorage.setItem('docType', JSON.stringify(docType.value))
        }
    })
}

onMounted(() => {
  console.log(userStore.userInfo.roleid,"登录用户信息")

 
}
)

// router.push('/login')
</script>

<style scoped>
.layout-container-demo .el-header {
  position: relative;
  background-color: #303133;
  color: #fff;
}

.layout-container-demo .el-aside {
  color: #fff;
  background: #303133;
  height: 100vh;
}

.layout-container-demo .el-menu {
  border-right: none;
}

.layout-container-demo .el-main {
  padding: 0;


}

.layout-container-demo .toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}

.layout-container-main {
  padding: 20px;


}

.el-menu {
  background-color: #303133;
  ;
}

.el-menu-item span {
  color: #fff;
}

.el-menu-item:hover {
  background-color: #076916;
}

.el-menu-item-group {
  background-color: #404040;
}

.el-menu-item-group-title {
  color: #fff;
}


.el-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 80px;
}


.title {
  font-size: 24px;
  font-weight: bold;
  margin-top: 20px;
  margin-left: 400px;
  margin-bottom: 20px;
  color: #fff
}

.title-item {
  /* background-color: #03e525 !important; */
  color: #fff;
}
</style>
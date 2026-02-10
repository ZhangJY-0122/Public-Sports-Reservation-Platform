<template>

  <el-row class="login-page">
  <el-col :span="12" class="bg-img"></el-col>

  <el-col :span="6" :offset="3" class="login-form">


    <el-form :model="formModel" :rules="rules" ref="form" size="large" aria-autocomplete="off" v-if="!isRegister" >
      <el-form-item>
        <h1>登录</h1>
      </el-form-item>
      <el-form-item prop="name">
        <el-input :perfix-icon="User" v-model="formModel.mobile"  placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input :perfix-icon="Lock"  v-model="formModel.password"  type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item>
         <el-button type="primary" @click="login">登录</el-button>
      </el-form-item>

     

    </el-form>

    

  </el-col>

</el-row>

</template>
<script setup>

import { ref, reactive } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores'
const userStore=useUserStore()
import {  userRegisterService,userLoginService } from '@/api/user.js'
import { ElMessage } from 'element-plus';

import { useRouter } from 'vue-router'
const router = useRouter()

const isRegister = ref(false)
const formModel=ref({
  mobile:'',
  password:'',

})

const form=ref()

const rules = {
  mobile: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 11, message: '长度在 3 到 10 个字符', trigger: 'blur' }
  ],
  password: [ 
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 3, max: 16, message: '长度在 6 到 16 个字符', trigger: 'blur' },
    {
      pattern: /^\S{3,15}$/,
      message: '密码必须是6-15位的非空字符',
      trigger: 'blur'
    }


  ]

}



// watch(isRegister, () => {
//   form.value.resetFields()
// })

const login = async () => {
  // 表单验证

  await form.value.validate()

  const res = await userLoginService(formModel.value)



  if (res.code ===0) {
  
    console.log(res.data,"用户登录返回信息")

    userStore.setUserInfo(res.data)
    localStorage.setItem("token",res.token?res.token:'3997')
    router.push('/')
  } else {
    ElMessage.error('用户名或密码错误')
  } 

}



</script>
<style scoped>
  body{
    background-image: url('/src/assets/bg.jpg');
  }
  .login-page{
    background-image: url('/src/assets/bg.jpg') ;
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
    height: 100vh;
  }
  .login-form{
    margin-top: 200px;
  }
</style>
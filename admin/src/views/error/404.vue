<template>
    <div class="error-page">
      <div class="error-content">
        <h1>404</h1>
        <p>抱歉，您访问的页面不存在</p>
        <el-button type="primary" @click="$router.push('/')">
          返回首页
        </el-button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NotFound'
  }
  </script>
  
  <style scoped>
  .error-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f5f5;
  }
  
  .error-content {
    text-align: center;
  }
  
  .error-content h1 {
    font-size: 72px;
    color: #409eff;
    margin-bottom: 20px;
  }
  
  .error-content p {
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
  }
  </style>
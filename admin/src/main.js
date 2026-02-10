import '@/assets/main.scss'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'




import { createApp } from 'vue'



import App from './App.vue'
import router from './router'
import pinia from '@/stores/index'
import  Print from 'vue3-print-nb'; //引入打印插件




const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.use(pinia)
app.use(router)
app.use(Print) //使用打印插件
app.mount('#app')

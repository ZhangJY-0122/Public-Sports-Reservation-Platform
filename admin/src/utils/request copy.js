import axios from 'axios'
import { useUserStore } from '@/stores/modules/user'
import { ElMessage } from 'element-plus'
import router from '@/router'
const baseURL = 'http://yjgl.tstakw.top/api'
// const baseURL = 'http://tsdlyy.cc/api'
const instance = axios.create({
    baseURL: baseURL,
    timeout: 5000,
    headers: { 'Content-Type': 'application/json' }
})
//请求拦截器
instance.interceptors.request.use((config) => {
    const userStore = useUserStore()
    if (userStore.token) {
        config.headers.Authorization =  'Bearer ' +  userStore.token
    }
    return config
},
    (err) => Promise.reject(err)
)

//响应拦截器
instance.interceptors.response.use((res) => {
    if (res.status ==200) {
        return res
    }
    //处理失败错误 抛出错误
    // ElMessage.error(res.data.message||'服务异常')
   return Promise.reject(res.data)
    
},
  
    (err) => {
        if (err.response.status == 401) {
            router.push('/login')
        }
        // ElMessage.error(err.response.data.message||'网络异常')
        Promise.reject(err)
    }
)

export default instance
export { baseURL }
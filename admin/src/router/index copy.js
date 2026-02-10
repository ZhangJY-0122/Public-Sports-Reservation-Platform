import { createRouter, createWebHistory, createWebHashHistory} from 'vue-router'
import { useUserStore } from '@/stores'

const router = createRouter({
  //vite中的环境变量
  // history: createWebHistory(import.meta.env.BASE_URL),
  history: createWebHashHistory(),
  routes: [
    {
      path: '/login',
      component:()=>import('@/views/login/LoginPage.vue')
    },
    
    {
      path: '/',
      component:()=>import('@/views/layout/LayoutContainer.vue'),
      redirect:'/common/index',
      children: [
        {
          path: 'common/index',
          component: () => import('@/views/common/Index.vue')
        },
       
          
       
        
        {
          path: 'common/test',
          component: () => import('@/views/common/test.vue')
        },
        {
          path: 'user/list',
          component: () => import('@/views/user/UserList.vue')
        }
        
      
     
      

        
        

       
      ]
     }
  ]
})




// 路由守卫 登录访问拦截 ai的写法
// router.beforeEach((to, from, next) => {
//   const token = localStorage.getItem('token')
//   if (to.path === '/login' || to.path === '/') {
//     next()
//   } else if (token) {
//     next()
//   } else {
//     next('/login')
//   }
// })  
// 路由守卫 登录访问拦截  教程的写法
// router.beforeEach((to)=>{
//   const token = localStorage.getItem('token')
//   if(!token && to.path !== '/login')
//   {
//     return '/login'
//   }
  
// })
//登录访问拦截 =>默认是直接放行的
//1根据返回值决定，是放行还是拦截11返回值:
//1.undefined/true 直接放行
//2.false 拦回from的地址页面
//3.具体路径或路径对象拦截到对应的地址

router.beforeEach((to) => {
  const useStore=useUserStore()
console.log(useStore.token,"token")
  if(!useStore.token && to.path !== '/login') return '/login'
})


export default router

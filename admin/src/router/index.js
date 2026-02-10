import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  // 使用 hash 模式
  history: createWebHashHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/login/LoginPage.vue'),
      meta: {
        title: '登录',
        requiresAuth: false // 不需要登录验证
      }
    },
    {
      path: '/',
      name: 'Layout',
      component: () => import('@/views/layout/LayoutContainer.vue'),
      redirect: '/common/index',
      meta: {
        requiresAuth: false // 需要登录验证  true false
      },
      children: [
        {
          path: 'common/index',
          name: 'Index',
          component: () => import('@/views/common/Index.vue'),
          meta: {
            title: '首页'
          }
        },
        {
          path: 'common/test',
          name: 'Test',
          component: () => import('@/views/common/test.vue'),
          meta: {
            title: '测试页面'
          }
        },
        {          path: 'common/test2',          name: 'Test2',          component: () => import('@/views/common/test2.vue'),          meta: {            title: '测试页面2'          }        },        {          path: 'common/business-analysis',          name: 'BusinessAnalysis',          component: () => import('@/views/common/BusinessAnalysis.vue'),          meta: {            title: '场馆营业分析'          }        },
        {
          path: 'user/list',
          name: 'UserList',
          component: () => import('@/views/user/UserList.vue'),
          meta: {
            title: '用户列表'
          }
        },
        {
          path: 'venues/list',
          name: 'VenueList',
          component: () => import('@/views/venues/VenueManagement.vue'),
          meta: {
            title: '场馆管理'
          }
        },
        {
          path: 'venue/categories',
          name: 'VenueCategoryList',
          component: () => import('@/views/venue_categories/VenueCategoryList.vue'),
          meta: {
            title: '场馆分类管理'
          }
        },
        {
          path: 'coach/list',
          name: 'CoachList',
          component: () => import('@/views/coaches/CoachManagement.vue'),
          meta: {
            title: '教练管理'
          }
        },
       
        {
          path: 'activities/list',
          name: 'ActivityList',
          component: () => import('@/views/activities/ActivityList.vue'),
          meta: {
            title: '活动管理'
          }
        },
        {
          path: 'bookings/list',
          name: 'BookingList',
          component: () => import('@/views/bookings/BookingList.vue'),
          meta: {
            title: '预约管理'
          }
        },
        {
          path: 'booking_shares/list',
          name: 'BookingShareList',
          component: () => import('@/views/booking_shares/BookingShareList.vue'),
          meta: {
            title: '预约分摊管理'
          }
        },
        {
          path: 'coach_bookings/list',
          name: 'CoachBookingList',
          component: () => import('@/views/coach_bookings/CoachBookingList.vue'),
          meta: {
            title: '教练预约管理'
          }
        },
        {
          path: 'events/list',
          name: 'EventList',
          component: () => import('@/views/events/EventList.vue'),
          meta: {
            title: '赛事管理'
          }
        },
        {
          path: 'event_registrations/list',
          name: 'EventRegistrationList',
          component: () => import('@/views/event_registrations/EventRegistrationList.vue'),
          meta: {
            title: '赛事报名管理'
          }
        },
        {
          path: 'friends/list',
          name: 'FriendList',
          component: () => import('@/views/friends/FriendList.vue'),
          meta: {
            title: '朋友关系管理'
          }
        },
        {
          path: 'friendships/list',
          name: 'FriendshipList',
          component: () => import('@/views/friendships/FriendshipList.vue'),
          meta: {
            title: '好友关系管理'
          }
        },
        {
          path: 'venue_reviews/list',
          name: 'VenueReviewList',
          component: () => import('@/views/venue_reviews/VenueReviewList.vue'),
          meta: {
            title: '场馆评价管理'
          }
        }
      ]
    },
    // 404 页面处理
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/error/404.vue'),
      meta: {
        title: '页面不存在'
      }
    }
  ]
})

// 路由导航守卫 - 登录访问拦截
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title + ' - 管理系统'
  } else {
    document.title = '管理系统'
  }

  // 检查路由是否需要登录
  if (to.meta.requiresAuth) {
    try {
      // 动态导入 store 避免循环依赖
      const { useUserStore } = require('@/stores/modules/user')
      const userStore = useUserStore()
      
      if (userStore.token) {
        // 已登录，放行
        next()
      } else {
        // 未登录，跳转到登录页
        next({
          path: '/login',
          query: { redirect: to.fullPath } // 记录要跳转的页面，登录后可以跳转回来
        })
      }
    } catch (error) {
      console.error('路由守卫错误:', error)
      // 如果 store 获取失败，使用 localStorage 作为备选方案
      const token = localStorage.getItem('token')
      if (token) {
        next()
      } else {
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        })
      }
    }
  } else {
    // 不需要登录验证的路由，直接放行
    next()
  }
})

// 路由错误处理
router.onError((error) => {
  console.error('路由错误:', error)
})

export default router
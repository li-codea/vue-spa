import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/search',
    name: 'search',
    // 搜索词走 query，例如 /search?q=星际穿越
    component: () => import('@/views/SearchView.vue'),
    meta: { title: '搜索' }
  },
  {
    path: '/detail/:id',
    name: 'detail',
    // :id 是影片 ID，例如 /detail/m1
    component: () => import('@/views/DetailView.vue'),
    meta: { title: '详情' }
  },
  {
    path: '/category/:genre',
    name: 'category',
    // 按类型浏览，例如 /category/科幻
    component: () => import('@/views/CategoryView.vue'),
    meta: { title: '分类' }
  },
  {
    path: '/watchlist',
    name: 'watchlist',
    component: () => import('@/views/WatchlistView.vue'),
    meta: { title: '我的片单' }
  },
  {
    path: '/stats',
    name: 'stats',
    component: () => import('@/views/StatsView.vue'),
    meta: { title: '数据统计' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { title: '页面不存在' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  // 切换页面时回到顶部
  scrollBehavior() {
    return { top: 0 }
  }
})

// 根据路由自动更新浏览器标题
router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} · 片单` : '片单'
})

export default router

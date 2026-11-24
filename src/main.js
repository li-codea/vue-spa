// 1. 引入 Vue 的核心创建函数
import { createApp } from 'vue'
// 2. 引入 Pinia 和它的持久化插件
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
// 3. 引入你的根组件（画板）
import App from './App.vue'
// 4. 引入路由
import router from './router'

// 5. 创建一个 Pinia 实例
const pinia = createPinia()
// 6. 给 Pinia 装上持久化插件
pinia.use(piniaPluginPersistedstate)

// 7. 创建 Vue 应用，并且开始“装配”
createApp(App)
  .use(pinia)   // 把 Pinia 装上去
  .use(router)  // 把路由装上去
  .mount('#app') // 最后一步！把装配好的应用，塞进 index.html 里那个 id="app" 的盒子里
<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useWatchlistStore } from '@/stores/watchlist'

const router = useRouter()
const route = useRoute()
const keyword = ref('')

const watchlistStore = useWatchlistStore()
const { watchlistCount } = storeToRefs(watchlistStore)

// 分类导航（与 mockData 里的 genre 对应）
const genres = ['剧情', '喜剧', '爱情', '科幻', '动作', '犯罪', '悬疑', '动画', '奇幻', '冒险', '战争', '传记', '音乐', '灾难', '家庭']

function isHomeActive() {
  return route.path === '/'
}
function isGenreActive(g) {
  return route.name === 'category' && route.params.genre === g
}

// 搜索提交：跳转 /search?q=关键词
function handleSearch() {
  const q = keyword.value.trim()
  if (!q) return
  router.push({ path: '/search', query: { q } })
}
</script>

<template>
  <div class="app">
    <!-- 顶部导航栏 -->
    <header class="site-header">
      <div class="navbar">
        <router-link to="/" class="logo">🎬 片单</router-link>

        <form class="search" @submit.prevent="handleSearch">
          <input
            v-model="keyword"
            type="search"
            placeholder="搜索电影、剧集…"
          />
          <button type="submit">搜索</button>
        </form>

        <router-link
          to="/stats"
          class="nav-link"
          :class="{ active: route.path === '/stats' }"
        >统计</router-link>

        <router-link to="/watchlist" class="watchlist-link">
          我的片单
          <span v-if="watchlistCount > 0" class="badge">{{ watchlistCount }}</span>
        </router-link>
      </div>

      <!-- 分类导航条 -->
      <nav class="genre-nav">
        <router-link to="/" :class="{ active: isHomeActive() }">全部</router-link>
        <router-link
          v-for="g in genres"
          :key="g"
          :to="`/category/${g}`"
          :class="{ active: isGenreActive(g) }"
        >{{ g }}</router-link>
      </nav>
    </header>

    <!-- 页面主体，随路由切换 -->
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<style>
/* 全局基础样式（非 scoped） */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
    'Microsoft YaHei', sans-serif;
  color: #f5f5f7;
  /* 深色背景 + 暗红/靛蓝微光 */
  background-color: #0e0e13;
  background-image: radial-gradient(
      circle at 12% 18%,
      rgba(229, 9, 20, 0.1),
      transparent 32%
    ),
    radial-gradient(
      circle at 88% 22%,
      rgba(99, 102, 241, 0.14),
      transparent 34%
    ),
    radial-gradient(
      circle at 55% 95%,
      rgba(245, 158, 11, 0.07),
      transparent 38%
    );
  background-attachment: fixed;
}
a {
  text-decoration: none;
  color: inherit;
}
</style>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部整体（主导航栏 + 分类条），吸顶 + 磨砂玻璃 */
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
}

/* 主导航栏 */
.navbar {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 0 32px;
  height: 64px;
  background: rgba(16, 16, 22, 0.72);
  backdrop-filter: blur(16px) saturate(140%);
  -webkit-backdrop-filter: blur(16px) saturate(140%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.logo {
  font-size: 20px;
  font-weight: 700;
  color: #e50914;
  white-space: nowrap;
}

/* 搜索框 */
.search {
  flex: 1;
  display: flex;
  gap: 8px;
  max-width: 480px;
  margin: 0 auto;
}
.search input {
  flex: 1;
  height: 40px;
  padding: 0 16px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  font-size: 14px;
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  color: #f5f5f7;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.search input::placeholder {
  color: #8a8f98;
}
.search input:focus {
  border-color: #e50914;
  box-shadow: 0 0 0 3px rgba(229, 9, 20, 0.2);
}
.search button {
  height: 40px;
  padding: 0 20px;
  border: none;
  border-radius: 20px;
  background: #e50914;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}
.search button:hover {
  background: #c50810;
}

/* 片单入口 */
.watchlist-link {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #b8b8c0;
  white-space: nowrap;
  transition: color 0.2s;
}
.watchlist-link:hover {
  color: #fff;
}
.nav-link {
  font-size: 14px;
  color: #b8b8c0;
  white-space: nowrap;
  transition: color 0.2s;
}
.nav-link:hover,
.nav-link.active {
  color: #fff;
}
.badge {
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #e50914;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  border-radius: 10px;
}

/* 分类导航条 */
.genre-nav {
  display: flex;
  gap: 6px;
  padding: 10px 32px;
  background: rgba(16, 16, 22, 0.55);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  overflow-x: auto;
  white-space: nowrap;
  scrollbar-width: none;
}
.genre-nav::-webkit-scrollbar {
  display: none;
}
.genre-nav a {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 13px;
  color: #b8b8c0;
  transition: background 0.2s, color 0.2s;
}
.genre-nav a:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}
.genre-nav a.active {
  background: #e50914;
  color: #fff;
}

/* 主体 */
.main {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;
}
</style>

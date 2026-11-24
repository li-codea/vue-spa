// src/stores/watchlist.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useWatchlistStore = defineStore(
  'watchlist',
  () => {
    // ---------- State ----------
    // 存放收藏的电影对象（存完整对象，片单页可直接渲染，无需再请求）
    const watchlist = ref([])

    // ---------- Getters ----------
    // 收藏总数（首页「我的片单」角标用）
    const watchlistCount = computed(() => watchlist.value.length)

    // 判断某部电影是否已收藏（详情页判断按钮高亮状态用）
    const isInWatchlist = computed(() => {
      return (id) => watchlist.value.some((movie) => movie.id === id)
    })

    // ---------- Actions ----------
    // 添加收藏：防重复，已存在则返回 false
    function addToWatchlist(movie) {
      if (watchlist.value.some((m) => m.id === movie.id)) {
        return false
      }
      watchlist.value.push(movie)
      return true
    }

    // 移除收藏
    function removeFromWatchlist(id) {
      watchlist.value = watchlist.value.filter((movie) => movie.id !== id)
    }

    // 切换收藏状态（详情页按钮最常用：收藏 ⇄ 取消收藏）
    function toggleWatchlist(movie) {
      if (isInWatchlist.value(movie.id)) {
        removeFromWatchlist(movie.id)
        return false
      }
      return addToWatchlist(movie)
    }

    // 清空片单
    function clearWatchlist() {
      watchlist.value = []
    }

    return {
      watchlist,
      watchlistCount,
      isInWatchlist,
      addToWatchlist,
      removeFromWatchlist,
      toggleWatchlist,
      clearWatchlist
    }
  },
  {
    // ---------- 持久化配置（pinia-plugin-persistedstate）----------
    persist: {
      key: 'watchlist',      // localStorage 里的键名，刷新后从这里恢复
      storage: localStorage  // 默认就是 localStorage，写出来是为了明确
    }
  }
)

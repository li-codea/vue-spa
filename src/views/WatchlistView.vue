<script setup>
import { storeToRefs } from 'pinia'
import { useWatchlistStore } from '@/stores/watchlist'
import MovieCard from '@/components/MovieCard.vue'

const watchlistStore = useWatchlistStore()
const { watchlist } = storeToRefs(watchlistStore)

function clearAll() {
  if (window.confirm('确定清空整个片单吗？')) {
    watchlistStore.clearWatchlist()
  }
}
</script>

<template>
  <div class="watchlist-view">
    <div class="header">
      <h1 class="page-title">我的片单（{{ watchlist.length }}）</h1>
      <button v-if="watchlist.length" class="clear-btn" @click="clearAll">
        清空
      </button>
    </div>

    <div v-if="watchlist.length === 0" class="empty">
      <p class="empty-text">片单还是空的，去发现些好片吧～</p>
      <router-link to="/" class="go-home">去首页逛逛</router-link>
    </div>

    <div v-else class="grid">
      <MovieCard v-for="movie in watchlist" :key="movie.id" :movie="movie" />
    </div>
  </div>
</template>

<style scoped>
.watchlist-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.page-title {
  font-size: 24px;
  font-weight: 700;
}
.clear-btn {
  padding: 8px 18px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.06);
  color: #b8b8c0;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s;
}
.clear-btn:hover {
  color: #e50914;
  border-color: #e50914;
}

.empty {
  padding: 80px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.empty-text {
  color: #9aa0ac;
}
.go-home {
  padding: 10px 22px;
  background: #e50914;
  color: #fff;
  border-radius: 8px;
  font-size: 14px;
}
.go-home:hover {
  background: #c50810;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 24px;
}
</style>

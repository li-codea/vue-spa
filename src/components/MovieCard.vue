<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useWatchlistStore } from '@/stores/watchlist'

const props = defineProps({
  movie: { type: Object, required: true }
})

const watchlistStore = useWatchlistStore()
const { isInWatchlist } = storeToRefs(watchlistStore)

// 是否已收藏（心形高亮用）
const favorited = computed(() => isInWatchlist.value(props.movie.id))

function toggleFavorite() {
  watchlistStore.toggleWatchlist(props.movie)
}
</script>

<template>
  <div class="card">
    <router-link :to="`/detail/${movie.id}`" class="card-link">
      <div class="poster">
        <img :src="movie.poster" :alt="movie.title" loading="lazy" />
        <span class="rating">
          <span class="star">★</span> {{ movie.rating }}
        </span>
      </div>
      <div class="info">
        <h3 class="title">{{ movie.title }}</h3>
        <p class="meta">{{ movie.year }} · {{ movie.genre.join(' / ') }}</p>
      </div>
    </router-link>

    <button
      class="fav"
      :class="{ active: favorited }"
      :title="favorited ? '取消收藏' : '加入片单'"
      @click.prevent="toggleFavorite"
    >
      {{ favorited ? '♥' : '♡' }}
    </button>
  </div>
</template>

<style scoped>
.card {
  position: relative;
  background: #1a1a23;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.45);
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.card:hover {
  transform: translateY(-6px) scale(1.03);
  border-color: rgba(229, 9, 20, 0.7);
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.6),
    0 0 22px rgba(229, 9, 20, 0.28);
}

.card-link {
  display: flex;
  flex-direction: column;
}

.poster {
  position: relative;
  aspect-ratio: 2 / 3;
  background: #26262f;
  overflow: hidden;
}
.poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}
.card:hover .poster img {
  transform: scale(1.06);
}

/* 评分角标（胶囊形） */
.rating {
  position: absolute;
  top: 10px;
  right: 10px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.14);
  color: #ffd43b;
  font-size: 13px;
  font-weight: 700;
  border-radius: 999px;
}
.rating .star {
  font-size: 12px;
}

.info {
  padding: 12px 14px 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.title {
  font-size: 15px;
  font-weight: 600;
  color: #f5f5f7;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.meta {
  font-size: 13px;
  color: #9aa0ac;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 收藏按钮（左上角） */
.fav {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  color: #d0d0d8;
  font-size: 18px;
  cursor: pointer;
  transition: color 0.2s, background 0.2s, transform 0.2s;
}
.fav:hover {
  transform: scale(1.12);
}
.fav.active {
  color: #e50914;
}
</style>

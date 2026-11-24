<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { fetchMovies } from '@/api/movies'
import { useWatchlistStore } from '@/stores/watchlist'
import MovieCard from '@/components/MovieCard.vue'

const route = useRoute()

const watchlistStore = useWatchlistStore()
const { isInWatchlist } = storeToRefs(watchlistStore)

const allMovies = ref([])
const movie = ref(null)
const loading = ref(true)
const error = ref('')

// 是否已收藏
const favorited = computed(
  () => !!movie.value && isInWatchlist.value(movie.value.id)
)

// 相关推荐：类型有交集（排除当前这部），最多 6 部
const related = computed(() => {
  if (!movie.value) return []
  const genres = movie.value.genre || []
  return allMovies.value
    .filter(
      (m) =>
        m.id !== movie.value.id &&
        (m.genre || []).some((g) => genres.includes(g))
    )
    .slice(0, 6)
})

async function load() {
  loading.value = true
  error.value = ''
  movie.value = null
  try {
    // 只在第一次拉取全量数据，避免每次切详情都重新请求
    if (allMovies.value.length === 0) {
      allMovies.value = await fetchMovies()
    }
    movie.value = allMovies.value.find((m) => m.id === route.params.id) || null
    if (!movie.value) error.value = '未找到该影片'
  } catch (err) {
    error.value = '加载失败'
  } finally {
    loading.value = false
  }
}

onMounted(load)
// 从「相关推荐」点到另一部详情时，:id 变化触发重新加载
watch(() => route.params.id, load)

function toggleFavorite() {
  if (movie.value) watchlistStore.toggleWatchlist(movie.value)
}
</script>

<template>
  <div class="detail">
    <div v-if="loading" class="state">加载中…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>

    <template v-else-if="movie">
      <!-- Hero 区 -->
      <div class="hero">
        <div
          class="hero-bg"
          :style="{ backgroundImage: `url(${movie.backdrop})` }"
        ></div>
        <!-- 黑色到透明的渐变遮罩，保证白色文字可读 -->
        <div class="hero-overlay"></div>
        <div class="hero-content">
          <img class="poster" :src="movie.poster" :alt="movie.title" />
          <div class="hero-info">
            <h1 class="title">
              {{ movie.title }}
              <span class="orig">{{ movie.originalTitle }}</span>
            </h1>
            <div class="tags">
              <span class="tag">{{ movie.year }}</span>
              <span class="tag">{{ movie.region }}</span>
              <span v-for="g in movie.genre" :key="g" class="tag">{{ g }}</span>
            </div>
            <p class="rating">
              ★ {{ movie.rating }}
              <span class="count">（{{ movie.ratingCount }} 人评分）</span>
            </p>
            <button
              class="fav-btn"
              :class="{ active: favorited }"
              @click="toggleFavorite"
            >
              {{ favorited ? '♥ 已加入片单' : '♡ 加入片单' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 剧情简介 -->
      <div class="section">
        <h2>剧情简介</h2>
        <p class="desc">{{ movie.description }}</p>
        <div class="meta-list">
          <p><strong>导演：</strong>{{ movie.director }}</p>
          <p><strong>主演：</strong>{{ movie.cast.join('、') }}</p>
          <p><strong>片长：</strong>{{ movie.duration }} 分钟</p>
        </div>
      </div>

      <!-- 相关推荐 -->
      <div v-if="related.length" class="section">
        <h2>相关推荐</h2>
        <div class="grid">
          <MovieCard v-for="m in related" :key="m.id" :movie="m" />
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.detail {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.state {
  padding: 60px 0;
  text-align: center;
  color: #9aa0ac;
}
.state.error {
  color: #e50914;
}

/* Hero 区 */
.hero {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  background: #14141a;
}
.hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
}
/* 黑色 → 透明 渐变遮罩（左→右 + 底→上），确保文字可读 */
.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
      90deg,
      rgba(0, 0, 0, 0.9) 0%,
      rgba(0, 0, 0, 0.5) 45%,
      rgba(0, 0, 0, 0.08) 100%
    ),
    linear-gradient(0deg, rgba(0, 0, 0, 0.7) 0%, transparent 45%);
}
.hero-content {
  position: relative;
  display: flex;
  gap: 28px;
  padding: 32px;
  align-items: center;
}
.poster {
  width: 200px;
  aspect-ratio: 2 / 3;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  flex-shrink: 0;
}
.hero-info {
  color: #fff;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.title {
  font-size: 32px;
  font-weight: 700;
}
.orig {
  font-size: 18px;
  font-weight: 400;
  color: #cbd5e1;
  margin-left: 8px;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.tag {
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  font-size: 13px;
}
.rating {
  font-size: 16px;
  color: #ffd43b;
}
.rating .count {
  font-size: 13px;
  color: #cbd5e1;
}

.fav-btn {
  align-self: flex-start;
  padding: 10px 22px;
  border: none;
  border-radius: 8px;
  background: #e50914;
  color: #fff;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s;
}
.fav-btn:hover {
  background: #c50810;
}
.fav-btn.active {
  background: rgba(255, 255, 255, 0.18);
}

/* 详情区块 */
.section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.section h2 {
  font-size: 20px;
  font-weight: 700;
}
.desc {
  line-height: 1.8;
  color: #c6c6cf;
}
.meta-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: #b8b8c0;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 24px;
}

@media (max-width: 640px) {
  .hero-content {
    flex-direction: column;
    align-items: flex-start;
  }
  .poster {
    width: 140px;
  }
}
</style>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { fetchMovies } from '@/api/movies'
import MovieCard from '@/components/MovieCard.vue'

const movies = ref([])
const loading = ref(true)
const error = ref('')

// 按热度（popularity）从高到低排序
const sortedByHot = computed(() =>
  [...movies.value].sort((a, b) => (b.popularity || 0) - (a.popularity || 0))
)

// 顶部推荐栏：热度前 3
const featured = computed(() => sortedByHot.value.slice(0, 3))

// 热门榜单：热度前 8
const ranking = computed(() => sortedByHot.value.slice(0, 8))

// 轮播当前索引 + 自动播放
const current = ref(0)
let timer = null

function next() {
  if (!featured.value.length) return
  current.value = (current.value + 1) % featured.value.length
}
function go(i) {
  current.value = i
}

async function load() {
  loading.value = true
  try {
    movies.value = await fetchMovies()
  } catch (err) {
    error.value = '加载失败，请确认 public/mock/mockData.json 是否存在'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  load()
  timer = setInterval(next, 4000)
})
onUnmounted(() => {
  clearInterval(timer)
})
</script>

<template>
  <section class="home">
    <div v-if="loading" class="state">加载中…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>

    <template v-else>
      <!-- 顶部推荐栏（轮播） -->
      <div class="banner">
        <div
          class="banner-track"
          :style="{ transform: `translateX(-${current * 100}%)` }"
        >
          <router-link
            v-for="m in featured"
            :key="m.id"
            :to="`/detail/${m.id}`"
            class="banner-slide"
          >
            <img class="banner-bg" :src="m.backdrop" :alt="m.title" />
            <div class="banner-overlay"></div>
            <div class="banner-content">
              <span class="banner-tag">🔥 热门推荐</span>
              <h2 class="banner-title">{{ m.title }}</h2>
              <p class="banner-desc">{{ m.description }}</p>
              <div class="banner-meta">
                ★ {{ m.rating }} · {{ m.year }} · {{ m.genre.join(' / ') }}
              </div>
            </div>
          </router-link>
        </div>
        <div class="banner-dots">
          <button
            v-for="(m, i) in featured"
            :key="m.id"
            :class="{ active: current === i }"
            @click="go(i)"
          ></button>
        </div>
      </div>

      <!-- 热门榜单 -->
      <section class="ranking-section">
        <h2 class="section-title">热门榜单</h2>
        <ol class="ranking-list">
          <li v-for="(m, i) in ranking" :key="m.id" class="ranking-item">
            <span class="rank" :class="{ top: i < 3 }">{{ i + 1 }}</span>
            <router-link :to="`/detail/${m.id}`" class="ranking-link">
              <img class="thumb" :src="m.poster" :alt="m.title" />
              <div class="ranking-info">
                <h3 class="ranking-title">{{ m.title }}</h3>
                <p class="ranking-meta">
                  {{ m.year }} · {{ m.genre.join(' / ') }}
                </p>
              </div>
              <div class="ranking-right">
                <span class="hot">🔥 {{ m.popularity }}</span>
                <span class="score">★ {{ m.rating }}</span>
              </div>
            </router-link>
          </li>
        </ol>
      </section>

      <!-- 全部影片 -->
      <section class="all-section">
        <h2 class="section-title">全部影片</h2>
        <div class="grid">
          <MovieCard v-for="movie in movies" :key="movie.id" :movie="movie" />
        </div>
      </section>
    </template>
  </section>
</template>

<style scoped>
.home {
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

.section-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 16px;
}

/* ===== 顶部推荐栏（轮播） ===== */
.banner {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
}
.banner-track {
  display: flex;
  transition: transform 0.5s ease;
}
.banner-slide {
  position: relative;
  min-width: 100%;
  aspect-ratio: 21 / 9;
  display: block;
}
.banner-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.banner-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
      90deg,
      rgba(0, 0, 0, 0.85) 0%,
      rgba(0, 0, 0, 0.4) 55%,
      rgba(0, 0, 0, 0.15) 100%
    ),
    linear-gradient(0deg, rgba(0, 0, 0, 0.5) 0%, transparent 50%);
}
.banner-content {
  position: absolute;
  left: 40px;
  bottom: 40px;
  max-width: 60%;
  color: #fff;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.banner-tag {
  align-self: flex-start;
  padding: 4px 12px;
  background: rgba(229, 9, 20, 0.9);
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}
.banner-title {
  font-size: 36px;
  font-weight: 700;
}
.banner-desc {
  font-size: 14px;
  line-height: 1.6;
  color: #e5e7eb;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.banner-meta {
  font-size: 14px;
  color: #ffd43b;
}
.banner-dots {
  position: absolute;
  right: 24px;
  bottom: 24px;
  display: flex;
  gap: 8px;
}
.banner-dots button {
  width: 10px;
  height: 10px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: all 0.2s;
}
.banner-dots button.active {
  background: #e50914;
  width: 24px;
  border-radius: 5px;
}

/* ===== 热门榜单 ===== */
.ranking-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.ranking-item {
  display: flex;
  align-items: center;
  gap: 16px;
}
.rank {
  width: 32px;
  font-size: 22px;
  font-weight: 800;
  color: #4a4a56;
  text-align: center;
  flex-shrink: 0;
}
.rank.top {
  color: #e50914;
}
.ranking-link {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px;
  background: #1a1a23;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  transition: border-color 0.2s, background 0.2s;
}
.ranking-link:hover {
  border-color: rgba(229, 9, 20, 0.5);
  background: #201f2b;
}
.thumb {
  width: 56px;
  aspect-ratio: 2 / 3;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}
.ranking-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.ranking-title {
  font-size: 15px;
  font-weight: 600;
  color: #f5f5f7;
}
.ranking-meta {
  font-size: 13px;
  color: #9aa0ac;
}
.ranking-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}
.hot {
  font-size: 13px;
  color: #ff8a80;
}
.score {
  font-size: 15px;
  color: #ffd43b;
  font-weight: 700;
}

/* ===== 全部影片 ===== */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 24px;
}

@media (max-width: 640px) {
  .banner-content {
    left: 20px;
    bottom: 20px;
    max-width: 80%;
  }
  .banner-title {
    font-size: 24px;
  }
  .banner-desc {
    display: none;
  }
}
</style>

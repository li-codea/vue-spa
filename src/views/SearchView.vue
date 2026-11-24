<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchMovies } from '@/api/movies'
import MovieCard from '@/components/MovieCard.vue'

const route = useRoute()

const allMovies = ref([])
const loading = ref(true)
const error = ref('')

// 搜索词来自 URL 的 ?q=
const keyword = computed(() => (route.query.q || '').trim())

// 客户端过滤：匹配片名/原名/导演/类型/演员
const results = computed(() => {
  if (!keyword.value) return []
  const kw = keyword.value.toLowerCase()
  return allMovies.value.filter((m) => {
    const haystack = [
      m.title,
      m.originalTitle,
      m.director,
      ...(m.genre || []),
      ...(m.cast || [])
    ]
      .join(' ')
      .toLowerCase()
    return haystack.includes(kw)
  })
})

async function load() {
  loading.value = true
  try {
    allMovies.value = await fetchMovies()
  } catch (err) {
    error.value = '加载失败'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="search-view">
    <h1 class="page-title">
      搜索<span v-if="keyword">「{{ keyword }}」</span>
    </h1>

    <div v-if="loading" class="state">加载中…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>
    <div v-else-if="!keyword" class="state">在顶部搜索框输入关键词</div>
    <div v-else-if="results.length === 0" class="state">
      没有找到与「{{ keyword }}」相关的影片
    </div>
    <div v-else class="grid">
      <MovieCard v-for="movie in results" :key="movie.id" :movie="movie" />
    </div>
  </div>
</template>

<style scoped>
.search-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.page-title {
  font-size: 24px;
  font-weight: 700;
}
.state {
  padding: 60px 0;
  text-align: center;
  color: #9aa0ac;
}
.state.error {
  color: #e50914;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 24px;
}
</style>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchMovies } from '@/api/movies'
import MovieCard from '@/components/MovieCard.vue'

const route = useRoute()

const allMovies = ref([])
const loading = ref(true)
const error = ref('')

// 当前类型（来自 URL /category/:genre）
const genre = computed(() => route.params.genre || '')

// 按类型过滤
const movies = computed(() =>
  allMovies.value.filter((m) => (m.genre || []).includes(genre.value))
)

async function load() {
  loading.value = true
  try {
    if (allMovies.value.length === 0) {
      allMovies.value = await fetchMovies()
    }
  } catch (err) {
    error.value = '加载失败'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <section class="category">
    <h1 class="page-title">{{ genre }} · 影片</h1>
    <p class="subtitle">共 {{ movies.length }} 部</p>

    <div v-if="loading" class="state">加载中…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>
    <div v-else-if="movies.length === 0" class="state">该类型下暂无影片</div>
    <div v-else class="grid">
      <MovieCard v-for="movie in movies" :key="movie.id" :movie="movie" />
    </div>
  </section>
</template>

<style scoped>
.category {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.page-title {
  font-size: 24px;
  font-weight: 700;
}
.subtitle {
  font-size: 14px;
  color: #8a8f98;
  margin-bottom: 16px;
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

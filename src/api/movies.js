// src/api/movies.js
// 统一的数据请求入口：以后接真实后端，只改这里的地址，页面不用动
import axios from 'axios'

const MOCK_URL = '/mock/mockData.json'

// 获取全部影片
export async function fetchMovies() {
  const { data } = await axios.get(MOCK_URL)
  return data
}

// 按 ID 获取单部影片（找不到返回 null）
export async function fetchMovieById(id) {
  const movies = await fetchMovies()
  return movies.find((m) => m.id === id) || null
}

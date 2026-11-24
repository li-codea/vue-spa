<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchMovies } from '@/api/movies'
import BaseChart from '@/components/BaseChart.vue'

// ---------- 数据状态 ----------
const movies = ref([])
const loading = ref(true)
const error = ref('')

// ---------- 配色（暗色主题，取自 dataviz 验证过的色板） ----------
const C = {
  blue: '#3987e5',
  orange: '#d95926',
  aqua: '#199e70',
  yellow: '#c98500',
  magenta: '#d55181'
}
const TEXT = '#b8b8c0' // 分类轴文字
const MUTED = '#8a8f98' // 数值轴文字
const GRID_LINE = 'rgba(255, 255, 255, 0.08)' // 网格线
const SURFACE = '#1a1a23' // 面板底色（环图分割缝用）

// 深色提示框
const TOOLTIP = {
  backgroundColor: 'rgba(18, 18, 26, 0.96)',
  borderColor: 'rgba(255, 255, 255, 0.12)',
  borderWidth: 1,
  textStyle: { color: '#f5f5f7', fontSize: 13 },
  padding: [8, 12]
}

// ---------- KPI 总览 ----------
const stats = computed(() => {
  const total = movies.value.length
  const avg = total ? movies.value.reduce((s, m) => s + m.rating, 0) / total : 0
  const top = [...movies.value].sort((a, b) => b.rating - a.rating)[0]
  const genreCount = new Set(movies.value.flatMap((m) => m.genre || [])).size
  return { total, avg, top, genreCount }
})

// ---------- 类型分布（TOP 8） ----------
const genreData = computed(() => {
  const g = {}
  movies.value.forEach((m) =>
    (m.genre || []).forEach((x) => (g[x] = (g[x] || 0) + 1))
  )
  return Object.entries(g)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
})

// ---------- 地区分布（TOP 5 + 其他） ----------
const regionData = computed(() => {
  const r = {}
  movies.value.forEach((m) => {
    String(m.region || '')
      .split('/')
      .map((s) => s.trim())
      .filter(Boolean)
      .forEach((x) => (r[x] = (r[x] || 0) + 1))
  })
  const sorted = Object.entries(r).sort((a, b) => b[1] - a[1])
  const top = sorted.slice(0, 5)
  const rest = sorted.slice(5).reduce((s, [, v]) => s + v, 0)
  if (rest) top.push(['其他', rest])
  return top
})

// ---------- 评分分布（每 0.5 分一档） ----------
const ratingData = computed(() => {
  const bins = []
  for (let lo = 6.0; lo < 10.0; lo += 0.5) {
    const hi = lo + 0.5
    const count = movies.value.filter((m) => m.rating >= lo && m.rating < hi).length
    bins.push({ label: lo.toFixed(1), range: `${lo.toFixed(1)}~${hi.toFixed(1)}`, count })
  }
  return bins
})

// ---------- 年代分布（每十年） ----------
const decadeData = computed(() => {
  const d = {}
  movies.value.forEach((m) => {
    const k = Math.floor(m.year / 10) * 10
    d[k] = (d[k] || 0) + 1
  })
  return Object.entries(d).sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
})

// ---------- 通用坐标轴 ----------
function catAxis(data, extra = {}) {
  return {
    type: 'category',
    data,
    axisLine: { lineStyle: { color: GRID_LINE } },
    axisTick: { show: false },
    axisLabel: { color: TEXT },
    ...extra
  }
}
function valueAxis(extra = {}) {
  return {
    type: 'value',
    axisLabel: { color: MUTED },
    splitLine: { lineStyle: { color: GRID_LINE } },
    ...extra
  }
}

// ---------- 图表配置 ----------

// 类型分布：横向柱状图（单色，比较数量大小）
const genreOption = computed(() => ({
  tooltip: { ...TOOLTIP, trigger: 'axis', axisPointer: { type: 'shadow' } },
  grid: { left: 4, right: 40, top: 4, bottom: 4, containLabel: true },
  xAxis: valueAxis(),
  yAxis: catAxis(genreData.value.map((d) => d[0]), {
    inverse: true,
    axisLine: { show: false },
    splitLine: { show: false }
  }),
  series: [
    {
      type: 'bar',
      data: genreData.value.map((d) => d[1]),
      barMaxWidth: 20,
      itemStyle: { color: C.blue, borderRadius: [0, 4, 4, 0] },
      label: { show: true, position: 'right', color: TEXT, fontSize: 12 }
    }
  ]
}))

// 评分分布：纵向柱状图（单色）
const ratingOption = computed(() => ({
  tooltip: {
    ...TOOLTIP,
    trigger: 'axis',
    axisPointer: { type: 'shadow' },
    formatter: (params) => {
      const d = ratingData.value[params[0].dataIndex]
      return `${d.range} 分：${d.count} 部`
    }
  },
  grid: { left: 4, right: 12, top: 24, bottom: 8, containLabel: true },
  xAxis: catAxis(ratingData.value.map((d) => d.label), {
    axisLabel: { color: TEXT, interval: 0, fontSize: 11 }
  }),
  yAxis: valueAxis(),
  series: [
    {
      type: 'bar',
      data: ratingData.value.map((d) => d.count),
      barMaxWidth: 24,
      itemStyle: { color: C.orange, borderRadius: [4, 4, 0, 0] },
      label: { show: true, position: 'top', color: TEXT, fontSize: 12 }
    }
  ]
}))

// 年代分布：面积折线（时间趋势）
const decadeOption = computed(() => ({
  tooltip: { ...TOOLTIP, trigger: 'axis' },
  grid: { left: 4, right: 16, top: 24, bottom: 8, containLabel: true },
  xAxis: catAxis(decadeData.value.map((d) => d[0]), {
    axisLabel: { color: TEXT, interval: 0 }
  }),
  yAxis: valueAxis(),
  series: [
    {
      type: 'line',
      data: decadeData.value.map((d) => d[1]),
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: { color: C.aqua, width: 2 },
      itemStyle: { color: C.aqua, borderColor: SURFACE, borderWidth: 2 },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(25, 158, 112, 0.10)' },
            { offset: 1, color: 'rgba(25, 158, 112, 0)' }
          ]
        }
      }
    }
  ]
}))

// 地区分布：环形图（分类色，占比）
const regionOption = computed(() => {
  const palette = [C.blue, C.orange, C.aqua, C.yellow, C.magenta]
  const data = regionData.value.map(([name, value], i) => ({
    name,
    value,
    itemStyle: { color: i < palette.length ? palette[i] : '#4a4a56' }
  }))
  return {
    tooltip: { ...TOOLTIP, trigger: 'item', formatter: '{b}：{c} 部（{d}%）' },
    legend: {
      bottom: 0,
      textStyle: { color: TEXT, fontSize: 12 },
      itemWidth: 10,
      itemHeight: 10,
      itemGap: 12
    },
    series: [
      {
        type: 'pie',
        radius: ['46%', '70%'],
        center: ['50%', '44%'],
        avoidLabelOverlap: true,
        itemStyle: { borderColor: SURFACE, borderWidth: 2 },
        label: { show: true, position: 'outside', formatter: '{d}%', color: TEXT, fontSize: 12 },
        labelLine: { length: 8, length2: 8, lineStyle: { color: GRID_LINE } },
        data
      }
    ]
  }
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    movies.value = await fetchMovies()
  } catch (err) {
    error.value = '加载失败'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <section class="stats">
    <header class="head">
      <h1 class="page-title">数据统计</h1>
      <p class="subtitle">基于本地 Mock 数据 · 共 {{ stats.total }} 部影片</p>
    </header>

    <div v-if="loading" class="state">加载中…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>

    <template v-else>
      <!-- KPI 总览 -->
      <div class="kpi-row">
        <div class="kpi">
          <span class="kpi-label">影片总数</span>
          <span class="kpi-value">{{ stats.total }}</span>
        </div>
        <div class="kpi">
          <span class="kpi-label">平均评分</span>
          <span class="kpi-value">{{ stats.avg.toFixed(2) }}</span>
        </div>
        <div class="kpi">
          <span class="kpi-label">最高评分</span>
          <span class="kpi-value">{{ stats.top?.rating ?? '—' }}</span>
          <span class="kpi-note">{{ stats.top?.title }}</span>
        </div>
        <div class="kpi">
          <span class="kpi-label">覆盖类型</span>
          <span class="kpi-value">{{ stats.genreCount }}</span>
        </div>
      </div>

      <!-- 图表区 -->
      <div class="charts-grid">
        <div class="panel">
          <h2 class="panel-title">类型分布<span class="panel-sub">TOP 8</span></h2>
          <BaseChart :option="genreOption" height="320px" />
        </div>
        <div class="panel">
          <h2 class="panel-title">地区分布</h2>
          <BaseChart :option="regionOption" height="320px" />
        </div>
        <div class="panel">
          <h2 class="panel-title">评分分布<span class="panel-sub">每 0.5 分一档</span></h2>
          <BaseChart :option="ratingOption" height="300px" />
        </div>
        <div class="panel">
          <h2 class="panel-title">年代分布<span class="panel-sub">按十年</span></h2>
          <BaseChart :option="decadeOption" height="300px" />
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped>
.stats {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.head {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.page-title {
  font-size: 24px;
  font-weight: 700;
}
.subtitle {
  font-size: 14px;
  color: #8a8f98;
}
.state {
  padding: 60px 0;
  text-align: center;
  color: #9aa0ac;
}
.state.error {
  color: #e50914;
}

/* KPI 卡片行 */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}
.kpi {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 18px 20px;
  background: #1a1a23;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
}
.kpi-label {
  font-size: 13px;
  color: #8a8f98;
}
.kpi-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
  color: #f5f5f7;
}
.kpi-note {
  font-size: 13px;
  color: #9aa0ac;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 图表面板 */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}
.panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 20px;
  background: #1a1a23;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
}
.panel-title {
  font-size: 16px;
  font-weight: 700;
}
.panel-sub {
  margin-left: 6px;
  font-size: 12px;
  font-weight: 400;
  color: #8a8f98;
}
</style>

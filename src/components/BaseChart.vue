<script setup>
// 通用 ECharts 容器：传入 option，负责初始化 / 重绘 / 自适应尺寸 / 销毁
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
// 按需引入（tree-shaking）：只打包用到的图表类型，减小体积
import * as echarts from 'echarts/core'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import { TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  BarChart,
  LineChart,
  PieChart,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  CanvasRenderer
])

const props = defineProps({
  option: { type: Object, required: true },
  height: { type: String, default: '320px' }
})

const chartEl = ref(null)
let chart = null
let resizeObserver = null

function render() {
  if (!chart) return
  // 第二个参数 true = 整体替换（notMerge），避免旧数据残留
  chart.setOption(props.option, true)
}

onMounted(() => {
  chart = echarts.init(chartEl.value)
  render()
  // 容器尺寸变化时自动重绘（比监听 window resize 更精确）
  resizeObserver = new ResizeObserver(() => chart && chart.resize())
  resizeObserver.observe(chartEl.value)
})

// option 变化时重绘（数据异步加载完成后触发）
watch(() => props.option, render, { deep: true })

onBeforeUnmount(() => {
  resizeObserver && resizeObserver.disconnect()
  chart && chart.dispose()
  chart = null
})
</script>

<template>
  <div ref="chartEl" class="base-chart" :style="{ height }"></div>
</template>

<style scoped>
.base-chart {
  width: 100%;
}
</style>

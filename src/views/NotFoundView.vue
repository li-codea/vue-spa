<template>
  <div class="not-found">
    <h1 class="code">404</h1>
    <p class="text">你访问的页面不存在</p>
    <router-link to="/" class="go-home">返回首页</router-link>
  </div>
</template>

<style scoped>
.not-found {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  text-align: center;
}
.code {
  font-size: 72px;
  font-weight: 800;
  color: #2a2a34;
}
.text {
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
</style>

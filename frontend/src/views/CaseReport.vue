<template>
  <div class="page-container">
    <nav class="navbar">
      <div class="nav-brand" @click="router.push('/')">医路达AI创作助手</div>
      <div class="nav-back" @click="router.push('/')">← 返回首页</div>
    </nav>
    <div class="content">
      <span class="orange-tag">病例报告</span>
      <h1 class="title">功能开发中</h1>
      <p class="desc">病例报告生成功能即将上线，敬请期待。</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  background: #fff;
  font-family: 'Noto Sans SC', system-ui, sans-serif;
}

.navbar {
  height: 60px;
  background: #000;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  font-weight: 800;
  font-size: 1.1rem;
  cursor: pointer;
}

.nav-back {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.nav-back:hover {
  opacity: 1;
}

.content {
  max-width: 800px;
  margin: 0 auto;
  padding: 120px 40px;
}

.orange-tag {
  display: inline-block;
  background: #FF4500;
  color: #fff;
  padding: 4px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 1px;
  margin-bottom: 24px;
}

.title {
  font-size: 3rem;
  font-weight: 600;
  margin: 0 0 20px 0;
}

.desc {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.7;
}
</style>

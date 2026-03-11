<template>
  <div class="page-container">
    <nav class="navbar">
      <div class="nav-brand" @click="router.push('/')">医路达AI创作助手</div>
      <div class="nav-back" @click="router.push('/')">← 返回首页</div>
    </nav>
    <div class="content">
      <div class="status-row">
        <span class="status-dot">■</span>
        <span class="status-text">DEVELOPMENT</span>
      </div>
      <h1 class="title">病例报告</h1>
      <p class="desc">该功能正在开发中，敬请期待</p>

      <div class="progress-box">
        <div class="progress-header">
          <span class="diamond-icon">◇</span> 开发进度
        </div>
        <div class="progress-list">
          <div class="progress-item done">
            <span class="item-num">01</span>
            <div class="item-info">
              <div class="item-title">需求设计</div>
              <div class="item-desc">病例报告模板 & 字段规范 & 交互流程</div>
            </div>
            <span class="item-status">✓</span>
          </div>
          <div class="progress-item active">
            <span class="item-num">02</span>
            <div class="item-info">
              <div class="item-title">表单开发</div>
              <div class="item-desc">病例信息录入 & 结构化数据采集</div>
            </div>
            <span class="item-status pulsing">●</span>
          </div>
          <div class="progress-item">
            <span class="item-num">03</span>
            <div class="item-info">
              <div class="item-title">AI 生成引擎</div>
              <div class="item-desc">病例报告智能生成 & 格式适配</div>
            </div>
          </div>
          <div class="progress-item">
            <span class="item-num">04</span>
            <div class="item-info">
              <div class="item-title">审核与导出</div>
              <div class="item-desc">内容审核 & 多格式导出 & 模板管理</div>
            </div>
          </div>
        </div>
      </div>

      <button class="back-btn" @click="router.push('/')">
        <span>返回首页</span>
        <span class="btn-arrow">←</span>
      </button>
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

.nav-back:hover { opacity: 1; }

.content {
  max-width: 600px;
  margin: 0 auto;
  padding: 80px 40px;
}

.status-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: #999;
}

.status-dot {
  color: #FF4500;
  font-size: 0.8rem;
}

.status-text {
  letter-spacing: 2px;
}

.title {
  font-size: 2.4rem;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.desc {
  font-size: 1.05rem;
  color: #666;
  line-height: 1.7;
  margin: 0 0 40px 0;
}

.progress-box {
  border: 1px solid #E5E5E5;
  padding: 30px;
  margin-bottom: 40px;
}

.progress-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.progress-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.progress-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.item-num {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: #000;
  opacity: 0.2;
  flex-shrink: 0;
}

.progress-item.done .item-num {
  opacity: 0.5;
}

.progress-item.active .item-num {
  opacity: 1;
  color: #FF4500;
}

.item-info {
  flex: 1;
}

.item-title {
  font-weight: 520;
  font-size: 1rem;
  margin-bottom: 4px;
}

.progress-item.active .item-title {
  color: #FF4500;
}

.item-desc {
  font-size: 0.85rem;
  color: #666;
}

.item-status {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  color: #999;
  flex-shrink: 0;
}

.progress-item.done .item-status {
  color: #4CAF50;
}

.pulsing {
  color: #FF4500;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.back-btn {
  width: 100%;
  background: #000;
  color: #fff;
  border: none;
  padding: 18px 24px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 0.95rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  letter-spacing: 1px;
  transition: all 0.25s;
}

.back-btn:hover {
  background: #FF4500;
  transform: translateY(-2px);
}

.btn-arrow {
  font-size: 1.2rem;
}

@media (max-width: 640px) {
  .content { padding: 40px 20px; }
  .navbar { padding: 0 20px; }
}
</style>

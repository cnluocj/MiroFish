<template>
  <div class="home-container">
    <div class="main-content">
      <div class="page-header">
        <span class="orange-tag">选择创作类型</span>
        <p class="page-desc">选择文档类型，AI将为您生成专业医学内容</p>
      </div>

      <!-- 卡片入口区域 -->
      <div class="card-grid">
        <!-- 卡片1: 医学科普文章 -->
        <div class="entry-card" @click="router.push('/science-article')">
          <div class="card-index">01</div>
          <div class="card-body">
            <div class="card-icon">◈</div>
            <h2 class="card-title">医学科普文章</h2>
            <p class="card-desc">面向大众的医学知识科普，语言通俗易懂，助力健康传播</p>
          </div>
          <div class="card-footer">
            <span class="card-tag">立即使用</span>
            <span class="card-arrow">→</span>
          </div>
          <div class="card-decoration"></div>
        </div>

        <!-- 卡片2: 病例报告 -->
        <div class="entry-card" @click="router.push('/case-report')">
          <div class="card-index">02</div>
          <div class="card-body">
            <div class="card-icon">◉</div>
            <h2 class="card-title">病例报告</h2>
            <p class="card-desc">规范化病案 Brief 流程，自动生成符合医学规范的病例报告</p>
          </div>
          <div class="card-footer">
            <span class="card-tag">立即使用</span>
            <span class="card-arrow">→</span>
          </div>
          <div class="card-decoration"></div>
        </div>

        <!-- 卡片3: 即将推出 -->
        <div class="entry-card card-disabled">
          <div class="card-index">03</div>
          <div class="card-body">
            <div class="card-icon">◇</div>
            <h2 class="card-title">更多类型</h2>
            <p class="card-desc">更多医学文档生成类型正在开发中，敬请期待</p>
          </div>
          <div class="card-footer">
            <span class="card-tag coming-soon">即将推出</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF4500;
  --gray-light: #F5F5F5;
  --gray-text: #666666;
  --border: #E5E5E5;
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  --font-cn: 'Noto Sans SC', system-ui, sans-serif;
}

.home-container {
  min-height: calc(100vh - var(--site-header-offset));
  background: var(--white);
  font-family: var(--font-sans);
  color: var(--black);
}

/* 主内容区 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 72px 40px 80px;
}

.page-header {
  margin-bottom: 60px;
}

.orange-tag {
  display: inline-block;
  background: var(--orange);
  color: var(--white);
  padding: 4px 10px;
  font-family: var(--font-mono);
  font-weight: 700;
  letter-spacing: 1px;
  font-size: 0.75rem;
  margin-bottom: 20px;
}

.page-desc {
  font-size: 1.1rem;
  color: var(--gray-text);
  margin: 0;
  font-family: var(--font-cn);
}

/* 卡片网格 */
.card-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

/* 单张卡片 */
.entry-card {
  border: 1.5px solid #000;
  padding: 36px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.25s ease;
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-height: 260px;
}

.entry-card:hover:not(.card-disabled) {
  transform: translateY(-4px);
  box-shadow: 6px 6px 0 var(--black);
}

.entry-card:hover:not(.card-disabled) .card-decoration {
  opacity: 1;
}

.entry-card:hover:not(.card-disabled) .card-arrow {
  color: var(--orange);
}


/* 禁用状态 */
.card-disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.card-index {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: #999;
  letter-spacing: 2px;
}

.card-body {
  flex: 1;
}

.card-icon {
  font-size: 1.8rem;
  margin-bottom: 16px;
  color: var(--black);
  line-height: 1;
}

.card-title {
  font-size: 1.6rem;
  font-weight: 600;
  margin: 0 0 12px 0;
  font-family: var(--font-cn);
  letter-spacing: 0px;
}

.card-desc {
  font-size: 0.95rem;
  color: var(--gray-text);
  line-height: 1.7;
  margin: 0;
  font-family: var(--font-cn);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-tag {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--black);
}

.coming-soon {
  color: #999;
}

.card-arrow {
  font-family: var(--font-mono);
  font-size: 1.2rem;
  color: var(--black);
  transition: color 0.2s;
}

/* 卡片右下角装饰块 */
.card-decoration {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 48px;
  height: 48px;
  background: var(--orange);
  opacity: 0;
  transition: opacity 0.25s ease;
  clip-path: polygon(100% 0, 100% 100%, 0 100%);
}

/* 响应式 */
@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: 1fr;
  }

  .main-content {
    padding: 40px 20px;
  }
}
</style>

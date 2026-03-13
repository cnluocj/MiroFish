<template>
  <Teleport to="body">
    <div v-if="visible" class="changelog-overlay" @click.self="$emit('close')">
      <div class="changelog-modal">
        <div class="changelog-header">
          <span class="changelog-title">功能更新日志</span>
          <button class="changelog-close" @click="$emit('close')">&times;</button>
        </div>
        <div class="changelog-body" v-html="rendered"></div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  visible: Boolean,
  content: { type: String, default: '' }
})

defineEmits(['close'])

const rendered = computed(() => {
  if (!props.content) return ''
  return props.content
    .split('\n')
    .map(line => {
      if (/^# /.test(line)) return `<h1>${line.slice(2)}</h1>`
      if (/^## /.test(line)) return `<h2>${line.slice(3)}</h2>`
      if (/^### /.test(line)) return `<h3>${line.slice(4)}</h3>`
      if (/^- /.test(line)) return `<li>${line.slice(2)}</li>`
      if (line.trim() === '') return '<br>'
      return `<p>${line}</p>`
    })
    .join('\n')
})
</script>

<style scoped>
.changelog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.changelog-modal {
  background: #fff;
  width: 600px;
  max-width: 90vw;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  border: 1px solid #E5E5E5;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.changelog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #E5E5E5;
}

.changelog-title {
  font-family: 'Noto Sans SC', system-ui, sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
}

.changelog-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  line-height: 1;
  padding: 0 4px;
  transition: color 0.2s;
}

.changelog-close:hover {
  color: #000;
}

.changelog-body {
  padding: 24px;
  overflow-y: auto;
  font-family: 'Noto Sans SC', system-ui, sans-serif;
  font-size: 0.92rem;
  line-height: 1.8;
  color: #333;
}

.changelog-body :deep(h1) {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0 0 16px;
  color: #000;
}

.changelog-body :deep(h2) {
  font-size: 1.05rem;
  font-weight: 600;
  margin: 20px 0 8px;
  color: #000;
  font-family: 'JetBrains Mono', monospace;
}

.changelog-body :deep(h3) {
  font-size: 0.95rem;
  font-weight: 600;
  margin: 16px 0 6px;
  color: #333;
}

.changelog-body :deep(li) {
  list-style: none;
  position: relative;
  padding-left: 16px;
  margin-bottom: 6px;
}

.changelog-body :deep(li)::before {
  content: '·';
  position: absolute;
  left: 0;
  color: #FF4500;
  font-weight: 700;
}

.changelog-body :deep(p) {
  margin: 4px 0;
}

.changelog-body :deep(br) {
  display: block;
  content: '';
  margin: 4px 0;
}
</style>

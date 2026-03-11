<template>
  <div class="page-container">
    <nav class="navbar">
      <div class="nav-brand" @click="router.push('/')">医路达AI创作助手</div>
      <div class="nav-back" @click="router.push('/')">← 返回首页</div>
    </nav>

    <div class="main-content">
      <div class="page-header">
        <span class="orange-tag">医学科普文章</span>
        <p class="page-desc">填写以下信息，AI 将为您生成专业的医学科普内容</p>
      </div>

      <div class="console-box">
        <!-- 01 目标读者 -->
        <div class="console-section">
          <div class="console-header">
            <span class="console-label">01 / 目标读者</span>
          </div>
          <input
            v-model="form.audience"
            class="text-input"
            placeholder="例：普通患者及家属、中学生群体、社区老年人..."
          />
        </div>

        <div class="console-divider"><span>配置参数</span></div>

        <!-- 02 科室或疾病领域 -->
        <div class="console-section">
          <div class="console-header">
            <span class="console-label">02 / 科室或疾病领域</span>
          </div>
          <select v-model="form.department" class="text-input select-input" @change="onDeptChange">
            <option value="" disabled>请选择科室或领域</option>
            <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
          </select>
          <input
            v-if="form.department === '其他'"
            v-model="form.departmentCustom"
            class="text-input"
            style="margin-top: 10px"
            placeholder="请输入具体科室或疾病领域..."
          />
        </div>

        <div class="console-divider"><span>内容设定</span></div>

        <!-- 03 科普主题 -->
        <div class="console-section">
          <div class="console-header">
            <span class="console-label">>_ 03 / 科普主题</span>
          </div>
          <div class="input-wrapper">
            <textarea
              v-model="form.topic"
              class="code-input"
              placeholder="// 描述您想科普的具体主题（例：高血压患者的日常饮食管理与用药注意事项）"
              rows="5"
            ></textarea>
          </div>
        </div>

        <div class="console-divider"><span>风格设定</span></div>

        <!-- 04 文章调性 -->
        <div class="console-section">
          <div class="console-header">
            <span class="console-label">04 / 文章调性</span>
          </div>
          <div class="radio-group">
            <label
              v-for="tone in tones"
              :key="tone.value"
              class="radio-item"
              :class="{ active: form.tone === tone.value }"
            >
              <input type="radio" v-model="form.tone" :value="tone.value" />
              <span class="radio-label">{{ tone.label }}</span>
              <span class="radio-desc">{{ tone.desc }}</span>
            </label>
          </div>
        </div>

        <div class="console-divider"><span>输出配置</span></div>

        <!-- 05 期望字数 -->
        <div class="console-section">
          <div class="console-header">
            <span class="console-label">05 / 期望字数</span>
            <span class="console-meta">{{ form.wordCount }} 字</span>
          </div>
          <div class="slider-wrapper">
            <span class="slider-bound">500</span>
            <input
              type="range"
              v-model.number="form.wordCount"
              min="500"
              max="5000"
              step="100"
              class="range-slider"
            />
            <span class="slider-bound">5000</span>
          </div>
          <div class="slider-ticks">
            <span>短文</span>
            <span>中篇</span>
            <span>长文</span>
          </div>
        </div>

        <div class="console-divider"><span>参考资料</span></div>

        <!-- 06 参考材料 -->
        <div class="console-section">
          <div class="console-header">
            <span class="console-label">06 / 参考材料</span>
            <span class="console-meta">支持格式: PDF, MD, TXT, DOCX</span>
          </div>
          <div
            class="upload-zone"
            :class="{ 'drag-over': isDragOver, 'has-files': form.files.length > 0 }"
            @dragover.prevent="isDragOver = true"
            @dragleave.prevent="isDragOver = false"
            @drop.prevent="handleDrop"
            @click="fileInput?.click()"
          >
            <input
              ref="fileInput"
              type="file"
              multiple
              accept=".pdf,.md,.txt,.docx"
              style="display: none"
              @change="handleFileSelect"
            />
            <div v-if="form.files.length === 0" class="upload-placeholder">
              <div class="upload-icon">↑</div>
              <div class="upload-title">拖拽文件上传</div>
              <div class="upload-hint">或点击浏览文件系统（可选）</div>
            </div>
            <div v-else class="file-list">
              <div v-for="(file, index) in form.files" :key="index" class="file-item">
                <span class="file-icon">📄</span>
                <span class="file-name">{{ file.name }}</span>
                <button @click.stop="form.files.splice(index, 1)" class="remove-btn">×</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="console-section btn-section">
          <button class="start-btn" :disabled="!canSubmit" @click="handleSubmit">
            <span>开始生成</span>
            <span class="btn-arrow">→</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const fileInput = ref(null)
const isDragOver = ref(false)

const departments = [
  '心内科', '神经内科', '呼吸内科', '消化内科', '内分泌科',
  '骨科', '妇产科', '儿科', '肿瘤科', '皮肤科', '眼科', '口腔科', '其他'
]

const tones = [
  { value: 'popular', label: '通俗易懂', desc: '面向大众，语言生动简洁' },
  { value: 'professional', label: '专业严谨', desc: '面向医疗从业者，术语规范' }
]

const form = ref({
  audience: '',
  department: '',
  departmentCustom: '',
  topic: '',
  tone: 'popular',
  wordCount: 1500,
  files: []
})

const onDeptChange = () => {
  if (form.value.department !== '其他') {
    form.value.departmentCustom = ''
  }
}

const canSubmit = computed(() => {
  return form.value.audience.trim() !== '' &&
    form.value.department !== '' &&
    form.value.topic.trim() !== ''
})

const addFiles = (rawFiles) => {
  const valid = Array.from(rawFiles).filter(f => {
    const ext = f.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt', 'docx'].includes(ext)
  })
  form.value.files.push(...valid)
}

const handleFileSelect = (e) => addFiles(e.target.files)

const handleDrop = (e) => {
  isDragOver.value = false
  addFiles(e.dataTransfer.files)
}

const handleSubmit = () => {
  if (!canSubmit.value) return
  alert('功能开发中，敬请期待！')
}
</script>

<style scoped>
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF4500;
  --gray-text: #666666;
  --border: #E5E5E5;
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  --font-cn: 'Noto Sans SC', system-ui, sans-serif;
}

.page-container {
  min-height: 100vh;
  background: #fff;
  font-family: var(--font-sans);
  color: #000;
}

/* 导航 */
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
  font-family: var(--font-cn);
  font-weight: 800;
  font-size: 1.1rem;
  cursor: pointer;
}

.nav-back {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.nav-back:hover { opacity: 1; }

/* 主内容 */
.main-content {
  max-width: 860px;
  margin: 0 auto;
  padding: 60px 40px 100px;
}

.page-header {
  margin-bottom: 40px;
}

.orange-tag {
  display: inline-block;
  background: #FF4500;
  color: #fff;
  padding: 4px 10px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.page-desc {
  font-size: 1rem;
  color: var(--gray-text);
  margin: 0;
  font-family: var(--font-cn);
}

/* console-box */
.console-box {
  border: 1px solid #CCC;
  padding: 8px;
}

.console-section {
  padding: 24px 24px 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #666;
}

.console-meta {
  color: #999;
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 4px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #EEE;
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #BBB;
  letter-spacing: 1px;
}

/* 文本输入 */
.text-input {
  width: 100%;
  border: 1px solid #DDD;
  background: #FAFAFA;
  padding: 12px 16px;
  font-family: var(--font-cn);
  font-size: 0.95rem;
  outline: none;
  box-sizing: border-box;
  color: #000;
  transition: border-color 0.2s;
}

.text-input:focus {
  border-color: #000;
  background: #fff;
}

.select-input {
  appearance: none;
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%23666' stroke-width='1.5' fill='none'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 40px;
}

/* textarea */
.input-wrapper {
  border: 1px solid #DDD;
  background: #FAFAFA;
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 16px 20px;
  font-family: var(--font-mono);
  font-size: 0.88rem;
  line-height: 1.7;
  resize: vertical;
  outline: none;
  box-sizing: border-box;
  color: #000;
}

/* 单选组 */
.radio-group {
  display: flex;
  gap: 16px;
}

.radio-item {
  flex: 1;
  border: 1.5px solid #DDD;
  padding: 16px 20px;
  cursor: pointer;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: border-color 0.2s, background 0.2s;
}

.radio-item.active {
  border-color: #000;
  background: #FAFAFA;
}

.radio-item input[type="radio"] {
  margin-top: 3px;
  accent-color: #000;
  flex-shrink: 0;
}

.radio-label {
  font-family: var(--font-cn);
  font-weight: 600;
  font-size: 0.95rem;
  display: block;
}

.radio-desc {
  font-family: var(--font-cn);
  font-size: 0.8rem;
  color: #999;
  display: block;
  margin-top: 4px;
}

.radio-item > span {
  display: flex;
  flex-direction: column;
}

/* 滑动条 */
.slider-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.slider-bound {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #999;
  white-space: nowrap;
}

.range-slider {
  flex: 1;
  height: 2px;
  accent-color: #000;
  cursor: pointer;
  outline: none;
}

.slider-ticks {
  display: flex;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #BBB;
  padding: 0 36px;
}

/* 上传区 */
.upload-zone {
  border: 1px dashed #CCC;
  min-height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: #FAFAFA;
  transition: all 0.2s;
}

.upload-zone.drag-over {
  border-color: #000;
  background: #F0F0F0;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  border-color: #999;
  background: #F5F5F5;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 36px;
  height: 36px;
  border: 1px solid #DDD;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  color: #999;
}

.upload-title {
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 4px;
  font-family: var(--font-cn);
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: #999;
}

.file-list {
  width: 100%;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-item {
  display: flex;
  align-items: center;
  background: #fff;
  padding: 8px 12px;
  border: 1px solid #EEE;
  font-family: var(--font-mono);
  font-size: 0.83rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  color: #999;
  line-height: 1;
}

/* 提交按钮 */
.start-btn {
  width: 100%;
  background: #000;
  color: #fff;
  border: none;
  padding: 20px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  letter-spacing: 1px;
  transition: all 0.25s;
}

.start-btn:not(:disabled):hover {
  background: #FF4500;
  transform: translateY(-2px);
}

.start-btn:disabled {
  background: #E5E5E5;
  color: #999;
  cursor: not-allowed;
}

.btn-arrow {
  font-size: 1.2rem;
}

/* 响应式 */
@media (max-width: 640px) {
  .main-content { padding: 40px 16px 80px; }
  .radio-group { flex-direction: column; }
  .navbar { padding: 0 20px; }
}
</style>

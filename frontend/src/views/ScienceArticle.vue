<template>
  <div class="page-container">
    <nav class="navbar">
      <div class="nav-brand" @click="router.push('/')">医路达AI创作助手</div>
      <div class="nav-back" @click="router.push('/')">← 返回首页</div>
    </nav>

    <div class="dashboard-section">
      <!-- 左栏：状态与工作流 -->
      <div class="left-panel">
        <div class="panel-header" @click="handleStatusClick" style="cursor: default; user-select: none;">
          <span class="status-dot">■</span> 系统状态
        </div>
        <ChangelogModal
          :visible="showChangelog"
          :content="changelogContent"
          @close="showChangelog = false"
        />

        <h2 class="section-title">准备就绪</h2>
        <p class="section-desc">
          AI 创作引擎待命中，填写右侧参数即可启动医学科普文章生成
        </p>

        <!-- 数据指标卡片 -->
        <div class="metrics-row">
          <div class="metric-card">
            <div class="metric-value">智能创作</div>
            <div class="metric-label">AI驱动 多轮润色</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">专业可靠</div>
            <div class="metric-label">医学知识图谱支撑</div>
          </div>
        </div>

        <!-- 工作流步骤 -->
        <div class="steps-container">
          <div class="steps-header">
            <span class="diamond-icon">◇</span> 工作流序列
          </div>
          <div class="workflow-list">
            <div class="workflow-item" :class="{ active: currentWorkflowStep === 0 }">
              <span class="step-num">01</span>
              <div class="step-info">
                <div class="step-title">参数配置</div>
                <div class="step-desc">目标读者 & 科室领域 & 主题设定 & 风格字数</div>
              </div>
            </div>
            <div class="workflow-item" :class="{ active: currentWorkflowStep === 1 }">
              <span class="step-num">02</span>
              <div class="step-info">
                <div class="step-title">文献检索</div>
                <div class="step-desc">自动检索相关医学文献 & 权威指南 & 循证依据</div>
              </div>
            </div>
            <div class="workflow-item" :class="{ active: currentWorkflowStep === 2 }">
              <span class="step-num">03</span>
              <div class="step-info">
                <div class="step-title">知识整合</div>
                <div class="step-desc">构建领域知识图谱 & 提取核心观点 & 素材整理</div>
              </div>
            </div>
            <div class="workflow-item" :class="{ active: currentWorkflowStep === 3 }">
              <span class="step-num">04</span>
              <div class="step-info">
                <div class="step-title">大纲规划</div>
                <div class="step-desc">智能生成文章结构 & 段落规划 & 逻辑梳理</div>
              </div>
            </div>
            <div class="workflow-item" :class="{ active: currentWorkflowStep === 4 }">
              <span class="step-num">05</span>
              <div class="step-info">
                <div class="step-title">内容创作</div>
                <div class="step-desc">逐段生成内容 & Markdown 渲染 & 实时预览</div>
              </div>
            </div>
            <div class="workflow-item" :class="{ active: currentWorkflowStep === 5 }">
              <span class="step-num">06</span>
              <div class="step-info">
                <div class="step-title">深度互动</div>
                <div class="step-desc">与 AI 对话优化内容 & 调整润色 & 导出成稿</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右栏：表单控制台 -->
      <div class="right-panel">
        <div class="console-box">
          <!-- 01 目标读者 -->
          <div class="console-section">
            <div class="console-header">
              <span class="console-label">01 / 目标读者</span>
            </div>
            <div class="radio-group">
              <label
                v-for="aud in audiences"
                :key="aud.value"
                class="radio-item compact"
                :class="{ active: form.audience === aud.value }"
              >
                <input type="radio" v-model="form.audience" :value="aud.value" />
                <span class="radio-label">{{ aud.label }}</span>
              </label>
            </div>
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
            <button class="start-btn" :disabled="!canSubmit || isSubmitting" @click="handleSubmit">
              <span>{{ isSubmitting ? '启动中...' : '开始生成' }}</span>
              <span class="btn-arrow">→</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { generateArticle } from '../api/article'
import { setArticleForm } from '../store/articleForm'
import changelogContent from '../changelogs/science-article.md?raw'
import ChangelogModal from '../components/ChangelogModal.vue'

const router = useRouter()
const fileInput = ref(null)
const isDragOver = ref(false)
const currentWorkflowStep = ref(0)
const isSubmitting = ref(false)
const showChangelog = ref(false)
let clickCount = 0
let clickTimer = null

const handleStatusClick = () => {
  clickCount++
  clearTimeout(clickTimer)
  if (clickCount >= 3) {
    clickCount = 0
    showChangelog.value = true
  } else {
    clickTimer = setTimeout(() => { clickCount = 0 }, 500)
  }
}

const audiences = [
  { value: 'general', label: '普通大众' },
  { value: 'patient', label: '患者及家属' },
  { value: 'professional', label: '医护同行' }
]

const departments = [
  '心内科', '神经内科', '呼吸内科', '消化内科', '内分泌科',
  '骨科', '妇产科', '儿科', '肿瘤科', '皮肤科', '眼科', '口腔科', '其他'
]

const topicSuggestions = {
  '心内科': '冠心病患者的日常管理：从饮食控制到规律运动的科学指南',
  '神经内科': '偏头痛的识别与应对：了解触发因素，掌握缓解方法',
  '呼吸内科': '慢性阻塞性肺疾病（COPD）的早期识别与居家管理',
  '消化内科': '胃食管反流病的生活方式调整与用药注意事项',
  '内分泌科': '糖尿病患者的血糖监测与饮食管理实用指南',
  '骨科': '腰椎间盘突出症的保守治疗与日常预防策略',
  '妇产科': '孕期营养管理：不同孕周的膳食搭配与营养补充',
  '儿科': '儿童常见发热的家庭护理与就医时机判断',
  '肿瘤科': '癌症筛查指南：哪些检查项目适合您的年龄段',
  '皮肤科': '湿疹的日常护理与用药管理：从保湿到规范治疗',
  '眼科': '青少年近视防控：科学用眼习惯与矫正方案选择',
  '口腔科': '牙周病的早期信号与预防：不只是刷牙那么简单'
}

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
  // 自动填充科普主题（每次切换科室都更新）
  if (form.value.department && form.value.department !== '其他') {
    form.value.topic = topicSuggestions[form.value.department] || ''
  }
}

const canSubmit = computed(() => {
  return form.value.audience !== '' &&
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

const handleSubmit = async () => {
  if (!canSubmit.value) return
  if (isSubmitting.value) return

  const payload = {
    ...form.value,
    department: form.value.department === '其他' ? form.value.departmentCustom.trim() : form.value.department,
    referenceMaterials: form.value.files.map(file => file.name)
  }

  try {
    isSubmitting.value = true
    setArticleForm(payload)
    const response = await generateArticle(payload)
    const articleId = response?.data?.article_id

    if (!articleId) {
      throw new Error('后端未返回 article_id')
    }

    router.push({ name: 'ArticleGenerate', params: { taskId: articleId } })
  } catch (error) {
    console.error('启动文章生成失败:', error)
    window.alert(error?.message || '启动文章生成失败，请检查后端服务或 LLM 配置')
  } finally {
    isSubmitting.value = false
  }
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
  min-height: calc(100vh - var(--site-header-offset));
  background: #fff;
  font-family: var(--font-sans);
  color: #000;
}

/* 导航 */
.navbar {
  height: 60px;
  background: #fff;
  color: #111827;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  border-bottom: 1px solid #E5E7EB;
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
  color: #6B7280;
  transition: color 0.2s;
}

.nav-back:hover { color: #111827; }

/* 双栏布局 */
.dashboard-section {
  display: flex;
  max-width: 1300px;
  margin: 0 auto;
  padding: 60px 40px 100px;
  gap: 50px;
  align-items: flex-start;
}

/* 左侧面板 */
.left-panel {
  flex: 0.8;
  position: sticky;
  top: calc(var(--site-header-offset) + 20px);
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: var(--orange);
  font-size: 0.8rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 520;
  margin: 0 0 15px 0;
}

.section-desc {
  color: var(--gray-text);
  margin-bottom: 25px;
  line-height: 1.6;
  font-family: var(--font-cn);
}

.metrics-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric-card {
  border: 1px solid var(--border);
  padding: 20px 30px;
  min-width: 130px;
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.4rem;
  font-weight: 520;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 0.8rem;
  color: #999;
  font-family: var(--font-cn);
}

/* 工作流步骤 */
.steps-container {
  border: 1px solid var(--border);
  padding: 30px;
  position: relative;
}

.steps-header {
  font-family: var(--font-mono);
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

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  transition: all 0.3s;
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 700;
  color: #000;
  opacity: 0.3;
  flex-shrink: 0;
}

.workflow-item.active .step-num {
  opacity: 1;
  color: var(--orange);
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 520;
  font-size: 1rem;
  margin-bottom: 4px;
  font-family: var(--font-cn);
}

.workflow-item.active .step-title {
  color: var(--orange);
}

.step-desc {
  font-size: 0.85rem;
  color: var(--gray-text);
  font-family: var(--font-cn);
}

/* 右栏 */
.right-panel {
  flex: 1.2;
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
  gap: 12px;
}

.radio-item {
  flex: 1;
  border: 1.5px solid #DDD;
  padding: 14px 16px;
  cursor: pointer;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  transition: border-color 0.2s, background 0.2s;
}

.radio-item.compact {
  align-items: center;
  padding: 12px 16px;
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
  font-size: 0.9rem;
  display: block;
}

.radio-desc {
  font-family: var(--font-cn);
  font-size: 0.75rem;
  color: #999;
  display: block;
  margin-top: 3px;
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
  min-height: 120px;
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
@media (max-width: 900px) {
  .dashboard-section {
    flex-direction: column;
    padding: 40px 20px 80px;
    gap: 40px;
  }
  .left-panel {
    position: static;
  }
  .radio-group {
    flex-direction: column;
  }
  .navbar { padding: 0 20px; }
  .metrics-row { flex-direction: column; }
}
</style>

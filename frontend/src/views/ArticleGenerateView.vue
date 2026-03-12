<template>
  <div class="main-view">
    <!-- Header -->
    <header class="app-header">
      <div class="header-left">
        <div class="brand" @click="router.push('/')">医路达AI创作助手</div>
        <span class="back-link" @click="router.push('/science-article')">← 返回</span>
      </div>

      <div class="header-center">
        <div class="view-switcher">
          <button
            v-for="m in [{ key: 'article', label: '文章' }, { key: 'split', label: '双栏' }, { key: 'workbench', label: '工作台' }]"
            :key="m.key"
            class="switch-btn"
            :class="{ active: viewMode === m.key }"
            @click="viewMode = m.key"
          >{{ m.label }}</button>
        </div>
      </div>

      <div class="header-right">
        <div class="workflow-step">
          <span class="step-num mono">{{ isComplete && rightMode === 'chat' ? 'Step 2/2' : 'Step 1/2' }}</span>
          <span class="step-name">{{ isComplete && rightMode === 'chat' ? '深度互动' : '文章生成' }}</span>
        </div>
        <div class="step-divider"></div>
        <span class="status-indicator" :class="statusClass">
          <span class="dot"></span>
          {{ statusText }}
        </span>
      </div>
    </header>

    <!-- Main Content -->
    <main class="content-area">
      <!-- Left: Article Panel -->
      <div class="panel-wrapper left" :style="leftPanelStyle">
        <div class="article-panel" ref="leftPanel">
          <!-- Waiting State -->
          <div v-if="!outline" class="waiting-placeholder">
            <div class="waiting-animation">
              <div class="waiting-ring"></div>
              <div class="waiting-ring"></div>
              <div class="waiting-ring"></div>
            </div>
            <span class="waiting-text">Waiting for Article Agent...</span>
          </div>

          <!-- Article Content -->
          <div v-else class="report-content-wrapper">
            <div class="report-header-block">
              <div class="report-meta">
                <span class="report-tag">{{ formData?.department || '医学科普' }}</span>
                <span class="report-tag tone-tag">{{ formData?.tone === 'professional' ? '专业严谨' : '通俗易懂' }}</span>
                <span class="report-id">约 {{ formData?.wordCount || 1500 }} 字</span>
              </div>
              <h1 class="main-title">{{ outline.title }}</h1>
              <p class="sub-title">{{ outline.summary }}</p>
              <div class="header-divider"></div>
            </div>

            <div class="sections-list">
              <div
                v-for="(section, idx) in outline.sections"
                :key="idx"
                class="report-section-item"
                :class="{
                  'is-active': currentSectionIndex === idx && !generatedSections[idx],
                  'is-completed': !!generatedSections[idx],
                  'is-pending': !generatedSections[idx] && currentSectionIndex !== idx
                }"
              >
                <div
                  class="section-header-row"
                  :class="{ clickable: !!generatedSections[idx] }"
                  @click="toggleSection(idx)"
                >
                  <span class="section-number mono">{{ String(idx + 1).padStart(2, '0') }}</span>
                  <h3 class="section-title">{{ section.title }}</h3>
                  <svg
                    v-if="generatedSections[idx]"
                    class="collapse-icon"
                    :class="{ 'is-collapsed': collapsedSections.has(idx) }"
                    viewBox="0 0 24 24" width="20" height="20"
                    fill="none" stroke="currentColor" stroke-width="2"
                  >
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </div>

                <div class="section-body" v-show="!collapsedSections.has(idx)">
                  <div v-if="generatedSections[idx]" class="generated-content" v-html="renderMarkdown(generatedSections[idx])"></div>
                  <div v-else-if="currentSectionIndex === idx" class="loading-state">
                    <div class="loading-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <circle cx="12" cy="12" r="10" stroke-width="4" stroke="#E5E7EB"></circle>
                        <path d="M12 2a10 10 0 0 1 10 10" stroke-width="4" stroke="#4B5563" stroke-linecap="round"></path>
                      </svg>
                    </div>
                    <span class="loading-text">正在生成{{ section.title }}...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Timeline / Chat -->
      <div class="panel-wrapper right" :style="rightPanelStyle">
        <div class="right-panel">
          <!-- Timeline Mode -->
          <template v-if="rightMode === 'timeline'">
            <!-- Panel Header -->
            <div v-if="!isComplete" class="panel-header" :class="`panel-header--${activeStepStatus}`">
              <span v-if="activeStepStatus === 'active'" class="header-dot"></span>
              <span class="header-index mono">{{ activeStepLabel }}</span>
              <span class="header-title">{{ activeStepTitle }}</span>
            </div>

            <!-- Workflow Overview -->
            <div class="workflow-overview" v-if="timeline.length > 0 || outline">
              <div class="workflow-metrics">
                <div class="metric">
                  <span class="metric-label">SECTIONS</span>
                  <span class="metric-value mono">{{ completedSections }}/{{ totalSections }}</span>
                </div>
                <div class="metric">
                  <span class="metric-label">ELAPSED</span>
                  <span class="metric-value mono">{{ elapsedTime }}</span>
                </div>
                <div class="metric metric-right">
                  <span class="metric-pill" :class="`pill--${statusClass}`">{{ statusText }}</span>
                </div>
              </div>

              <!-- Step Tree -->
              <div class="workflow-steps">
                <div
                  class="wf-step"
                  :class="`wf-step--${outline ? 'done' : (timeline.length > 0 ? 'active' : 'todo')}`"
                >
                  <div class="wf-step-connector">
                    <div class="wf-step-dot"></div>
                    <div class="wf-step-line"></div>
                  </div>
                  <div class="wf-step-content">
                    <div class="wf-step-title-row">
                      <span class="wf-step-index mono">PL</span>
                      <span class="wf-step-title">规划大纲</span>
                    </div>
                  </div>
                </div>

                <template v-if="outline">
                  <div
                    v-for="(section, idx) in outline.sections"
                    :key="idx"
                    class="wf-step"
                    :class="`wf-step--${generatedSections[idx] ? 'done' : (currentSectionIndex === idx && !generatedSections[idx] ? 'active' : 'todo')}`"
                  >
                    <div class="wf-step-connector">
                      <div class="wf-step-dot"></div>
                      <div class="wf-step-line" v-if="idx < outline.sections.length - 1 || !isComplete"></div>
                    </div>
                    <div class="wf-step-content">
                      <div class="wf-step-title-row">
                        <span class="wf-step-index mono">{{ String(idx + 1).padStart(2, '0') }}</span>
                        <span class="wf-step-title">{{ section.title }}</span>
                        <span v-if="currentSectionIndex === idx && !generatedSections[idx]" class="wf-step-meta mono">ACTIVE</span>
                      </div>
                    </div>
                  </div>
                </template>

                <div class="wf-step" :class="`wf-step--${isComplete ? 'done' : 'todo'}`">
                  <div class="wf-step-connector">
                    <div class="wf-step-dot"></div>
                  </div>
                  <div class="wf-step-content">
                    <div class="wf-step-title-row">
                      <span class="wf-step-index mono">OK</span>
                      <span class="wf-step-title">生成完成</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Next Step Button -->
              <button v-if="isComplete" class="next-step-btn" @click="rightMode = 'chat'">
                <span>进入深度互动</span>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </button>

              <div class="workflow-divider"></div>
            </div>

            <!-- Timeline -->
            <div class="workflow-timeline" ref="timelineContainer">
              <div v-for="(entry, idx) in timeline" :key="idx" class="timeline-item" :class="`node--${entry.type === 'success' ? 'done' : (entry.type === 'active' ? 'active' : '')}`">
                <div class="timeline-connector">
                  <div class="connector-dot" :class="`dot-${entry.type === 'success' ? 'done' : (entry.type === 'active' ? 'active' : 'muted')}`"></div>
                  <div class="connector-line" v-if="idx < timeline.length - 1"></div>
                </div>
                <div class="timeline-content">
                  <div class="timeline-header">
                    <span class="action-label">{{ entry.label }}</span>
                    <span class="action-time mono">{{ entry.time }}</span>
                  </div>
                  <div v-if="entry.detail" class="timeline-body">
                    <div class="status-message" :class="entry.type === 'success' ? 'success' : 'planning'">{{ entry.detail }}</div>
                  </div>
                </div>
              </div>

              <div v-if="timeline.length === 0" class="timeline-empty">
                等待 Agent 开始工作...
              </div>
            </div>
          </template>

          <!-- Chat Mode -->
          <template v-else>
            <div class="chat-header">
              <button class="back-to-timeline" @click="rightMode = 'timeline'">← 生成记录</button>
              <span class="chat-title">深度互动</span>
            </div>

            <div class="chat-messages" ref="chatContainer">
              <div v-if="chatHistory.length === 0" class="chat-empty">
                <div class="waiting-animation small">
                  <div class="waiting-ring"></div>
                  <div class="waiting-ring"></div>
                </div>
                <div class="chat-empty-text">您可以就生成的文章向 AI 提问、要求修改或深入讨论</div>
              </div>
              <div
                v-for="(msg, idx) in chatHistory"
                :key="idx"
                class="chat-msg"
                :class="msg.role"
              >
                <div class="msg-header">
                  <span class="msg-name">{{ msg.role === 'user' ? '您' : 'AI 助手' }}</span>
                  <span class="msg-time mono">{{ msg.time }}</span>
                </div>
                <div class="msg-body" v-html="msg.role === 'assistant' ? renderMarkdown(msg.content) : escapeHtml(msg.content)"></div>
              </div>
              <div v-if="isSending" class="chat-msg assistant">
                <div class="msg-header"><span class="msg-name">AI 助手</span></div>
                <div class="msg-body typing">
                  <div class="loading-icon small">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <circle cx="12" cy="12" r="10" stroke-width="4" stroke="#E5E7EB"></circle>
                      <path d="M12 2a10 10 0 0 1 10 10" stroke-width="4" stroke="#4B5563" stroke-linecap="round"></path>
                    </svg>
                  </div>
                  <span>思考中...</span>
                </div>
              </div>
            </div>

            <div class="chat-input-area">
              <textarea
                v-model="chatInput"
                class="chat-textarea"
                placeholder="输入您的问题或修改建议..."
                rows="2"
                @keydown.enter.exact.prevent="sendMessage"
              ></textarea>
              <button
                class="send-btn"
                :disabled="!chatInput.trim() || isSending"
                @click="sendMessage"
              >发送</button>
            </div>
          </template>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { getArticleForm } from '../store/articleForm'

const router = useRouter()
const formData = ref(getArticleForm())

// Layout
const viewMode = ref('split')
const rightMode = ref('timeline')

// Generation state
const outline = ref(null)
const generatedSections = ref({})
const currentSectionIndex = ref(null)
const isComplete = ref(false)
const collapsedSections = ref(new Set())
const timeline = ref([])
const startTime = ref(null)
const elapsedSeconds = ref(0)

// Chat state
const chatHistory = ref([])
const chatInput = ref('')
const isSending = ref(false)
const chatContainer = ref(null)
const timelineContainer = ref(null)
const leftPanel = ref(null)

// Timers
let timers = []
let elapsedTimer = null

// --- Computed ---
const totalSections = computed(() => outline.value?.sections?.length || 0)
const completedSections = computed(() => Object.keys(generatedSections.value).length)
const progressPercent = computed(() => {
  if (!totalSections.value) return 0
  return Math.round((completedSections.value / totalSections.value) * 100)
})

const statusClass = computed(() => isComplete.value ? 'completed' : 'processing')
const statusText = computed(() => {
  if (isComplete.value) return 'COMPLETED'
  if (outline.value) return 'GENERATING'
  return 'PLANNING'
})

const elapsedTime = computed(() => {
  const s = elapsedSeconds.value
  const min = Math.floor(s / 60)
  const sec = s % 60
  return min > 0 ? `${min}m ${sec}s` : `${sec}s`
})

// Active step for panel header
const activeStepStatus = computed(() => {
  if (isComplete.value) return 'done'
  return 'active'
})

const activeStepLabel = computed(() => {
  if (!outline.value) return 'PL'
  if (currentSectionIndex.value !== null) return String(currentSectionIndex.value + 1).padStart(2, '0')
  return 'PL'
})

const activeStepTitle = computed(() => {
  if (!outline.value) return '规划大纲'
  if (currentSectionIndex.value !== null && outline.value.sections[currentSectionIndex.value]) {
    return outline.value.sections[currentSectionIndex.value].title
  }
  return '规划大纲'
})

const leftPanelStyle = computed(() => {
  if (viewMode.value === 'article') return { width: '100%', opacity: 1, transform: 'translateX(0)' }
  if (viewMode.value === 'workbench') return { width: '0%', opacity: 0, transform: 'translateX(-20px)' }
  return { width: '50%', opacity: 1, transform: 'translateX(0)' }
})

const rightPanelStyle = computed(() => {
  if (viewMode.value === 'workbench') return { width: '100%', opacity: 1, transform: 'translateX(0)' }
  if (viewMode.value === 'article') return { width: '0%', opacity: 0, transform: 'translateX(20px)' }
  return { width: '50%', opacity: 1, transform: 'translateX(0)' }
})

// --- Methods ---
const toggleSection = (idx) => {
  if (!generatedSections.value[idx]) return
  const s = new Set(collapsedSections.value)
  s.has(idx) ? s.delete(idx) : s.add(idx)
  collapsedSections.value = s
}

const getTimeStr = () => {
  const now = new Date()
  return now.toLocaleTimeString('zh-CN', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

const addTimeline = (type, label, detail = '') => {
  timeline.value.push({ type, label, detail, time: getTimeStr() })
  nextTick(() => {
    if (timelineContainer.value) {
      timelineContainer.value.scrollTop = timelineContainer.value.scrollHeight
    }
  })
}

// --- Mock Generation ---
const buildMockOutline = () => {
  const topic = formData.value?.topic || '医学科普'
  const audience = formData.value?.audience || '普通读者'
  const toneLabel = formData.value?.tone === 'professional' ? '专业严谨，术语规范' : '通俗易懂，贴近生活'

  return {
    title: topic,
    summary: `本文围绕"${topic}"这一主题，面向${audience}，从基础概念、核心知识、实践建议和常见误区四个维度展开科普。内容力求${toneLabel}，帮助读者建立科学的健康认知。`,
    sections: [
      { title: '引言与背景', description: '简介主题的重要性和现状' },
      { title: '核心知识解析', description: '深入讲解关键医学知识' },
      { title: '实践与建议', description: '给出具体的生活指导' },
      { title: '常见误区与注意事项', description: '澄清认知偏差' },
      { title: '总结与展望', description: '全文总结与进一步建议' }
    ]
  }
}

const buildMockContents = () => {
  const topic = formData.value?.topic || '该疾病'
  const dept = formData.value?.department || '相关科室'

  return [
    `近年来，随着人们健康意识的提高，关于"${topic}"的讨论越来越受到关注。据${dept}临床数据显示，相关健康问题的发病率呈逐年上升趋势，已成为不容忽视的公共卫生议题。\n\n本文将从专业角度出发，为您系统梳理这一领域的核心知识，帮助您建立科学、正确的健康认知。\n\n> 健康科普的目标不是制造焦虑，而是帮助每个人成为自己健康的第一责任人。`,

    `### 基本概念\n\n要理解${topic}，首先需要了解其基本的医学原理。从${dept}的角度来看，这涉及到人体多个系统的协调运作。\n\n### 发病机制\n\n目前医学研究表明，相关疾病的发生往往与以下因素有关：\n\n- **遗传因素**：家族史是重要的风险评估指标\n- **环境因素**：生活方式、饮食习惯、职业暴露等\n- **年龄因素**：不同年龄段的发病特点有所差异\n\n### 诊断标准\n\n临床上通常依据以下指标进行综合评估，建议定期进行相关检查。`,

    `### 生活方式调整\n\n科学的生活方式是预防和管理的基础：\n\n1. **合理膳食**：注重营养均衡，控制总热量摄入\n2. **适度运动**：建议每周进行 150 分钟以上的中等强度有氧运动\n3. **规律作息**：保证充足睡眠，避免熬夜\n4. **情绪管理**：保持积极心态，学会压力调节\n\n### 就医指导\n\n出现以下情况时，建议及时到${dept}就诊：\n\n- 症状持续加重或反复发作\n- 常规措施无法有效控制\n- 出现新的异常症状`,

    `### 误区一：没有症状就不需要关注\n\n许多疾病在早期可能没有明显症状，但这并不意味着可以忽视。定期体检和筛查对于早期发现、早期干预至关重要。\n\n### 误区二：偏方和保健品可以替代正规治疗\n\n目前没有科学证据表明偏方或保健品能够替代经过临床验证的正规治疗方案。生病后应及时就医，遵医嘱用药。\n\n### 误区三：治疗效果好了就可以自行停药\n\n擅自停药或减量可能导致病情反复甚至加重。用药调整应在医生指导下进行。\n\n> **提醒**：任何治疗方案的调整都应咨询专业医生，切勿自行决定。`,

    `${topic}是一个需要长期关注和科学管理的健康议题。通过本文的介绍，希望读者能够：\n\n1. 建立对该领域的基本认知\n2. 掌握科学的预防和管理方法\n3. 避免常见的认知误区\n4. 在需要时及时寻求专业医疗帮助\n\n健康管理是一场马拉松，需要耐心和坚持。祝您身体健康！\n\n---\n\n*本文仅供科普参考，具体诊疗方案请咨询${dept}专业医生。*`
  ]
}

const startMockGeneration = () => {
  startTime.value = Date.now()
  elapsedTimer = setInterval(() => {
    elapsedSeconds.value = Math.floor((Date.now() - startTime.value) / 1000)
  }, 1000)

  timers.push(setTimeout(() => {
    addTimeline('info', '初始化生成引擎')
    addTimeline('info', `读取表单参数`, `主题: "${formData.value?.topic || '未设置'}"`)
  }, 300))

  timers.push(setTimeout(() => {
    addTimeline('active', '开始规划文章大纲...')
  }, 800))

  timers.push(setTimeout(() => {
    outline.value = buildMockOutline()
    addTimeline('success', '大纲规划完成', `共 ${outline.value.sections.length} 个章节`)
    generateNextSection(0)
  }, 2500))
}

const generateNextSection = (index) => {
  const sections = outline.value.sections
  const contents = buildMockContents()

  if (index >= sections.length) {
    timers.push(setTimeout(() => {
      isComplete.value = true
      currentSectionIndex.value = null
      clearInterval(elapsedTimer)
      addTimeline('success', '文章生成完成', '所有章节已生成，可进入深度互动')
    }, 500))
    return
  }

  currentSectionIndex.value = index
  addTimeline('active', `正在生成: ${sections[index].title}`)

  timers.push(setTimeout(() => {
    generatedSections.value[index] = contents[index] || '内容生成中...'
    addTimeline('success', `完成: ${sections[index].title}`)
    generateNextSection(index + 1)
  }, 1500 + Math.random() * 1500))
}

// --- Chat ---
const sendMessage = () => {
  const text = chatInput.value.trim()
  if (!text || isSending.value) return

  chatHistory.value.push({ role: 'user', content: text, time: getTimeStr() })
  chatInput.value = ''
  isSending.value = true
  scrollChatToBottom()

  const dept = formData.value?.department || '临床'
  const topic = formData.value?.topic || '这个领域'
  const mockResponses = [
    `关于您的问题，结合文章内容来看，这是一个很好的切入点。"${topic}"确实有很多值得深入探讨的方面。\n\n从${dept}角度来说，建议关注以下几点：\n\n1. 个体化差异是需要重点考虑的因素\n2. 最新的循证医学证据不断在更新\n3. 与主治医生的充分沟通非常重要\n\n您还想了解哪方面的具体内容？`,
    `感谢您的提问！这个问题在${dept}中确实很常见。\n\n根据目前的研究和指南推荐，核心建议是：\n\n- **规范化管理**是基础\n- **定期随访**不可忽视\n- **患者教育**对预后有积极影响\n\n如果需要，我可以针对文章中的某个具体章节做更详细的展开说明。`,
    `这是一个非常专业的问题。让我结合文章内容为您分析：\n\n文章中提到的核心知识点为我们提供了一个基本框架。在此基础上，我想补充以下几点：\n\n> 循证医学强调的是"最佳证据、临床经验和患者偏好"的有机结合。\n\n实际应用中需要根据具体情况灵活调整。建议您将这些信息作为与医生沟通的参考，而非直接的诊疗依据。`
  ]

  timers.push(setTimeout(() => {
    const idx = chatHistory.value.filter(m => m.role === 'assistant').length % mockResponses.length
    chatHistory.value.push({ role: 'assistant', content: mockResponses[idx], time: getTimeStr() })
    isSending.value = false
    scrollChatToBottom()
  }, 1000 + Math.random() * 1000))
}

const scrollChatToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  })
}

// --- Markdown ---
const escapeHtml = (text) => {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

const renderMarkdown = (text) => {
  if (!text) return ''
  let html = escapeHtml(text)
  html = html.replace(/^### (.+)$/gm, '<h4>$1</h4>')
  html = html.replace(/^## (.+)$/gm, '<h3>$1</h3>')
  html = html.replace(/^# (.+)$/gm, '<h2>$1</h2>')
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>')
  html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>')
  html = html.replace(/^---$/gm, '<hr>')
  html = html.replace(/^- (.+)$/gm, '<li class="ul-li">$1</li>')
  html = html.replace(/^\d+\. (.+)$/gm, '<li class="ol-li">$1</li>')
  html = html.replace(/((?:<li class="ul-li">.*<\/li>\n?)+)/g, '<ul>$1</ul>')
  html = html.replace(/((?:<li class="ol-li">.*<\/li>\n?)+)/g, '<ol>$1</ol>')
  html = html.replace(/`(.+?)`/g, '<code>$1</code>')
  html = html.replace(/\n\n/g, '</p><p>')
  html = '<p>' + html + '</p>'
  html = html.replace(/<p><(h[234]|blockquote|ul|ol|hr)/g, '<$1')
  html = html.replace(/<\/(h[234]|blockquote|ul|ol)><\/p>/g, '</$1>')
  html = html.replace(/<hr><\/p>/g, '<hr>')
  html = html.replace(/<p><\/p>/g, '')
  return html
}

// --- Lifecycle ---
onMounted(() => {
  if (!formData.value) {
    router.push('/science-article')
    return
  }
  startMockGeneration()
})

onUnmounted(() => {
  timers.forEach(clearTimeout)
  if (elapsedTimer) clearInterval(elapsedTimer)
})
</script>

<style scoped>
.mono { font-family: 'JetBrains Mono', monospace; }

/* === Layout === */
.main-view {
  height: calc(100vh - var(--site-header-offset));
  display: flex;
  flex-direction: column;
  background: #FFF;
  overflow: hidden;
  font-family: 'Inter', 'Noto Sans SC', system-ui, sans-serif;
}

/* === Header === */
.app-header {
  height: 60px;
  border-bottom: 1px solid #EAEAEA;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #FFF;
  z-index: 100;
  flex-shrink: 0;
  position: relative;
}

.header-left { display: flex; align-items: center; gap: 20px; }

.brand {
  font-family: 'Noto Sans SC', system-ui, sans-serif;
  font-weight: 800;
  font-size: 16px;
  cursor: pointer;
}

.back-link {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #9CA3AF;
  cursor: pointer;
  transition: color 0.2s;
}
.back-link:hover { color: #111827; }

.header-center { position: absolute; left: 50%; transform: translateX(-50%); }

.view-switcher {
  display: flex;
  background: #F5F5F5;
  padding: 4px;
  border-radius: 6px;
  gap: 4px;
}

.switch-btn {
  border: none;
  background: transparent;
  padding: 6px 16px;
  font-size: 12px;
  font-weight: 600;
  color: #6B7280;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.switch-btn.active {
  background: #FFF;
  color: #111827;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.header-right { display: flex; align-items: center; gap: 16px; }

.workflow-step { display: flex; align-items: center; gap: 8px; font-size: 14px; }
.step-num { font-weight: 700; color: #9CA3AF; }
.step-name { font-weight: 700; color: #111827; }
.step-divider { width: 1px; height: 14px; background: #E5E7EB; }

.status-indicator { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #6B7280; font-weight: 500; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: #D1D5DB; }
.status-indicator.processing .dot { background: #F59E0B; animation: pulse 1s infinite; }
.status-indicator.completed .dot { background: #10B981; }

@keyframes pulse { 50% { opacity: 0.5; } }

/* === Content Area === */
.content-area { flex: 1; display: flex; overflow: hidden; }

.panel-wrapper {
  height: 100%;
  overflow: hidden;
  transition: width 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), opacity 0.3s ease, transform 0.3s ease;
  will-change: width, opacity, transform;
}

.panel-wrapper.left { border-right: 1px solid #E5E7EB; }

/* === Left Panel === */
.article-panel {
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 30px 50px 60px;
}

.article-panel::-webkit-scrollbar { width: 6px; }
.article-panel::-webkit-scrollbar-track { background: transparent; }
.article-panel::-webkit-scrollbar-thumb { background: transparent; border-radius: 3px; }
.article-panel:hover::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); }

/* Waiting */
.waiting-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  color: #9CA3AF;
}

.waiting-animation { position: relative; width: 48px; height: 48px; }
.waiting-animation.small { width: 32px; height: 32px; margin-bottom: 12px; }

.waiting-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid #E5E7EB;
  border-radius: 50%;
  animation: ripple 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
.waiting-ring:nth-child(2) { animation-delay: 0.4s; }
.waiting-ring:nth-child(3) { animation-delay: 0.8s; }

@keyframes ripple {
  0% { transform: scale(0.5); opacity: 1; }
  100% { transform: scale(2); opacity: 0; }
}

.waiting-text { font-size: 14px; }

/* Report Content */
.report-content-wrapper { max-width: 800px; margin: 0 auto; width: 100%; }

.report-header-block { margin-bottom: 30px; }

.report-meta { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }

.report-tag {
  background: #000;
  color: #FFF;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 8px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.tone-tag { background: #FF4500; }

.report-id {
  font-size: 11px;
  color: #9CA3AF;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.main-title {
  font-family: 'Times New Roman', Times, serif;
  font-size: 36px;
  font-weight: 700;
  color: #111827;
  line-height: 1.2;
  margin: 0 0 16px 0;
  letter-spacing: -0.02em;
}

.sub-title {
  font-family: 'Times New Roman', Times, serif;
  font-size: 16px;
  color: #6B7280;
  font-style: italic;
  line-height: 1.6;
  margin: 0 0 30px 0;
  font-weight: 400;
}

.header-divider { height: 1px; background: #E5E7EB; width: 100%; }

/* Sections */
.sections-list { display: flex; flex-direction: column; gap: 32px; }

.report-section-item { display: flex; flex-direction: column; gap: 12px; }

.section-header-row {
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 8px 12px;
  margin: -8px -12px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.section-header-row.clickable { cursor: pointer; }
.section-header-row.clickable:hover { background-color: #F9FAFB; }

.section-number { font-size: 16px; color: #9CA3AF; font-weight: 500; }

.section-title {
  font-family: 'Times New Roman', Times, serif;
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin: 0;
  transition: color 0.3s;
}

.report-section-item.is-pending .section-title { color: #D1D5DB; }

.collapse-icon {
  margin-left: auto;
  color: #9CA3AF;
  transition: transform 0.3s;
  flex-shrink: 0;
  align-self: center;
}

.collapse-icon.is-collapsed { transform: rotate(-90deg); }

.section-body { padding-left: 28px; overflow: hidden; }

.generated-content {
  font-family: 'Inter', 'Noto Sans SC', system-ui, sans-serif;
  font-size: 14px;
  line-height: 1.8;
  color: #374151;
}

.generated-content :deep(p) { margin-bottom: 1em; }
.generated-content :deep(h2), .generated-content :deep(h3), .generated-content :deep(h4) {
  font-family: 'Times New Roman', Times, serif;
  color: #111827;
  margin-top: 1.5em;
  margin-bottom: 0.8em;
  font-weight: 700;
}
.generated-content :deep(h3) { font-size: 18px; }
.generated-content :deep(h4) { font-size: 16px; }
.generated-content :deep(ul), .generated-content :deep(ol) { padding-left: 24px; margin: 12px 0; }
.generated-content :deep(li) { margin: 6px 0; }
.generated-content :deep(blockquote) {
  border-left: 3px solid #E5E7EB;
  padding-left: 16px;
  margin: 1.5em 0;
  color: #6B7280;
  font-style: italic;
  font-family: 'Times New Roman', Times, serif;
}
.generated-content :deep(hr) { border: none; border-top: 1px solid #E5E7EB; margin: 1.5em 0; }
.generated-content :deep(code) {
  background: #F9FAFB;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  border: 1px solid #E5E7EB;
}
.generated-content :deep(strong) { font-weight: 600; color: #111827; }

/* Loading */
.loading-state {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #6B7280;
  font-size: 14px;
  margin-top: 4px;
}

.loading-icon {
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-icon.small { width: 14px; height: 14px; }

.loading-text {
  font-family: 'Times New Roman', Times, serif;
  font-size: 15px;
  color: #4B5563;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* === Right Panel === */
.right-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #FFF;

  --wf-border: #E5E7EB;
  --wf-divider: #F3F4F6;
  --wf-active-bg: #FAFAFA;
  --wf-active-border: #1F2937;
  --wf-active-dot: #1F2937;
  --wf-active-text: #1F2937;
  --wf-done-bg: #F9FAFB;
  --wf-done-border: #E5E7EB;
  --wf-done-dot: #10B981;
  --wf-muted-dot: #D1D5DB;
  --wf-todo-text: #9CA3AF;
}

.right-panel::-webkit-scrollbar { width: 6px; }
.right-panel::-webkit-scrollbar-track { background: transparent; }
.right-panel::-webkit-scrollbar-thumb { background: transparent; border-radius: 3px; }
.right-panel:hover::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); }

/* Panel Header */
.panel-header {
  padding: 14px 20px;
  border-bottom: 1px solid var(--wf-divider);
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.panel-header--active { border-color: #1F2937; }

.header-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--wf-active-dot);
  animation: pulse 1s infinite;
}

.header-index { font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.02em; }
.panel-header--active .header-index { color: #1F2937; }

.header-title { font-size: 13px; font-weight: 600; color: #111827; }

/* Workflow Overview */
.workflow-overview { padding: 16px 20px 0; }

.workflow-metrics {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.metric { display: inline-flex; align-items: baseline; gap: 6px; }
.metric-right { margin-left: auto; }

.metric-label {
  font-size: 11px;
  font-weight: 600;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.metric-value { font-size: 12px; color: #374151; }

.metric-pill {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid var(--wf-border);
  background: #F9FAFB;
  color: #6B7280;
}

.pill--processing { background: var(--wf-active-bg); border-color: var(--wf-active-border); color: var(--wf-active-text); }
.pill--completed { background: #ECFDF5; border-color: #A7F3D0; color: #065F46; }

/* Workflow Steps */
.workflow-steps { display: flex; flex-direction: column; gap: 10px; padding-bottom: 10px; }

.wf-step {
  display: grid;
  grid-template-columns: 24px 1fr;
  gap: 12px;
  padding: 10px 12px;
  border: 1px solid var(--wf-divider);
  border-radius: 8px;
  background: #FFF;
}

.wf-step--active { background: var(--wf-active-bg); border-color: var(--wf-active-border); }
.wf-step--done { background: var(--wf-done-bg); border-color: var(--wf-done-border); }
.wf-step--todo { background: transparent; border-style: dashed; border-color: var(--wf-border); }

.wf-step-connector { display: flex; flex-direction: column; align-items: center; width: 24px; flex-shrink: 0; }

.wf-step-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--wf-muted-dot);
  border: 2px solid #FFF;
  z-index: 1;
}

.wf-step--active .wf-step-dot { background: var(--wf-active-dot); box-shadow: 0 0 0 3px rgba(31, 41, 55, 0.12); }
.wf-step--done .wf-step-dot { background: var(--wf-done-dot); }

.wf-step-line { width: 2px; flex: 1; background: var(--wf-divider); margin-top: -2px; }

.wf-step-title-row { display: flex; align-items: baseline; gap: 10px; min-width: 0; }

.wf-step-index { font-size: 11px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.02em; flex-shrink: 0; }
.wf-step--todo .wf-step-index { color: var(--wf-todo-text); }
.wf-step--done .wf-step-index { color: var(--wf-done-dot); }

.wf-step-title {
  font-family: 'Times New Roman', Times, serif;
  font-size: 13px;
  font-weight: 600;
  color: #111827;
  line-height: 1.35;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.wf-step--todo .wf-step-title { color: var(--wf-todo-text); }

.wf-step-meta {
  margin-left: auto;
  font-size: 10px;
  font-weight: 700;
  color: var(--wf-active-text);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  flex-shrink: 0;
}

/* Next Step Button */
.next-step-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px 16px;
  margin-top: 10px;
  background: #111827;
  color: #FFF;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.next-step-btn:hover { background: #FF4500; transform: translateY(-1px); }

.workflow-divider { height: 1px; background: var(--wf-divider); margin: 14px 0 0; }

/* Workflow Timeline */
.workflow-timeline {
  padding: 14px 20px 24px;
  flex: 1;
  overflow-y: auto;
}

.timeline-item {
  display: grid;
  grid-template-columns: 24px 1fr;
  gap: 12px;
  padding: 10px 12px;
  margin-bottom: 10px;
  border: 1px solid var(--wf-divider);
  border-radius: 8px;
  background: #FFF;
  transition: background-color 0.15s, border-color 0.15s;
}

.timeline-item:hover { background: #F9FAFB; border-color: var(--wf-border); }
.timeline-item.node--active { background: var(--wf-active-bg); border-color: var(--wf-active-border); }
.timeline-item.node--done { background: var(--wf-done-bg); border-color: var(--wf-done-border); }

.timeline-connector { display: flex; flex-direction: column; align-items: center; width: 24px; flex-shrink: 0; }

.connector-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--wf-muted-dot);
  border: 2px solid #FFF;
  z-index: 1;
}

.connector-line { width: 2px; flex: 1; background: var(--wf-divider); margin-top: -2px; }

.dot-active { background: var(--wf-active-dot); box-shadow: 0 0 0 3px rgba(31, 41, 55, 0.12); }
.dot-done { background: var(--wf-done-dot); }
.dot-muted { background: var(--wf-muted-dot); }

.timeline-content { min-width: 0; }

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.action-label { font-size: 12px; font-weight: 600; color: #374151; letter-spacing: 0.03em; }
.action-time { font-size: 11px; color: #9CA3AF; }

.timeline-body { font-size: 13px; color: #4B5563; }

.status-message {
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 13px;
  border: 1px solid transparent;
}

.status-message.planning { background: var(--wf-active-bg); border-color: var(--wf-active-border); color: var(--wf-active-text); }
.status-message.success { background: #ECFDF5; border-color: #A7F3D0; color: #065F46; }

.timeline-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #D1D5DB;
  font-size: 14px;
}

/* === Chat Mode === */
.chat-header {
  padding: 16px 20px;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.back-to-timeline {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #9CA3AF;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}
.back-to-timeline:hover { color: #111827; }

.chat-title { font-weight: 700; font-size: 14px; color: #111827; }

.chat-messages { flex: 1; overflow-y: auto; padding: 20px 24px; }

.chat-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #D1D5DB;
}

.chat-empty-text { font-size: 13px; text-align: center; max-width: 280px; line-height: 1.7; }

.chat-msg { margin-bottom: 20px; }

.msg-header { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.msg-name { font-weight: 700; font-size: 12px; }
.chat-msg.user .msg-name { color: #111827; }
.chat-msg.assistant .msg-name { color: #FF4500; }
.msg-time { font-size: 11px; color: #D1D5DB; }

.msg-body {
  font-size: 14px;
  line-height: 1.8;
  color: #374151;
  padding: 12px 16px;
  border-radius: 8px;
  font-family: 'Inter', 'Noto Sans SC', system-ui, sans-serif;
}

.chat-msg.user .msg-body { background: #F9FAFB; border: 1px solid #E5E7EB; }
.chat-msg.assistant .msg-body { background: #FFFBF5; border: 1px solid #FED7AA; }

.msg-body.typing {
  color: #9CA3AF;
  display: flex;
  align-items: center;
  gap: 8px;
}

.msg-body h3, .msg-body h4 { margin: 12px 0 6px; font-size: 14px; font-weight: 700; color: #111827; }
.msg-body ul, .msg-body ol { padding-left: 20px; margin: 8px 0; }
.msg-body li { margin-bottom: 4px; }
.msg-body blockquote {
  border-left: 3px solid #E5E7EB;
  padding: 6px 12px;
  margin: 10px 0;
  color: #6B7280;
  font-style: italic;
}
.msg-body strong { font-weight: 600; color: #111827; }
.msg-body code {
  background: #F9FAFB;
  padding: 1px 4px;
  border-radius: 3px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  border: 1px solid #E5E7EB;
}

/* Chat Input */
.chat-input-area {
  padding: 16px 20px;
  border-top: 1px solid #E5E7EB;
  display: flex;
  gap: 10px;
  align-items: flex-end;
  flex-shrink: 0;
}

.chat-textarea {
  flex: 1;
  border: 1px solid #E5E7EB;
  padding: 10px 14px;
  font-family: 'Inter', 'Noto Sans SC', system-ui, sans-serif;
  font-size: 14px;
  resize: none;
  outline: none;
  line-height: 1.5;
  background: #F9FAFB;
  border-radius: 6px;
  transition: border-color 0.2s;
}
.chat-textarea:focus { border-color: #1F2937; background: #FFF; }

.send-btn {
  padding: 10px 20px;
  background: #111827;
  color: #FFF;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}
.send-btn:hover:not(:disabled) { background: #FF4500; }
.send-btn:disabled { background: #E5E7EB; color: #9CA3AF; cursor: not-allowed; }

/* === Responsive === */
@media (max-width: 768px) {
  .header-center { display: none; }
  .header-right { display: none; }
  .content-area { flex-direction: column; }
  .panel-wrapper { width: 100% !important; opacity: 1 !important; transform: none !important; }
  .panel-wrapper.left { border-right: none; border-bottom: 1px solid #E5E7EB; height: 50%; }
  .panel-wrapper.right { height: 50%; }
  .article-panel { padding: 20px 24px 40px; }
  .main-title { font-size: 24px; }
  .section-title { font-size: 18px; }
}
</style>

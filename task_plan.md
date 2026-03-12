# Task Plan: 医路达AI创作助手

## 目标
将 MiroFish 改造为 **医路达AI创作助手**（AI医学文章生成系统）。

---

## Phase 1: 首页改造 ✅

### 1.1 品牌替换
- [x] `frontend/index.html`: title 改为 "医路达AI创作助手"，meta description 更新
- [x] `frontend/src/views/Home.vue`: 导航栏品牌名 "MIROFISH" → "医路达AI创作助手"

### 1.2 移除不相关元素
- [x] 移除导航栏 GitHub 链接、Hero 区域、Dashboard 区域、HistoryDatabase
- [x] 清理 script 逻辑和 CSS

### 1.3 新增文档类型卡片入口
- [x] 3 张卡片（医学科普文章、病例报告、更多类型置灰）
- [x] 路由 + 占位页面

---

## Phase 2: 医学科普文章表单 ✅

- [x] ScienceArticle.vue 改为 console-box 步骤式表单
- [x] 6 个表单步骤：目标读者、科室领域、科普主题、文章调性、期望字数、参考材料上传

---

## Phase 3: 文章生成 + 深度互动 ← CURRENT

### 背景分析

原 MiroFish 流程：Step1 图谱构建 → Step2 环境搭建 → Step3 模拟运行 → **Step4 报告生成** → **Step5 深度互动**

我们需要的核心是 **Step4（文章生成）** 和 **Step5（深度互动）**。
前置步骤（文献检索等）未来再做，但流程架构保留扩展性。

### 整体方案

```
ScienceArticle.vue (表单)
  ↓ 点击"开始生成"
ArticleGenerateView.vue (文章生成 — 改造自 ReportView 模式)
  ├─ 左栏：文章内容（大纲 → 逐段生成，markdown 渲染）
  ├─ 右栏：生成时间线（步骤状态、agent 日志）
  ├─ 视图模式切换（双栏 / 工作台）
  ↓ 生成完成后
  └─ 进入深度互动模式（右栏切换为聊天界面）
```

**关键决策：合并 Step4+Step5 为一个页面**，生成完成后右栏从"时间线"切换为"聊天"，
避免多余的页面跳转，用户体验更流畅。

### 3.1 路由与页面结构
- [ ] 新增路由 `/science-article/generate/:taskId`
- [ ] 新建 `ArticleGenerateView.vue`（文章生成主视图）
- [ ] ScienceArticle.vue 表单提交后跳转到生成页面

### 3.2 文章生成页面 — 布局
- [ ] 顶部 Header：品牌名 + 返回按钮 + 步骤指示器 + 视图模式切换（双栏/工作台）
- [ ] 双栏布局（参考 ReportView 的 main-split-layout）
  - 左栏：文章内容面板
  - 右栏：生成进度 / 互动面板

### 3.3 文章生成页面 — 左栏（文章内容）
- [ ] 文章头部区域：标题、摘要、元信息（科室、调性、字数等）
- [ ] 章节列表：先显示大纲骨架，逐段填充内容
- [ ] 每个章节：标题 + markdown 渲染内容 + 折叠/展开
- [ ] 生成中的章节：显示 loading 动画
- [ ] 全文只读展示（不可编辑）

### 3.4 文章生成页面 — 右栏（生成模式）
- [ ] 工作流概览：总章节数 / 已完成 / 耗时 / 进度条
- [ ] 工作流步骤树：PL(规划) → 01(章节1) → 02(章节2) → ... → OK(完成)
- [ ] 时间线日志：显示 agent 的每一步操作（规划、生成中、完成等）
- [ ] 生成完成后：显示"进入深度互动"按钮

### 3.5 文章生成页面 — 右栏（互动模式，生成完成后）
- [ ] 聊天界面：与 AI 讨论生成的文章
- [ ] 消息列表（用户/AI 气泡）+ 底部输入框
- [ ] 支持 markdown 渲染 AI 回复
- [ ] 保留聊天历史

### 3.6 数据流 & API 策略
- [ ] **方案A（有后端API）**：复用/改造现有 report API
  - POST `/api/article/generate` — 开始生成（传入表单参数）
  - GET `/api/article/{taskId}/agent-log?from_line=N` — 增量轮询日志
  - POST `/api/article/chat` — 与 AI 对话
- [ ] **方案B（纯前端Mock）**：先用模拟数据展示完整 UI 流程
  - Mock 大纲数据 + 逐段延时填充
  - Mock 时间线日志
  - Mock 聊天回复

### 3.7 先做界面，后接 API
- [ ] 第一步：搭建页面骨架（布局、路由、组件结构）
- [ ] 第二步：用 Mock 数据实现完整 UI 交互（大纲→逐段生成动画→完成→聊天）
- [ ] 第三步：对接真实后端 API（替换 Mock 为真实轮询）

---

## Phase 3.3: 对接真实 LLM API ← CURRENT

### 目标
将 ArticleGenerateView.vue 的 mock 数据替换为真实 LLM 调用，实现：表单提交 → LLM 生成大纲 → 逐段生成文章内容 → 深度互动聊天。

### 背景分析

**现有后端能力：**
- Flask 应用 (`/backend/`)，端口 5001
- `LLMClient` (`/backend/app/utils/llm_client.py`) — OpenAI SDK 格式，支持任意兼容 API
- `TaskManager` (`/backend/app/models/task.py`) — 线程安全的异步任务管理，支持进度更新
- `ReportAgent` (`/backend/app/services/report_agent.py`) — 完整的 ReACT agent，但**强依赖 Zep 图谱和 OASIS 模拟**
- 日志系统 (`ReportLogger`) — JSONL 格式增量日志

**问题：ReportAgent 不能直接复用**
- 现有流程：`simulation_id` → 从 Zep 知识图谱搜索 → ReACT 循环（3-5次工具调用/章节） → 生成
- 医学科普文章不需要知识图谱和模拟，只需要 LLM 根据表单参数直接生成
- 如果强行复用，需要 Zep API Key + 预先构建图谱，过于重量级

**方案：新建轻量级 ArticleAgent**
- 不依赖 Zep/OASIS，直接用 LLM 生成
- 复用现有 `LLMClient`、`TaskManager`、日志系统
- 流程：表单参数 → LLM 规划大纲 (JSON) → 逐段 LLM 生成内容 → 组装全文
- 聊天：将全文作为上下文，LLM 直接回答

---

### 架构设计

```
前端 ArticleGenerateView.vue
  │
  ├─ POST /api/article/generate  →  创建任务，后台线程启动 ArticleAgent
  │    body: { topic, department, audience, tone, wordCount }
  │    return: { task_id, article_id }
  │
  ├─ GET /api/article/{id}/agent-log?from_line=N  →  增量轮询 JSONL 日志
  │    前端解析 action 类型，驱动 UI 状态：
  │    - planning_complete → 显示大纲
  │    - section_start → 设置 currentSectionIndex
  │    - section_complete → 填充章节内容
  │    - report_complete → 标记完成
  │
  ├─ GET /api/article/{id}/progress  →  轮询进度百分比（备用）
  │
  └─ POST /api/article/chat  →  深度互动
       body: { article_id, message, chat_history }
       return: { response }
```

---

### 3.3.1 后端：新建 ArticleAgent 服务

**新文件**: `/backend/app/services/article_agent.py`

**核心类**: `ArticleAgent`

**复用的模块：**
| 模块 | 来源 | 用途 |
|------|------|------|
| `LLMClient` | `/backend/app/utils/llm_client.py` | 调用 LLM |
| `TaskManager` | `/backend/app/models/task.py` | 异步任务管理 |
| `ReportLogger` | 从 `report_agent.py` 提取或重写 | JSONL 日志 |

**不复用的模块：**
| 模块 | 原因 |
|------|------|
| `ZepToolsService` | 不需要知识图谱搜索 |
| `ReportAgent` 的 ReACT 循环 | 科普文章不需要工具调用循环 |
| OASIS 相关 | 不需要模拟 |

**ArticleAgent 流程：**

```python
class ArticleAgent:
    def __init__(self, article_id, form_data, llm_client=None):
        self.article_id = article_id
        self.form_data = form_data  # {topic, department, audience, tone, wordCount}
        self.llm = llm_client or LLMClient()
        self.logger = ArticleLogger(article_id)  # JSONL 日志

    def run(self):
        """主流程（在后台线程中执行）"""
        # 1. 规划大纲
        self.logger.log('planning_start')
        outline = self._plan_outline()
        self.logger.log('planning_complete', outline=outline)

        # 2. 逐段生成
        sections = {}
        for i, section in enumerate(outline['sections']):
            self.logger.log('section_start', section_index=i, section_title=section['title'])
            content = self._generate_section(section, outline, sections)
            sections[i] = content
            self.logger.log('section_complete', section_index=i, content=content)

        # 3. 组装全文
        full_content = self._assemble(outline, sections)
        self.logger.log('report_complete', content=full_content)

    def _plan_outline(self):
        """用 LLM 生成大纲（JSON 格式）"""
        # 系统提示：你是医学科普文章专家...
        # 用户提示：根据 {topic}, {department}, {audience}, {tone}, {wordCount} 生成大纲
        # 返回: { title, summary, sections: [{title, description}] }
        pass

    def _generate_section(self, section, outline, prev_sections):
        """用 LLM 生成单个章节"""
        # 系统提示：你正在撰写医学科普文章，当前章节是...
        # 包含：文章大纲、前面章节摘要、当前章节要求
        # 返回：markdown 格式内容
        pass
```

**Prompt 设计要点：**

1. **大纲规划 prompt**
   - 系统角色：资深医学科普作家
   - 输入：topic, department, audience, tone, wordCount
   - 输出格式：JSON `{title, summary, sections: [{title, description}]}`
   - 章节数：根据 wordCount 自动决定（1500字→3-4节，3000字→5-6节）
   - temperature: 0.3

2. **章节生成 prompt**
   - 系统角色：同上
   - 输入：完整大纲、前序章节内容（截断到4000字）、当前章节标题和描述
   - 输出：纯 markdown 内容（不含章节标题，标题由前端渲染）
   - 风格要求：根据 tone 调整（professional=术语精确、casual=通俗比喻）
   - 目标字数：wordCount / 章节数
   - temperature: 0.5

3. **聊天 prompt**
   - 系统角色：文章作者 AI 助手
   - 上下文：全文内容（前15000字）
   - 输入：用户问题 + chat_history
   - temperature: 0.5

**日志格式（JSONL，与现有 ReportLogger 兼容）：**
```json
{"timestamp":"...","action":"planning_start","stage":"planning","details":{}}
{"timestamp":"...","action":"planning_complete","stage":"planning","details":{"outline":{...}}}
{"timestamp":"...","action":"section_start","stage":"generating","details":{"section_index":0,"section_title":"引言"}}
{"timestamp":"...","action":"section_complete","stage":"generating","details":{"section_index":0,"content":"..."}}
{"timestamp":"...","action":"report_complete","stage":"completed","details":{"total_sections":5,"total_time_seconds":45}}
```

**文件存储结构：**
```
backend/uploads/articles/{article_id}/
  ├── meta.json         # 元数据 + 最终结果
  ├── agent_log.jsonl   # 增量日志（前端轮询用）
  └── progress.json     # 进度百分比
```

### 3.3 当前实现策略 (2026-03-12)
- [x] 后端新增 `article` blueprint，并在 Flask app 中注册 `/api/article/*`
- [x] 新建 `backend/app/services/article_agent.py`，包含 `ArticleLogger`、`ArticleManager`、`ArticleAgent`
- [x] 生成链路采用后台线程 + `TaskManager`，避免阻塞请求
- [x] 前端新增 `frontend/src/api/article.js`
- [x] `ScienceArticle.vue` 提交时先调 `/api/article/generate`，再跳转到生成页
- [x] `ArticleGenerateView.vue` 改为真实轮询 `/api/article/{id}/agent-log` 和 `/api/article/chat`
- [x] 保留当前 UI，不在本轮重做布局，只替换数据源与状态驱动

### 3.3 实现结果 (2026-03-12)
- [x] 构建验证通过：`npm run build`
- [x] 后端语法检查通过：`python3 -m py_compile ...`
- [ ] 待你本地用真实 `LLM_API_KEY` 做一次端到端联调

---

### 3.3.2 后端：新建 Article API 路由

**新文件**: `/backend/app/api/article.py`

**端点：**

#### `POST /api/article/generate`
```
Request: { topic, department, audience, tone, wordCount }
Response: { success: true, data: { article_id, task_id } }
```
- 创建 article_id (uuid)
- 创建 TaskManager 任务
- 启动后台线程 `ArticleAgent.run()`
- 立即返回 article_id + task_id

#### `GET /api/article/{article_id}/agent-log`
```
Query: from_line=0
Response: { success: true, data: { logs: [...], from_line: N } }
```
- 读取 `agent_log.jsonl`，从 from_line 开始返回新行
- 前端轮询此接口驱动 UI

#### `GET /api/article/{article_id}/progress`
```
Response: { success: true, data: { status, progress, message } }
```
- 读取 `progress.json`

#### `POST /api/article/chat`
```
Request: { article_id, message, chat_history }
Response: { success: true, data: { response } }
```
- 读取 meta.json 中的全文
- 构建聊天 prompt，调用 LLM
- 返回回复

**注册蓝图：** 修改 `/backend/app/api/__init__.py` 和 `/backend/app/__init__.py`

---

### 3.3.3 前端：新建 article API 模块

**新文件**: `/frontend/src/api/article.js`

```javascript
import service from './index'

// 开始生成文章
export const generateArticle = (data) => {
  return service.post('/api/article/generate', data)
}

// 获取增量日志
export const getArticleLog = (articleId, fromLine = 0) => {
  return service.get(`/api/article/${articleId}/agent-log`, {
    params: { from_line: fromLine }
  })
}

// 获取进度
export const getArticleProgress = (articleId) => {
  return service.get(`/api/article/${articleId}/progress`)
}

// 聊天互动
export const chatWithArticle = (data) => {
  return service.post('/api/article/chat', data)
}
```

---

### 3.3.4 前端：改造 ArticleGenerateView.vue

**文件**: `/frontend/src/views/ArticleGenerateView.vue`

**核心改动：用真实 API 替换所有 mock 逻辑**

#### 删除的代码
- `buildMockOutline()` 函数
- `buildMockContents()` 函数
- `startMockGeneration()` 函数
- `generateNextSection()` 函数
- `sendMessage()` 中的 mockResponses 和 setTimeout

#### 新增的代码

**1. onMounted：调用生成 API + 启动轮询**
```javascript
onMounted(async () => {
  if (!formData.value) { router.push('/science-article'); return }

  startTime.value = Date.now()
  elapsedTimer = setInterval(() => {
    elapsedSeconds.value = Math.floor((Date.now() - startTime.value) / 1000)
  }, 1000)

  // 调用生成 API
  const res = await generateArticle({
    topic: formData.value.topic,
    department: formData.value.department,
    audience: formData.value.audience,
    tone: formData.value.tone,
    wordCount: formData.value.wordCount
  })
  articleId.value = res.data.article_id

  // 启动日志轮询
  startPolling()
})
```

**2. 日志轮询逻辑**
```javascript
let fromLine = 0
let pollTimer = null

const startPolling = () => {
  pollTimer = setInterval(async () => {
    const res = await getArticleLog(articleId.value, fromLine)
    const logs = res.data.logs
    fromLine = res.data.from_line

    for (const log of logs) {
      handleLogEntry(log)
    }

    // 生成完成后停止轮询
    if (isComplete.value) {
      clearInterval(pollTimer)
      clearInterval(elapsedTimer)
    }
  }, 2000)  // 每 2 秒轮询一次
}
```

**3. 日志事件处理**
```javascript
const handleLogEntry = (log) => {
  switch (log.action) {
    case 'planning_start':
      addTimeline('active', '开始规划文章大纲...')
      break

    case 'planning_complete':
      outline.value = log.details.outline
      addTimeline('success', '大纲规划完成', `共 ${outline.value.sections.length} 个章节`)
      break

    case 'section_start':
      currentSectionIndex.value = log.details.section_index
      addTimeline('active', `正在生成: ${log.details.section_title}`)
      break

    case 'section_complete':
      generatedSections.value[log.details.section_index] = log.details.content
      addTimeline('success', `完成: ${log.details.section_title}`)
      break

    case 'report_complete':
      isComplete.value = true
      currentSectionIndex.value = null
      addTimeline('success', '文章生成完成', '所有章节已生成，可进入深度互动')
      break

    case 'error':
      addTimeline('error', '生成出错', log.details.error_message)
      break
  }
}
```

**4. 聊天改为真实 API**
```javascript
const sendMessage = async () => {
  const text = chatInput.value.trim()
  if (!text || isSending.value) return

  chatHistory.value.push({ role: 'user', content: text, time: getTimeStr() })
  chatInput.value = ''
  isSending.value = true
  scrollChatToBottom()

  try {
    const res = await chatWithArticle({
      article_id: articleId.value,
      message: text,
      chat_history: chatHistory.value.slice(0, -1)  // 不含刚添加的用户消息
    })
    chatHistory.value.push({ role: 'assistant', content: res.data.response, time: getTimeStr() })
  } catch (err) {
    chatHistory.value.push({ role: 'assistant', content: '抱歉，回复时出现错误，请重试。', time: getTimeStr() })
  }

  isSending.value = false
  scrollChatToBottom()
}
```

**5. onUnmounted 清理**
```javascript
onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
  if (elapsedTimer) clearInterval(elapsedTimer)
})
```

---

### 3.3.5 后端注册新蓝图

**修改**: `/backend/app/api/__init__.py`
```python
article_bp = Blueprint('article', __name__)
from . import article  # noqa
```

**修改**: `/backend/app/__init__.py`
```python
from .api import graph_bp, simulation_bp, report_bp, article_bp
app.register_blueprint(article_bp, url_prefix='/api/article')
```

---

### 3.3.6 Docker 部署适配

前后端都从本地代码构建，不依赖外部镜像。

**新建**: `/backend/Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "run.py"]
```

**修改**: `/frontend/nginx.conf` — 添加 API 反向代理
```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location /api/ {
        proxy_pass http://backend:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

这样前端 axios 的 baseURL 用空字符串（同域），API 请求通过 Nginx 转发到后端容器。

**重写**: `/docker-compose.yml`
```yaml
services:
  backend:
    build: ./backend
    container_name: mirofish-backend
    env_file:
      - .env
    volumes:
      - ./backend/uploads:/app/uploads
    restart: unless-stopped

  web:
    build: ./frontend
    container_name: mirofish-web
    ports:
      - "3333:80"
    depends_on:
      - backend
    restart: unless-stopped
```

> 只暴露 3333 端口（前端 Nginx），后端 5001 端口仅在 Docker 内部网络可达。
> Caddy 配置中 `ai.medstarai.com` 继续反代到 3333 端口即可。

---

### 3.3.7 环境变量

后端 `.env` 需要配置：
```env
LLM_API_KEY=<your-api-key>
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=x-ai/grok-4.1-fast
```

> 不需要 ZEP_API_KEY（ArticleAgent 不用 Zep）

---

### 3.3.8 实施顺序

| 步骤 | 文件 | 说明 |
|------|------|------|
| 1 | `/backend/app/services/article_agent.py` | 新建 ArticleAgent + ArticleLogger |
| 2 | `/backend/app/api/article.py` | 新建 API 路由 (generate, agent-log, progress, chat) |
| 3 | `/backend/app/api/__init__.py` | 注册 article_bp 蓝图 |
| 4 | `/backend/app/__init__.py` | 注册蓝图到 Flask app |
| 5 | `/frontend/src/api/article.js` | 新建前端 API 模块 |
| 6 | `/frontend/src/views/ArticleGenerateView.vue` | 替换 mock → 真实 API |
| 7 | `/frontend/nginx.conf` | 添加 `/api/` 反向代理到 backend 容器 |
| 8 | `/backend/Dockerfile` | 新建后端 Docker 镜像（Python 3.11 + Flask） |
| 9 | `/backend/.dockerignore` | 排除 __pycache__/uploads/.env |
| 10 | `/docker-compose.yml` | 重写：backend(本地构建) + web(Nginx)，只暴露 3333 |
| 11 | `/frontend/src/api/index.js` | baseURL 改为空（通过 Nginx 同域代理） |

### 3.3.9 验证清单

- [ ] 后端 `python -c "from app.services.article_agent import ArticleAgent"` 无报错
- [ ] `POST /api/article/generate` 返回 article_id + task_id
- [ ] `GET /api/article/{id}/agent-log` 返回增量 JSONL 日志
- [ ] 前端轮询日志 → 大纲出现 → 章节逐个生成 → 完成
- [ ] 聊天 `POST /api/article/chat` 返回 LLM 真实回复
- [ ] Docker `docker compose up -d --build` 正常启动
- [ ] 通过 `http://localhost:3333` 完整走通流程

### 决策记录 (2026-03-12)
1. **后端部署**：从本地 `/backend` 代码构建 Docker 镜像，不依赖旧版 `ghcr.io` 镜像
2. **LLM 配置**：使用现有 `.env` 中的 OpenRouter Key + `x-ai/grok-4.1-fast`
3. **实时机制**：保持 HTTP 轮询（2秒），与原始项目 ReportView 一致，不引入 WebSocket

---

## Phase 4: UI 优化与体验改进 ← CURRENT

### 4.1 病例报告页面优化
- [ ] CaseReport.vue — 改为更精致的"正在开发中，敬请期待"样式

### 4.2 目标读者改为单选
- [ ] ScienceArticle.vue — 将 input 改为 radio 单选（普通大众、患者及家属、医护同行）

### 4.3 科室选择后自动填充科普主题
- [ ] ScienceArticle.vue — 添加科室→默认主题映射，选择科室后自动填入 topic

### 4.4 表单页面双栏改造
- [ ] ScienceArticle.vue — 改为左右双栏布局
  - 左栏：参考原始首页左面板样式（状态指示 + 工作流步骤列表）
  - 右栏：现有表单（console-box）
  - 虚拟步骤：文献检索 → 知识图谱 → 素材整理 → 大纲规划 → 内容创作 → 审核优化

---

## Phase 5: 集成主站 Header ← CURRENT

### 目标
将主站（yizhibang）的全站导航 Header 集成到当前项目（MiroFish），使两个站点在导航层面统一，用户可以在主站和 AI写作站之间无缝切换。

### 决策记录 (2026-03-12)
1. **全局集成**: 所有页面都显示主站导航，包括工作流页面 → 在 App.vue 全局引入
2. **原有 navbar**: 保留并改为白色背景，顺移到主站导航下方，后续再调整
3. **Logo**: 使用主站域名绝对 URL 引用 (`https://medstarai.com/images/home/医职帮logo.png`)
4. **AI写作链接**: 保持主站原有链接 `https://ai.medstarai.com/medical-science`

---

### 主站源码参考 (必读)

主站代码位于 `/Users/luochujian/work/newwork/yizhibang`，技术栈: **Next.js 15 + React 19 + CSS Modules**。

需要参考的两个文件:
- **React 组件**: `/Users/luochujian/work/newwork/yizhibang/src/app/home/components/Header.tsx` (141行)
- **CSS 样式**: `/Users/luochujian/work/newwork/yizhibang/src/app/home/components/Header.module.css` (382行)

> 实现前请完整阅读这两个文件，理解结构后用 Vue 3 重写，不要遗漏任何功能。

#### 主站 Header 导航数据结构
```javascript
const navItems = [
  { href: "/home", label: "网站首页" },
  { href: "/zhicheng", label: "职称评审" },
  {
    href: "/business", label: "业务板块", submenu: [
      { href: "/business/overview", label: "业务概述" },
      { href: "/business/research", label: "课题申报指导" },
      { href: "/business/publication", label: "著作出书" },
      { href: "/business/health", label: "健康科普" },
    ]
  },
  { href: "https://ai.medstarai.com/medical-science", label: "AI写作" },
  { href: "/training", label: "培训课程" },
  { href: "/news", label: "新闻通知" },
  { href: "/about", label: "关于我们" },
];
```

#### 主站 Header 关键样式参数
| 属性 | 桌面端 | 移动端 |
|------|--------|--------|
| 背景 | `#fff` | `#fff` |
| 阴影 | `0 2px 4px rgba(0,0,0,0.1)` | 同左 |
| z-index | `1000` | `1999` (header), `2000` (弹出菜单) |
| 最大宽度 | `1200px` (居中) | 全宽 |
| 导航文字 | `#333`, `16px` | `#333`, `16px` |
| 导航高度 | `40px` per link | — |
| 激活态背景 | `#007bff` | — |
| 激活态文字 | `#fff` | — |
| 激活态圆角 | `border-radius: 50px` | — |
| Hover 背景 | `#f0f0f0` (普通), `#0056b3` (激活) | `#f0f8ff` |
| Logo 高度 | `50px` | `30px` |
| Logo 右边距 | `140px` | `20px` |
| 断点 | — | `@media (max-width: 992px)` |

#### 主站 Header 结构概览 (3 部分)
```
1. 桌面端 (.topBg) — 992px 以上显示
   └ .topCon.pageContainer.topContainer (max-width: 1200px, 居中)
     ├ .logo > a > img (医职帮logo.png)
     └ nav.navBg.navContainer > .tNav > ul.navList
       └ li.navLi (.another=激活) > a.navLink > span
         └ ul.submenu (子菜单, hover 显示)

2. 移动端头部 (.phoneHeader) — 992px 以下显示, position: fixed
   └ .headerTop (flex, space-between)
     ├ .headerTel > a > img (mobile logo)
     └ .headerMenu (汉堡按钮, 3个 span)

3. 移动端弹出菜单 (.navFlyout) — 点击汉堡后显示
   └ .navBox (白色卡片, 90% 宽, max-width: 360px)
     ├ .closeButton > img (close.png)
     ├ h4 "快捷导航"
     └ ul > li > a (导航链接)
       └ ul.mobileSubmenu > li > a.mobileSubmenuLink (子菜单)
```

#### 主站图片资源
- Logo: 主站路径 `/public/images/home/医职帮logo.png`，在本项目中用绝对 URL: `https://medstarai.com/images/home/医职帮logo.png`
- 关闭按钮: 主站路径 `/public/images/close.png`，在本项目中可用 SVG 内联替代 (一个 × 图标)，避免额外资源依赖

---

### 当前项目需要修改的文件

当前项目位于 `/Users/luochujian/work/newwork/MiroFish`，技术栈: **Vue 3 + Vite + Vue Router 4**。

#### 需要新建的文件
| 文件 | 用途 |
|------|------|
| `frontend/src/components/SiteHeader.vue` | 主站导航 Header 组件 (Vue 3 重写) |

#### 需要修改的文件
| 文件 | 修改内容 |
|------|---------|
| `frontend/src/App.vue` | 全局接入 `SiteHeader`，为页面提供统一外层布局 |
| `frontend/src/views/Home.vue` | 移除旧黑色 navbar，改为依赖全局 Header |
| `frontend/src/views/ScienceArticle.vue` | 移除旧黑色 navbar，调整 sticky 偏移 |
| `frontend/src/views/CaseReport.vue` | 移除旧黑色 navbar，改为白色内容头部结构 |
| `frontend/src/views/ArticleGenerateView.vue` | 保留功能性 header，但适配全局 Header 叠加后的页面高度 |
| `frontend/src/views/MainView.vue` | 保留功能性 header，但适配全局 Header 叠加后的页面高度 |
| `frontend/src/views/SimulationView.vue` | 保留功能性 header，但适配全局 Header 叠加后的页面高度 |
| `frontend/src/views/ReportView.vue` | 保留功能性 header，但适配全局 Header 叠加后的页面高度 |

### Phase 5 实施策略 (2026-03-12)
1. 新增 `SiteHeader.vue`，完整复刻主站桌面/移动端导航能力，内部链接统一改为 `https://medstarai.com/*`
2. 在 `App.vue` 全局挂载主站 Header，并通过 CSS 变量统一管理桌面/移动端顶部占位
3. 入口页删除旧黑色 navbar；工作流页保留原有功能性 header，作为第二层页面头部
4. 只实现 Phase 5，不在本轮顺带重构其他页面业务逻辑

### Phase 5 实施结果 (2026-03-12)
- [x] `frontend/src/components/SiteHeader.vue` 已完成，支持桌面端导航、业务板块子菜单、移动端抽屉菜单
- [x] `frontend/src/App.vue` 已完成全局接入，并统一设置 `--site-header-offset`
- [x] 首页 / 科普表单 / 病例报告页已完成顶部结构适配
- [x] 工作流页面 (`MainView` / `SimulationView` / `SimulationRunView` / `ReportView` / `InteractionView` / `ArticleGenerateView`) 已完成高度与品牌适配
- [x] `npm run build` 已通过
- [ ] 本地人工视觉验收待执行（由用户自行启动项目）
|------|----------|
| `frontend/src/App.vue` | 在 `<router-view />` 上方引入 SiteHeader 组件 |
| `frontend/src/views/Home.vue` | `.navbar` 背景 `#000` → `#fff`，文字颜色 `#fff` → `#333` |
| `frontend/src/views/ScienceArticle.vue` | `.navbar` 背景 `#000` → `#fff`，文字颜色 `#fff` → `#333` |
| `frontend/src/views/CaseReport.vue` | `.navbar` 背景 `#000` → `#fff`，文字颜色 `#fff` → `#333` |

> 注意: MainView.vue、ArticleGenerateView.vue、SimulationView.vue、ReportView.vue 的 header 已经是白色 (`#FFF`)，无需改色。

---

### 5.1 新建 SiteHeader.vue

**文件路径**: `frontend/src/components/SiteHeader.vue`

**功能要求**:
1. 将主站 `Header.tsx` 的 React 逻辑用 Vue 3 Composition API (`<script setup>`) 重写
2. 将主站 `Header.module.css` 的样式用 Vue `<style scoped>` 重写

**导航链接改造规则**:
- 主站内部链接 (如 `/home`, `/zhicheng`) → 改为绝对 URL `https://medstarai.com/home`, `https://medstarai.com/zhicheng`
- 子菜单链接同理: `/business/overview` → `https://medstarai.com/business/overview`
- "AI写作" 链接保持原值: `https://ai.medstarai.com/medical-science`
- 所有链接用 `<a href="..." >` 标签, 非 Vue Router 的 `<router-link>`（因为都是外部跳转）

**Active 状态**:
- "AI写作" 这个 tab 在本站应**始终高亮**（加 `.another` class），因为当前站就是 AI 写作站
- 不需要 `usePathname()` 检测逻辑，直接硬编码 "AI写作" 为 active

**Vue 3 改写要点**:
- `useState` → `ref()`
- `useEffect` → `onMounted` / `onUnmounted` / `watch`
- `useRef` → `ref()` + template ref
- `usePathname()` → 不需要（active 硬编码）
- `Image` (Next.js) → 普通 `<img>` 标签
- CSS Modules → Vue `<style scoped>`，class 名直接写（不用 `styles.xxx`）

**移动端关闭按钮**:
- 主站用 `<Image src="/images/close.png" />`
- 本站改用内联 SVG（一个 × 图标），避免额外图片依赖:
```html
<svg width="14" height="14" viewBox="0 0 14 14" fill="#333">
  <path d="M1 1L13 13M13 1L1 13" stroke="#333" stroke-width="2" stroke-linecap="round"/>
</svg>
```

### 5.2 修改 App.vue

**文件路径**: `frontend/src/App.vue`

**当前内容**:
```vue
<template>
  <router-view />
</template>

<script setup>
// 使用 Vue Router 来管理页面
</script>
```

**修改为**:
```vue
<template>
  <SiteHeader />
  <router-view />
</template>

<script setup>
import SiteHeader from './components/SiteHeader.vue'
</script>
```

### 5.3 修改入口页面 Header 颜色 (黑→白)

需要修改 3 个文件的 `.navbar` 样式:

#### Home.vue (`frontend/src/views/Home.vue`)
当前样式:
```css
.navbar {
  height: 60px;
  background: var(--black);  /* #000000 */
  color: var(--white);       /* #FFFFFF */
  ...
}
```
改为:
```css
.navbar {
  height: 60px;
  background: #fff;
  color: #333;
  border-bottom: 1px solid #eaeaea;  /* 加一条分隔线替代黑色背景的视觉边界 */
  ...
}
```

#### ScienceArticle.vue (`frontend/src/views/ScienceArticle.vue`)
当前样式:
```css
.navbar {
  height: 60px;
  background: #000;
  color: #fff;
  ...
}
```
改为:
```css
.navbar {
  height: 60px;
  background: #fff;
  color: #333;
  border-bottom: 1px solid #eaeaea;
  ...
}
```
同时 `.nav-back` 的 `opacity: 0.7` 可能需要调整为 `color: #999` 以在白底上保持可读性。

#### CaseReport.vue (`frontend/src/views/CaseReport.vue`)
与 ScienceArticle.vue 相同的改法。

### 5.4 验证清单

- [ ] 桌面端 (>992px): 主站导航横向排列，Logo 左侧，7个导航项，"AI写作"蓝色高亮
- [ ] 桌面端: "业务板块" hover 时显示4项子菜单
- [ ] 移动端 (≤992px): 隐藏桌面导航，显示汉堡菜单
- [ ] 移动端: 点击汉堡后弹出导航面板，显示所有导航项
- [ ] 移动端: 点击关闭按钮或面板外区域关闭菜单
- [ ] 所有页面: 主站导航 Header 出现在页面最顶部
- [ ] Home/ScienceArticle/CaseReport: 原有 navbar 变为白色，位于主站导航下方
- [ ] MainView/ArticleGenerateView: 双层 header (主站导航 + 功能性 header)
- [ ] 所有外部链接正确指向 `https://medstarai.com/xxx`
- [ ] 构建通过: `cd frontend && npm run build`

---

## Phase 6: 统一 AI写作 导航链接 + 清理 Caddy 重定向

### 目标
1. 将主站和 AI 写作站的 "AI写作" tab 链接统一改为 `https://ai.medstarai.com`（指向首页而非不存在的 `/medical-science` 路径）
2. 删除主站 Caddy 配置中多余的 `/medical-science*` 重定向规则
3. 主站 Header.tsx 的 AI写作 active 检测逻辑需适配新链接

### 背景

当前问题：
- 主站 Header.tsx 中 AI写作 href 为 `https://ai.medstarai.com/medical-science`
- AI 站 Vue Router 中没有 `/medical-science` 路由（实际路由是 `/` 和 `/science-article`）
- Caddy 主站配置有 `@medical path /medical-science*` → `redir https://ai.medstarai.com{uri}`，这是多余的一跳
- AI 站 SiteHeader.vue 中 AI写作 href 也是 `https://ai.medstarai.com/medical-science`

### 决策 (2026-03-12)
- AI写作 tab 链接统一改为 `https://ai.medstarai.com`（首页）
- 删除 Caddy 主站的 medical-science 重定向规则
- 采用方案 A（保持子域名方案），不做路径合并

---

### 6.1 修改 AI 站 SiteHeader.vue

**文件**: `/Users/luochujian/work/newwork/MiroFish/frontend/src/components/SiteHeader.vue`

**改动**: 第 133 行，AI写作 href 改为 `https://ai.medstarai.com`

当前:
```javascript
{ href: 'https://ai.medstarai.com/medical-science', label: 'AI写作', key: 'ai-writing' },
```
改为:
```javascript
{ href: 'https://ai.medstarai.com', label: 'AI写作', key: 'ai-writing' },
```

### 6.2 修改主站 Header.tsx

**文件**: `/Users/luochujian/work/newwork/yizhibang/src/app/home/components/Header.tsx`

**改动**: 第 52 行，AI写作 href 改为 `https://ai.medstarai.com`

当前:
```javascript
{ href: "https://ai.medstarai.com/medical-science", label: "AI写作" },
```
改为:
```javascript
{ href: "https://ai.medstarai.com", label: "AI写作" },
```

**注意**: 主站 Header 的 active 检测逻辑在第 72 行:
```javascript
pathname === item.href || (item.href !== "/home" && pathname && pathname.startsWith(item.href)) || (item.href === "/home" && pathname === "/")
```
由于 AI写作 的 href 是外部绝对 URL (`https://ai.medstarai.com`)，而 `pathname` 是当前页面的相对路径（如 `/home`、`/zhicheng`），两者永远不会匹配。所以在主站上 AI写作 tab **不会被高亮**，这是正确的行为（用户在主站时不应高亮 AI写作）。无需额外修改检测逻辑。

### 6.3 修改 Caddy 配置

**文件**: 服务器上的 Caddyfile（用户需自行定位）

**改动**: 删除主站配置块中的 medical-science 重定向规则

当前:
```caddyfile
medstarai.com, www.medstarai.com {
    @medical path /medical-science*
    redir @medical https://ai.medstarai.com{uri}

    reverse_proxy 154.17.1.94:3000 {
        ...
    }
}
```

改为:
```caddyfile
medstarai.com, www.medstarai.com {
    reverse_proxy 154.17.1.94:3000 {
        header_up Host {host}
        header_up X-Real-IP {remote}
        header_up X-Forwarded-For {remote}
        header_up X-Forwarded-Proto {scheme}
    }
}
```

AI 站配置不变。

### 6.4 验证清单

- [ ] AI 站 SiteHeader.vue: AI写作 href 指向 `https://ai.medstarai.com`
- [ ] 主站 Header.tsx: AI写作 href 指向 `https://ai.medstarai.com`
- [ ] 主站 Header: 在主站浏览时 AI写作 tab 不高亮（正确行为）
- [ ] AI 站 SiteHeader: AI写作 tab 始终高亮（通过 `key: 'ai-writing'` 硬编码）
- [ ] Caddy: 删除 `@medical` 重定向后，`medstarai.com/medical-science` 不再跳转（由 Next.js 处理，可能显示 404，这是预期行为）
- [ ] 两个项目分别构建通过
- [ ] Caddy reload 后验证链路正常

---

## 关键文件

| 文件 | 状态 | 用途 |
|------|------|------|
| `frontend/src/views/Home.vue` | ✅ | 首页卡片入口 |
| `frontend/src/views/ScienceArticle.vue` | ✅ | 科普文章表单 |
| `frontend/src/views/ArticleGenerateView.vue` | 🆕 | 文章生成+互动主视图 |
| `frontend/src/router/index.js` | 需更新 | 添加生成页路由 |
| `frontend/src/api/article.js` | 🆕 | 文章生成 API 模块（或 Mock） |
| `frontend/src/components/SiteHeader.vue` | 🆕 Phase5 | 主站导航 Header 组件 (从主站 React 重写为 Vue 3) |
| `frontend/src/App.vue` | 需更新 Phase5 | 全局引入 SiteHeader |

## 设计参考（从现有代码复用）

| 原组件 | 复用内容 |
|--------|----------|
| `ReportView.vue` | 页面布局结构、Header、视图模式切换 |
| `Step4Report.vue` | 左栏文章渲染、右栏时间线、工作流步骤树、轮询机制 |
| `Step5Interaction.vue` | 聊天界面、消息气泡、markdown 渲染、输入框 |

## 决策记录
- 保留现有设计系统（配色、字体、动画风格）
- 一步步来，不多做
- Phase 3 合并 Step4+Step5 为一个页面（生成完成后右栏切换为聊天）
- 先 Mock UI，后接 API
- 保留多步骤流程架构，未来可在生成前插入"文献检索"等步骤

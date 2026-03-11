# Findings: 项目研究记录

## 现有技术栈
- 前端: Vue 3 + Vite + Vue Router 4
- 样式: 纯 CSS（无框架），CSS 变量主题
- 字体: JetBrains Mono / Space Grotesk / Noto Sans SC / Inter
- 配色: 黑(#000) 白(#FFF) 橙(#FF4500) 灰(#666/#999/#E5E5E5)

## 首页现有结构 (Home.vue, ~890行)
1. 导航栏 — 黑底，"MIROFISH" + GitHub 链接
2. Hero 区 — 标语、描述、Logo、滚动按钮
3. Dashboard 区 — 左侧指标+工作流，右侧上传控制台
4. 历史记录区 — HistoryDatabase 组件

## 原 MiroFish Step4 报告生成架构（Phase 3 参考）

### 核心模式：大纲优先 → 逐段生成
1. Agent 先输出 `planning_complete`（含 outline: title, summary, sections）
2. 逐个 section 生成：`section_start` → `tool_call/result` → `llm_response` → `section_complete`
3. 最终 `report_complete`

### 关键技术点
- **增量轮询**：GET agent-log?from_line=N，每 2s 拉取新日志
- **双栏布局**：左栏文章 + 右栏时间线，支持 graph/split/workbench 三种模式
- **状态驱动**：reportOutline → generatedSections{} → isComplete
- **Markdown 渲染**：自实现 renderMarkdown()，支持标题/列表/代码/引用

### Step5 深度互动
- 右栏切换为聊天界面
- 支持两种对话目标：Report Agent / 模拟个体
- 聊天历史按目标分别缓存（chatHistoryCache）
- POST /api/report/chat 与 agent 对话

### 关键 API 端点
- POST `/api/report/generate` → { report_id }
- GET `/api/report/{id}/agent-log?from_line=N` → { from_line, logs }
- POST `/api/report/chat` → { response }

## 原始 console-section 步骤式设计（供 Phase 2 参考）
- 容器：`.console-box` 双边框（外 1px 实线 + 8px padding）
- 每步：`.console-section`（padding 20px）
  - 头部：`.console-header`（flex, 左 `.console-label` 如 `01 / 现实种子`，右 `.console-meta`）
  - 标签字体：JetBrains Mono, 0.75rem, #666
- 步骤间：`.console-divider`（左右线 + 中间文字如"输入参数"）
- 底部按钮：`.start-engine-btn`（全宽黑底按钮，hover 变橙，pulse-border 动画）
- 上传区域：`.upload-zone`（虚线边框，支持多文件拖拽+点击，`multiple` 属性）
- 输入区域：`.input-wrapper` + `.code-input`（textarea，JetBrains Mono 字体）

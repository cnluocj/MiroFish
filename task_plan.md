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

## 关键文件

| 文件 | 状态 | 用途 |
|------|------|------|
| `frontend/src/views/Home.vue` | ✅ | 首页卡片入口 |
| `frontend/src/views/ScienceArticle.vue` | ✅ | 科普文章表单 |
| `frontend/src/views/ArticleGenerateView.vue` | 🆕 | 文章生成+互动主视图 |
| `frontend/src/router/index.js` | 需更新 | 添加生成页路由 |
| `frontend/src/api/article.js` | 🆕 | 文章生成 API 模块（或 Mock） |

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

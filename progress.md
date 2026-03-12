# Progress Log

## Session 1 — 2026-03-11

### 完成
- [x] 项目结构研究
- [x] 首页现有代码分析
- [x] 制定改造计划

### 待执行
- [x] Phase 1: 首页改造 — 完成

## Session 2 — 2026-03-11

### 完成
- [x] frontend/index.html — 更新 title/meta
- [x] frontend/src/views/Home.vue — 全部重写：移除 Hero/Dashboard/HistoryDatabase，新增3张卡片入口
- [x] frontend/src/router/index.js — 添加 /science-article 和 /case-report 路由
- [x] frontend/src/views/ScienceArticle.vue — 新建占位页面
- [x] frontend/src/views/CaseReport.vue — 新建占位页面

## Session 3 — 2026-03-11

### 完成
- [x] 新建分支 feat/yiluda-homepage，提交 Phase 1 改动
- [x] Phase 2: ScienceArticle.vue 重写为完整表单页面（6步骤，界面完成，功能暂不接通）

## Session 4 — 2026-03-11

### 完成
- [x] 深入研究 Step4Report + Step5Interaction 代码架构
- [x] 制定 Phase 3 计划：文章生成 + 深度互动

### 待执行
- [x] Phase 3.1: 路由 + 页面骨架
- [x] Phase 3.2: Mock 数据驱动完整 UI
- [ ] Phase 3.3: 对接真实 API

## Session 5 — 2026-03-11

### 完成
- [x] 新建 frontend/src/store/articleForm.js — 表单数据传递 store
- [x] 新建 frontend/src/views/ArticleGenerateView.vue — 文章生成+互动页面（含 Mock 数据）
- [x] 更新 frontend/src/router/index.js — 添加 /science-article/generate/:taskId 路由
- [x] 更新 frontend/src/views/ScienceArticle.vue — 表单提交后跳转到生成页面
- [x] 构建验证通过

## Session 6 — 2026-03-11

### 完成
- [x] 4.1 CaseReport.vue — 开发中提示页面（进度条 + 脉冲动画 + 工作流步骤）
- [x] 4.2 ScienceArticle.vue — 目标读者改为单选（普通大众/患者及家属/医护同行）
- [x] 4.3 ScienceArticle.vue — 科室选择后自动填充科普主题（12个科室映射）
- [x] 4.4 ScienceArticle.vue — 双栏布局改造（左侧工作流6步骤 + 右侧表单）
- [x] 构建验证通过

## Session 7 — 2026-03-12

### 完成
- [x] 研究主站 yizhibang Header 组件 (Header.tsx + Header.module.css)
- [x] 研究当前项目所有页面的 header 实现 (7个页面)
- [x] 识别技术栈差异 (React CSS Modules → Vue Scoped CSS)
- [x] 识别导航项和路由改造需求
- [x] 制定 Phase 5 计划

### 待执行
- [ ] Phase 5: 集成主站 Header (用户确认后开始实现)

## Session 8 — 2026-03-12

### 完成
- [x] 基于主站 Header 与当前 Vue 页面结构，确定 Phase 5 接入策略
- [x] 确认全局接入点为 `frontend/src/App.vue`
- [x] 确认受影响页面范围（Home / ScienceArticle / CaseReport / MainView / SimulationView / ReportView / ArticleGenerateView）
- [x] 新建 `frontend/src/components/SiteHeader.vue`
- [x] 更新 `frontend/src/App.vue` 全局挂载主站 Header
- [x] 完成入口页与工作流页的顶部布局适配
- [x] `npm run build` 构建通过

### 待执行
- [ ] 用户本地启动后进行人工视觉验收

## Session 9 — 2026-03-12

### 完成
- [x] 分析 Caddy 配置和导航链路问题
- [x] 确定方案 A（保持子域名），AI写作链接改为 `https://ai.medstarai.com`
- [x] 制定 Phase 6 计划（含主站 + AI站 + Caddy 三处改动）
- [x] Phase 6 代码改动完成（SiteHeader.vue + Header.tsx），Caddy 由用户手动修改
- [x] 深入研究后端架构（ReportAgent, LLMClient, TaskManager, 日志系统）
- [x] 研究前端 ArticleGenerateView.vue 完整代码（mock 逻辑、UI 状态驱动）
- [x] 制定 Phase 3.3 详细计划（ArticleAgent + API + 前端改造 + Docker）

### 待执行
- [ ] Phase 3.3: 对接真实 LLM API（用户确认后开始实现）

## Session 10 — 2026-03-12

### 完成
- [x] 恢复 Phase 3.3 上下文并确认新任务为“真实 LLM API 对接”
- [x] 复核后端可复用能力（LLMClient / TaskManager / ReportLogger 模式）
- [x] 复核前端现有 mock 生成逻辑和提交链路
- [x] 确定实现路径为新增独立 `article` 服务和 API

### 进行中
- [x] 后端实现 `ArticleAgent + /api/article/*`
- [x] 前端将 ScienceArticle / ArticleGenerateView 接到真实 API

### 完成
- [x] 新建 `backend/app/services/article_agent.py`
- [x] 新建 `backend/app/api/article.py`
- [x] 注册 `article` blueprint 到 Flask app
- [x] 新建 `frontend/src/api/article.js`
- [x] `ScienceArticle.vue` 接入真实生成启动接口
- [x] `ArticleGenerateView.vue` 接入真实日志轮询与聊天接口
- [x] `python3 -m py_compile` 通过
- [x] `npm run build` 通过

### 待执行
- [ ] 用户本地以真实 LLM 配置完成一次端到端生成验证

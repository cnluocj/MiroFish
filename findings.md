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

---

## Phase 5 调研：集成主站 Header

### 主站 Header 组件 (yizhibang)

**源文件:**
- `/yizhibang/src/app/home/components/Header.tsx` (React, 'use client')
- `/yizhibang/src/app/home/components/Header.module.css`

**技术栈差异:**
| 项目 | 框架 | 样式方案 |
|------|------|----------|
| 主站 yizhibang | Next.js 15 + React 19 | CSS Modules |
| 当前项目 MiroFish | Vue 3 + Vite | Scoped CSS |

**导航项 (7项):**
| 导航 | URL | 类型 | 备注 |
|------|-----|------|------|
| 网站首页 | `/home` | 主站内部 | → `https://medstarai.com/home` |
| 职称评审 | `/zhicheng` | 主站内部 | → `https://medstarai.com/zhicheng` |
| 业务板块 | `/business` | 主站内部 | → `https://medstarai.com/business` (有4子菜单) |
| **AI写作** | `https://ai.medstarai.com/medical-science` | 外部 | **当前项目，应高亮** |
| 培训课程 | `/training` | 主站内部 | → `https://medstarai.com/training` |
| 新闻通知 | `/news` | 主站内部 | → `https://medstarai.com/news` |
| 关于我们 | `/about` | 主站内部 | → `https://medstarai.com/about` |

**业务板块子菜单 (4项):**
- 业务概述 → `https://medstarai.com/business/overview`
- 课题申报指导 → `https://medstarai.com/business/research`
- 著作出书 → `https://medstarai.com/business/publication`
- 健康科普 → `https://medstarai.com/business/health`

**主站 Header 样式关键参数:**
- 背景: `#fff` (白色), 阴影: `0 2px 4px rgba(0,0,0,0.1)`
- 导航文字: `#333`, `16px`
- 激活态: `#007bff` 蓝色背景 + 白色文字, `border-radius: 50px`
- Logo: `医职帮logo.png` (高50px, 右边距140px)
- 桌面端: `.topBg`, 最大宽度 1200px
- 移动端: `.phoneHeader` (992px以下显示), 汉堡菜单 + 弹出导航

**路由检测逻辑 (React usePathname):**
```
pathname === item.href ||
(item.href !== "/home" && pathname.startsWith(item.href)) ||
(item.href === "/home" && pathname === "/")
```

### 当前项目 Header 现状

**无独立 Header 组件**, 代码直接写在每个 view 文件中。

**各页面 Header 颜色:**
| 页面 | 背景色 | Header 类型 |
|------|--------|-------------|
| Home.vue | 黑色 `#000` | 简单 nav (品牌名) |
| ScienceArticle.vue | 黑色 `#000` | nav + 返回按钮 |
| CaseReport.vue | 黑色 `#000` | nav + 返回按钮 |
| MainView.vue | 白色 `#FFF` | 功能性 (视图切换+步骤指示器) |
| ArticleGenerateView.vue | 白色 `#FFF` | 功能性 (视图切换+步骤指示器) |
| SimulationView.vue | 白色 `#FFF` | 功能性 |
| ReportView.vue | 白色 `#FFF` | 功能性 |

### 核心挑战
1. **React → Vue**: 需将 React 组件重写为 Vue 3 组件
2. **路由改造**: 主站内部链接需改为 `https://medstarai.com` 的绝对 URL
3. **资源依赖**: Logo 图片需复制到本项目或用绝对 URL 引用
4. **Active 状态**: "AI写作" tab 在本站应始终处于高亮状态
5. **双层 Header**: 工作流页面已有功能性 header，主站导航应叠加在上方
6. **黑色 Header → 白色**: 入口页面的黑色 header 需改为白色以统一风格

### Phase 5 实现补充结论 (2026-03-12)
- 当前项目最合适的接入点是 `frontend/src/App.vue`，因为现有路由页面都直接挂在 `router-view`
- 首页、科普表单页、病例报告页仍保留旧黑色 navbar，需删除以避免与主站白色导航重复
- `ScienceArticle.vue` 左侧面板使用 `position: sticky; top: 80px;`，接入全局 Header 后需要改成基于全局 CSS 变量的偏移
- `MainView.vue`、`SimulationView.vue`、`ReportView.vue`、`ArticleGenerateView.vue` 当前都是 `height: 100vh` 的双层布局，接入全局 Header 后需要改成 `calc(100vh - var(--site-header-offset))`
- 主站 Header 的移动端关闭按钮可以直接用内联 SVG，不需要额外引入 `close.png`

### Phase 5 已实现项 (2026-03-12)
- 新增 `SiteHeader.vue`，按 Vue 3 重写主站 Header，并将站内链接统一改成 `https://medstarai.com/*`
- 在当前 AI 写作站内，导航高亮固定落在“AI写作”
- 通过 `App.vue` 注入全局顶部占位变量，避免固定 Header 压住页面内容
- 入口型页面改成依赖全局 Header；工作流页面继续保留本地功能性 header 作为第二层头部
- 构建验证通过，未发现编译级错误

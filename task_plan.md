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

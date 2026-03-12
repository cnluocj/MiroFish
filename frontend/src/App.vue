<template>
  <SiteHeader />
  <div class="app-shell">
    <router-view />
  </div>
</template>

<script setup>
import SiteHeader from './components/SiteHeader.vue'
</script>

<style>
:root {
  --site-header-height-desktop: 70px;
  --site-header-height-mobile: 50px;
  --site-header-offset: var(--site-header-height-desktop);
}

@media (max-width: 992px) {
  :root {
    --site-header-offset: var(--site-header-height-mobile);
  }
}

/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  font-family: 'JetBrains Mono', 'Space Grotesk', 'Noto Sans SC', monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #000000;
  background-color: #ffffff;
}

body {
  overflow-x: hidden;
}

.app-shell {
  min-height: 100vh;
  padding-top: var(--site-header-offset);
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #000000;
}

::-webkit-scrollbar-thumb:hover {
  background: #333333;
}

/* 全局按钮样式 */
button {
  font-family: inherit;
}
</style>

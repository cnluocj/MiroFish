<template>
  <div class="site-header desktop-header">
    <div class="site-header__inner">
      <a class="site-header__logo" :href="homeUrl" aria-label="医职帮首页">
        <img
          src="https://medstarai.com/images/home/%E5%8C%BB%E8%81%8C%E5%B8%AElogo.png"
          alt="医职帮 Logo"
        />
      </a>

      <nav class="site-nav" aria-label="主站导航">
        <ul class="site-nav__list">
          <li
            v-for="item in navItems"
            :key="item.href"
            class="site-nav__item"
            :class="{ 'is-active': isActive(item) }"
          >
            <a class="site-nav__link" :href="item.href">
              <span>{{ item.label }}</span>
            </a>

            <ul v-if="item.submenu" class="site-nav__submenu">
              <li v-for="subItem in item.submenu" :key="subItem.href">
                <a :href="subItem.href">{{ subItem.label }}</a>
              </li>
            </ul>
          </li>
        </ul>
      </nav>
    </div>
  </div>

  <div class="site-header mobile-header" :class="{ 'menu-open': isMobileMenuOpen }">
    <div class="mobile-header__inner">
      <a class="mobile-header__logo" :href="homeUrl" aria-label="医职帮首页">
        <img
          src="https://medstarai.com/images/home/%E5%8C%BB%E8%81%8C%E5%B8%AElogo.png"
          alt="医职帮 Logo"
        />
      </a>

      <button
        class="mobile-header__menu"
        type="button"
        aria-label="打开导航菜单"
        :aria-expanded="String(isMobileMenuOpen)"
        @click="toggleMobileMenu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </div>

  <div
    v-if="isMobileMenuOpen"
    class="mobile-flyout"
    @click="closeMobileMenu"
  >
    <div
      ref="navBoxRef"
      class="mobile-flyout__panel"
      @click.stop
    >
      <button
        class="mobile-flyout__close"
        type="button"
        aria-label="关闭导航菜单"
        @click="closeMobileMenu"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 6l12 12"></path>
          <path d="M18 6L6 18"></path>
        </svg>
      </button>

      <h4>快捷导航</h4>

      <ul class="mobile-flyout__list">
        <li v-for="item in navItems" :key="item.href">
          <a
            class="mobile-flyout__link"
            :class="{ 'is-active': isActive(item) }"
            :href="item.href"
            @click="closeMobileMenu"
          >
            {{ item.label }}
          </a>

          <ul v-if="item.submenu" class="mobile-flyout__submenu">
            <li v-for="subItem in item.submenu" :key="subItem.href">
              <a
                class="mobile-flyout__sublink"
                :href="subItem.href"
                @click="closeMobileMenu"
              >
                {{ subItem.label }}
              </a>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const navBoxRef = ref(null)
const isMobileMenuOpen = ref(false)

const homeUrl = 'https://medstarai.com/home'
const siteBaseUrl = 'https://medstarai.com'

const navItems = computed(() => [
  { href: `${siteBaseUrl}/home`, label: '网站首页' },
  { href: `${siteBaseUrl}/zhicheng`, label: '职称评审' },
  {
    href: `${siteBaseUrl}/business`,
    label: '业务板块',
    submenu: [
      { href: `${siteBaseUrl}/business/overview`, label: '业务概述' },
      { href: `${siteBaseUrl}/business/research`, label: '课题申报指导' },
      { href: `${siteBaseUrl}/business/publication`, label: '著作出书' },
      { href: `${siteBaseUrl}/business/health`, label: '健康科普' }
    ]
  },
  { href: 'https://ai.medstarai.com/medical-science', label: 'AI写作', key: 'ai-writing' },
  { href: `${siteBaseUrl}/training`, label: '培训课程' },
  { href: `${siteBaseUrl}/news`, label: '新闻通知' },
  { href: `${siteBaseUrl}/about`, label: '关于我们' }
])

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const isActive = (item) => {
  return item.key === 'ai-writing'
}

const handleOutsideClick = (event) => {
  if (navBoxRef.value && !navBoxRef.value.contains(event.target)) {
    closeMobileMenu()
  }
}

const handleEscape = (event) => {
  if (event.key === 'Escape') {
    closeMobileMenu()
  }
}

watch(
  () => route.fullPath,
  () => {
    closeMobileMenu()
  }
)

watch(isMobileMenuOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})

onMounted(() => {
  document.addEventListener('mousedown', handleOutsideClick)
  document.addEventListener('keydown', handleEscape)
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  document.removeEventListener('mousedown', handleOutsideClick)
  document.removeEventListener('keydown', handleEscape)
})
</script>

<style scoped>
.site-header,
.mobile-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: #fff;
}

.site-header {
  z-index: 1000;
  padding: 10px 0;
}

.site-header__inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
  display: flex;
  align-items: center;
}

.site-header__logo {
  margin-right: 140px;
  flex-shrink: 0;
}

.site-header__logo img {
  display: block;
  height: 50px;
  width: auto;
}

.site-nav {
  flex: 1;
}

.site-nav__list {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
}

.site-nav__item {
  position: relative;
  min-width: 110px;
  margin: 0 5px;
  text-align: center;
}

.site-nav__item:first-child {
  margin-left: 0;
}

.site-nav__item:last-child {
  margin-right: 0;
}

.site-nav__link {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 10px;
  color: #333;
  text-decoration: none;
  font-size: 16px;
  white-space: nowrap;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.site-nav__item.is-active .site-nav__link {
  background: #007bff;
  color: #fff;
  border-radius: 50px;
}

.site-nav__item:hover .site-nav__link {
  background: #f0f0f0;
}

.site-nav__item.is-active:hover .site-nav__link {
  background: #0056b3;
}

.site-nav__submenu {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  min-width: 160px;
  margin: 0;
  padding: 6px 0;
  list-style: none;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
  opacity: 0;
  visibility: hidden;
  transform: translateY(4px);
  transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s ease;
  z-index: 1010;
}

.site-nav__item:hover .site-nav__submenu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.site-nav__submenu a {
  display: block;
  padding: 8px 15px;
  color: #333;
  font-size: 14px;
  text-decoration: none;
  white-space: nowrap;
}

.site-nav__submenu a:hover {
  background: #f0f0f0;
}

.mobile-header {
  display: none;
  z-index: 1999;
  padding: 10px 15px;
}

.mobile-header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mobile-header__logo img {
  display: block;
  height: 30px;
  width: auto;
}

.mobile-header__menu {
  border: none;
  background: transparent;
  padding: 5px;
  border-radius: 5px;
  cursor: pointer;
}

.mobile-header__menu span {
  display: block;
  width: 24px;
  height: 3px;
  margin: 5px 0;
  background: #333;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.mobile-header.menu-open .mobile-header__menu span:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}

.mobile-header.menu-open .mobile-header__menu span:nth-child(2) {
  opacity: 0;
}

.mobile-header.menu-open .mobile-header__menu span:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}

.mobile-flyout {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background: rgba(0, 0, 0, 0.5);
  padding: 20px 0;
  overflow-y: auto;
}

.mobile-flyout__panel {
  position: relative;
  width: min(90%, 360px);
  margin: 50px auto 0;
  padding: 25px 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.mobile-flyout__close {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  background: #f0f0f0;
  color: #333;
  cursor: pointer;
}

.mobile-flyout__close svg {
  width: 14px;
  height: 14px;
}

.mobile-flyout h4 {
  margin: 0 0 20px;
  padding-bottom: 15px;
  text-align: center;
  color: #333;
  font-size: 18px;
  font-weight: 600;
  position: relative;
}

.mobile-flyout h4::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 40px;
  height: 3px;
  transform: translateX(-50%);
  border-radius: 999px;
  background: #007bff;
}

.mobile-flyout__list,
.mobile-flyout__submenu {
  list-style: none;
  margin: 0;
  padding: 0;
}

.mobile-flyout__list > li + li {
  margin-top: 4px;
}

.mobile-flyout__link,
.mobile-flyout__sublink {
  display: block;
  padding: 12px 15px;
  color: #333;
  text-decoration: none;
  border-radius: 8px;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.mobile-flyout__link {
  font-size: 16px;
  font-weight: 500;
}

.mobile-flyout__link:hover,
.mobile-flyout__link.is-active {
  background: #f0f8ff;
  color: #007bff;
}

.mobile-flyout__submenu {
  margin: 5px 0 10px 20px;
  padding-left: 12px;
  border-left: 2px solid #e0e0e0;
}

.mobile-flyout__sublink {
  padding: 8px 15px;
  font-size: 14px;
  color: #555;
}

.mobile-flyout__sublink:hover {
  color: #007bff;
}

@media (max-width: 992px) {
  .site-header {
    display: none;
  }

  .mobile-header {
    display: block;
  }
}

@media (min-width: 993px) {
  .mobile-flyout {
    display: none;
  }
}
</style>

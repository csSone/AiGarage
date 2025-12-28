<script setup lang="ts">

// 导航栏数据
const navItems = [
  { name: '首页', path: '/' },
  { name: 'Z-Index演示', path: '/position' },
  { name: '项目', path: '/projects' },
  { name: '文档', path: '/docs' },
  { name: '关于', path: '/about' }
]


</script>

<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- Logo -->
      <div class="nav-logo">
        <h2>AiGarage</h2>
      </div>

      <!-- 导航菜单 -->
      <div class="nav-menu">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
        >
          {{ item.name }}
        </router-link>
      </div>

      <!-- 右侧按钮 -->
      <div class="nav-actions">
        <button class="nav-btn">开始使用</button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background: white;
  border-bottom: 1px solid #e9ecef;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.nav-logo h2 {
  color: #667eea;
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}

.nav-menu {
  display: flex;
  gap: 30px;
}

.nav-link {
  color: #495057;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
  position: relative;
}

.nav-link:hover {
  color: #667eea;
}

.nav-link.router-link-active {
  color: #667eea;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -22px;
  left: 0;
  right: 0;
  height: 3px;
  background: #667eea;
  border-radius: 2px 2px 0 0;
}

.nav-actions {
  display: flex;
  align-items: center;
}

.nav-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 25px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.nav-btn:hover {
  background: #5a67d8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 15px;
  }

  .nav-menu {
    display: none; /* 在小屏幕上隐藏菜单，后续可以添加汉堡菜单 */
  }

  .nav-logo h2 {
    font-size: 20px;
  }

  .nav-btn {
    padding: 8px 16px;
    font-size: 14px;
  }
}
</style>
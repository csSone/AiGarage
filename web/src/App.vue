<script setup>
import NavBar from './components/NavBar.vue'
import CopyrightIcp from './components/CopyrightIcp.vue';
</script>

<template>
  <div class="app-layout">
    <!-- 导航栏 -->
    <NavBar />

    <!-- 主要内容区域 - 路由视图 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 页脚区域 -->
    <footer class="app-footer">
      <CopyrightIcp />
    </footer>
  </div>
</template>

<style>
/* 重置默认样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

.app-layout {
  min-height: 100vh; /* 视口高度 */
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1; /* 占据剩余空间 */
  display: flex;
  flex-direction: column;
}

.app-footer {
  flex-shrink: 0; /* 不收缩 */
  width: 100%;
}
</style>

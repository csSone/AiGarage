<script setup lang="ts">
// No reactive state needed for this component
</script>

<template>
  <div class="scoped-demo">
    <h2>Scoped CSS演示</h2>

    <div class="box scoped-box">
      <h3>Scoped样式盒子</h3>
      <p>这个盒子使用scoped样式</p>
    </div>

    <div class="box global-box">
      <h3>全局样式盒子</h3>
      <p>这个盒子使用全局样式</p>
    </div>

    <div class="demo-section">
      <h4>样式对比</h4>
      <button class="scoped-btn">Scoped按钮</button>
      <button class="global-btn">全局按钮</button>
    </div>

    <!-- 子组件样式测试 -->
    <div class="child-test">
      <h4>子组件样式测试</h4>
      <div class="test-content">
        <p>测试内容 - 尝试用scoped样式影响我</p>
      </div>
    </div>
  </div>
</template>

<!-- Scoped样式 - 只影响当前组件 -->
<style scoped>
.scoped-demo {
  padding: 20px;
  border: 2px solid #3b82f6;
  border-radius: 8px;
  margin: 20px 0;
}

.scoped-demo h2 {
  color: #3b82f6;
  text-align: center;
  margin-bottom: 20px;
}

.box {
  padding: 15px;
  margin: 10px 0;
  border-radius: 5px;
  text-align: center;
}

.scoped-box {
  background: #dbeafe;
  border: 2px solid #3b82f6;
  color: #1e40af;
}

.global-box {
  background: #fef3c7;
  border: 2px solid #f59e0b;
  color: #92400e;
}

.demo-section {
  margin: 20px 0;
  text-align: center;
}

.demo-section h4 {
  margin-bottom: 15px;
  color: #374151;
}

.scoped-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 0 10px;
  border-radius: 5px;
  cursor: pointer;
}

.scoped-btn:hover {
  background: #2563eb;
}

/* 测试scoped样式的影响范围 */
.child-test {
  margin: 20px 0;
  padding: 15px;
  background: #f3f4f6;
  border-radius: 5px;
}

.child-test h4 {
  color: #374151;
  margin-bottom: 10px;
}

/* 这个样式不会影响.test-content，因为它在子组件结构中 */
.test-content {
  /* 在scoped中，这个样式可能不会按预期工作 */
  border: 1px solid #d1d5db;
  padding: 10px;
  border-radius: 3px;
}

/* 使用深度选择器影响子元素 */
:deep(.test-content) {
  background: #e0e7ff;
  border-color: #6366f1;
}

/* 滑动动画 */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scoped-demo {
  animation: slideIn 0.5s ease-out;
}
</style>

<!-- 全局样式 - 影响整个应用 -->
<style>
/* 全局按钮样式 - 可能影响其他组件 */
.global-btn {
  background: #10b981;
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 0 10px;
  border-radius: 5px;
  cursor: pointer;
}

.global-btn:hover {
  background: #059669;
}

/* 全局警告类 */
.warning {
  color: #ef4444;
  font-weight: bold;
}

/* 全局工具类 */
.text-center {
  text-align: center;
}

.mb-20 {
  margin-bottom: 20px;
}
</style>
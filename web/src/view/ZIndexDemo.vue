<script setup lang="ts">
import { ref } from 'vue'

// 当前显示的层级
const currentZIndex = ref(1)

const layers = [
  { name: '底层', z: 1, color: '#fee2e2', border: '#ef4444' },
  { name: '中层', z: 10, color: '#dbeafe', border: '#3b82f6' },
  { name: '顶层', z: 100, color: '#d1fae5', border: '#10b981' }
]

const showLayer = (z: number) => {
  currentZIndex.value = z
}
</script>

<template>
  <div class="z-index-demo">
    <h1>z-index 层级演示</h1>

    <!-- 控制按钮 -->
    <div class="controls">
      <button
        v-for="layer in layers"
        :key="layer.z"
        @click="showLayer(layer.z)"
        :class="{ active: currentZIndex === layer.z }"
        class="control-btn"
      >
        显示 {{ layer.name }} (z-index: {{ layer.z }})
      </button>
    </div>

    <!-- 层级演示区域 -->
    <div class="demo-stage">
      <div class="stage-label">层级演示区域</div>

      <!-- 底层 -->
      <div
        class="layer bottom-layer"
        :style="{ zIndex: currentZIndex >= 1 ? 1 : -1 }"
        :class="{ visible: currentZIndex >= 1 }"
      >
        <div class="layer-content">
          <h3>底层</h3>
          <p>z-index: 1</p>
          <div class="layer-desc">这是最底层元素</div>
        </div>
      </div>

      <!-- 中层 -->
      <div
        class="layer middle-layer"
        :style="{ zIndex: currentZIndex >= 10 ? 10 : -1 }"
        :class="{ visible: currentZIndex >= 10 }"
      >
        <div class="layer-content">
          <h3>中层</h3>
          <p>z-index: 10</p>
          <div class="layer-desc">这是中间层元素</div>
        </div>
      </div>

      <!-- 顶层 -->
      <div
        class="layer top-layer"
        :style="{ zIndex: currentZIndex >= 100 ? 100 : -1 }"
        :class="{ visible: currentZIndex >= 100 }"
      >
        <div class="layer-content">
          <h3>顶层</h3>
          <p>z-index: 100</p>
          <div class="layer-desc">这是最顶层元素</div>
        </div>
      </div>
    </div>

    <!-- 说明文字 -->
    <div class="explanation">
      <h2>z-index 规则说明</h2>
      <ul>
        <li><strong>数值越大，层级越高</strong>：z-index: 100 在 z-index: 10 之上</li>
        <li><strong>必须配合定位</strong>：position: relative/absolute/fixed/sticky</li>
        <li><strong>负数有效</strong>：z-index: -1 会在 z-index: 0 下面</li>
        <li><strong>默认值</strong>：auto (相当于0)</li>
      </ul>
    </div>

    <!-- 实际应用例子 -->
    <div class="real-examples">
      <h2>实际应用场景</h2>

      <div class="example-grid">
        <!-- 模态框例子 -->
        <div class="example-card">
          <h3>模态框 (z-index: 1000)</h3>
          <div class="example-scene">
            <div class="modal-backdrop">背景遮罩 (z-index: 999)</div>
            <div class="modal-content">模态框内容 (z-index: 1000)</div>
          </div>
        </div>

        <!-- 导航栏例子 -->
        <div class="example-card">
          <h3>导航栏 (z-index: 100)</h3>
          <div class="example-scene">
            <div class="navbar-example">导航栏</div>
            <div class="content-example">页面内容</div>
          </div>
        </div>

        <!-- 工具提示例子 -->
        <div class="example-card">
          <h3>工具提示 (z-index: 50)</h3>
          <div class="example-scene">
            <div class="button-example">按钮</div>
            <div class="tooltip">工具提示</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.z-index-demo {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

h1, h2 {
  text-align: center;
  color: #1f2937;
}

h1 {
  margin-bottom: 30px;
}

h2 {
  margin: 40px 0 20px 0;
  color: #374151;
}

/* 控制按钮 */
.controls {
  text-align: center;
  margin-bottom: 40px;
}

.control-btn {
  background: #e5e7eb;
  border: none;
  padding: 10px 20px;
  margin: 0 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s;
}

.control-btn:hover {
  background: #d1d5db;
}

.control-btn.active {
  background: #3b82f6;
  color: white;
}

/* 演示舞台 */
.demo-stage {
  position: relative;
  width: 100%;
  height: 400px;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  margin: 20px 0;
  overflow: hidden;
}

.stage-label {
  position: absolute;
  top: 10px;
  left: 10px;
  color: #6b7280;
  font-size: 12px;
  z-index: 0;
}

/* 层级元素 */
.layer {
  position: absolute;
  width: 300px;
  height: 200px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.5s ease;
  border: 3px solid;
  opacity: 0.3;
}

.layer.visible {
  opacity: 1;
}

.bottom-layer {
  background: #fee2e2;
  border-color: #ef4444;
  width: 350px;
  height: 250px;
}

.middle-layer {
  background: #dbeafe;
  border-color: #3b82f6;
  width: 300px;
  height: 200px;
}

.top-layer {
  background: #d1fae5;
  border-color: #10b981;
  width: 250px;
  height: 150px;
}

.layer-content {
  text-align: center;
}

.layer-content h3 {
  margin: 0 0 5px 0;
  font-size: 18px;
}

.layer-content p {
  margin: 0 0 10px 0;
  font-weight: bold;
  font-size: 14px;
}

.layer-desc {
  font-size: 12px;
  opacity: 0.8;
}

/* 说明区域 */
.explanation {
  background: #f3f4f6;
  padding: 20px;
  border-radius: 8px;
  margin: 30px 0;
}

.explanation ul {
  margin: 0;
  padding-left: 20px;
}

.explanation li {
  margin: 10px 0;
  line-height: 1.5;
}

/* 实际应用例子 */
.example-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.example-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
}

.example-card h3 {
  margin: 0 0 15px 0;
  color: #374151;
  text-align: center;
}

.example-scene {
  position: relative;
  height: 150px;
  background: #f9fafb;
  border-radius: 5px;
  overflow: hidden;
}

/* 模态框例子 */
.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.modal-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border-radius: 5px;
  z-index: 1000;
}

/* 导航栏例子 */
.navbar-example {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50px;
  background: #3b82f6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.content-example {
  position: absolute;
  top: 60px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

/* 工具提示例子 */
.button-example {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #6b7280;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  z-index: 10;
}

.tooltip {
  position: absolute;
  top: 30%;
  left: 60%;
  background: #1f2937;
  color: white;
  padding: 5px 10px;
  border-radius: 3px;
  font-size: 12px;
  z-index: 50;
}

.tooltip::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 20px;
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid #1f2937;
}
</style>
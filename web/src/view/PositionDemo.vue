<script setup lang="ts">
// 定位演示数据
const positioningTypes = [
  {
    name: 'Static (默认)',
    description: '正常文档流，不特殊定位',
    position: 'static',
    color: '#667eea'
  },
  {
    name: 'Relative',
    description: '相对定位，相对于原位置偏移',
    position: 'relative',
    color: '#48bb78'
  },
  {
    name: 'Absolute',
    description: '绝对定位，相对于最近已定位祖先元素',
    position: 'absolute',
    color: '#ed8936'
  },
  {
    name: 'Fixed',
    description: '固定定位，相对于视口固定',
    position: 'fixed',
    color: '#e53e3e'
  },
  {
    name: 'Sticky',
    description: '粘性定位，滚动时在指定位置固定',
    position: 'sticky',
    color: '#38b2ac'
  }
]
</script>

<template>
  <div class="demo-container">
    <h1>CSS定位属性演示</h1>

    <!-- 演示区域 -->
    <div class="demo-area">
      <h2>1. 不同定位类型对比</h2>

      <div class="positioning-demo">
        <!-- 静态定位 -->
        <div class="demo-box static-box">
          <h3>Static</h3>
          <p>正常文档流</p>
        </div>

        <!-- 相对定位 -->
        <div class="demo-box relative-box">
          <h3>Relative</h3>
          <p>top: 20px, left: 20px</p>
        </div>

        <!-- 绝对定位演示容器 -->
        <div class="absolute-container">
          <h4>绝对定位容器 (position: relative)</h4>
          <div class="demo-box absolute-box">
            <h3>Absolute</h3>
            <p>bottom: 10px, right: 10px</p>
          </div>
        </div>
      </div>

      <!-- Fixed定位演示 -->
      <div class="fixed-demo">
        <h2>2. Fixed定位 (固定在右上角)</h2>
        <div class="fixed-box">
          Fixed Box
        </div>
      </div>

      <!-- Sticky定位演示 -->
      <div class="sticky-demo">
        <h2>3. Sticky定位 (滚动时固定)</h2>
        <div class="sticky-header">
          滚动时我会固定在顶部
        </div>

        <!-- 模拟长内容 -->
        <div class="long-content">
          <p v-for="i in 20" :key="i">内容段落 {{ i }} - 向下滚动查看sticky效果</p>
        </div>
      </div>

      <!-- Z-index 演示 -->
      <div class="z-index-demo">
        <h2>4. Z-index 层级关系</h2>
        <div class="z-index-container">
          <div class="z-box z-low">z-index: 1</div>
          <div class="z-box z-medium">z-index: 10</div>
          <div class="z-box z-high">z-index: 100</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.demo-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  color: #2d3748;
  margin-bottom: 40px;
}

h2 {
  color: #4a5568;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 10px;
  margin: 40px 0 20px 0;
}

/* ===== 定位演示样式 ===== */
.positioning-demo {
  position: relative;
  height: 300px;
  background: #f7fafc;
  border: 2px dashed #cbd5e0;
  margin: 20px 0;
  padding: 20px;
}

.demo-box {
  width: 150px;
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  text-align: center;
  border-radius: 8px;
  font-size: 14px;
}

/* Static - 默认定位 */
.static-box {
  background: #667eea;
  /* position: static; (默认，可省略) */
}

/* Relative - 相对定位 */
.relative-box {
  background: #48bb78;
  position: relative;
  top: 20px;
  left: 20px;
  z-index: 2;
}

/* Absolute容器 */
.absolute-container {
  position: relative;
  width: 200px;
  height: 150px;
  background: #edf2f7;
  border: 2px solid #cbd5e0;
  margin-left: 200px;
  margin-top: -100px;
}

.absolute-container h4 {
  text-align: center;
  margin: 10px 0;
  color: #4a5568;
  font-size: 12px;
}

/* Absolute - 绝对定位 */
.absolute-box {
  background: #ed8936;
  position: absolute;
  bottom: 10px;
  right: 10px;
  z-index: 3;
}

/* Fixed - 固定定位 */
.fixed-box {
  background: #e53e3e;
  color: white;
  padding: 15px;
  border-radius: 8px;
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  font-weight: bold;
}

/* Sticky - 粘性定位 */
.sticky-header {
  background: #38b2ac;
  color: white;
  padding: 15px;
  text-align: center;
  font-weight: bold;
  position: sticky;
  top: 0;
  z-index: 100;
  margin-bottom: 20px;
}

.long-content {
  background: #f8f9fa;
  padding: 20px;
  line-height: 1.6;
}

.long-content p {
  margin: 10px 0;
  padding: 10px;
  background: white;
  border-radius: 4px;
  border-left: 4px solid #667eea;
}

/* Z-index 演示 */
.z-index-container {
  position: relative;
  height: 200px;
  background: #edf2f7;
  margin: 20px 0;
}

.z-box {
  position: absolute;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  border-radius: 8px;
  font-size: 14px;
}

.z-low {
  background: #f56565;
  top: 20px;
  left: 20px;
  z-index: 1;
}

.z-medium {
  background: #4299e1;
  top: 50px;
  left: 70px;
  z-index: 10;
}

.z-high {
  background: #9f7aea;
  top: 80px;
  left: 120px;
  z-index: 100;
}
</style>
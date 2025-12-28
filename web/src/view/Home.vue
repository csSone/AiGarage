<script setup lang="ts">
import ScopedDemo from '../components/ScopedDemo.vue'
</script>

<template>
  <div class="homepage">
    <!-- 1. 头部区域 - Hero Section -->
    <header class="hero">
      <div class="hero-content">
        <h1>AiGarage</h1>
        <p class="tagline">你的AI创意实践实验室</p>
        <p class="description">探索人工智能的无限可能，在这里构建、测试、分享你的AI项目</p>
        <button class="cta-button">开始探索</button>
      </div>
    </header>

    <!-- 2. 功能介绍区域 - Features Section -->
    <section class="features">
      <h2>核心功能</h2>
      <div class="feature-list">
        <div class="feature-item">
          <h3>AI模型实验</h3>
          <p>支持多种AI框架和模型，快速搭建实验环境</p>
        </div>
        <div class="feature-item">
          <h3>数据处理</h3>
          <p>强大的数据预处理和可视化工具</p>
        </div>
        <div class="feature-item">
          <h3>项目分享</h3>
          <p>轻松分享和协作你的AI项目成果</p>
        </div>
      </div>
    </section>

    <!-- 3. 项目展示区域 - Projects Section -->
    <section class="projects">
      <h2>精选项目</h2>
      <div class="project-grid">
        <div class="project-card">
          <h3>图像识别</h3>
          <p>基于深度学习的图像分类项目</p>
        </div>
        <div class="project-card">
          <h3>文本分析</h3>
          <p>自然语言处理和情感分析</p>
        </div>
        <div class="project-card">
          <h3>数据可视化</h3>
          <p>交互式数据分析和展示</p>
        </div>
      </div>
    </section>

    <!-- CSS样式演示区域 -->
    <section class="css-demo">
      <div class="container">
        <h2>CSS样式管理演示</h2>
        <p class="text-center">了解scoped与全局样式的区别</p>
        <ScopedDemo />
      </div>
    </section>

  </div>
</template>

<style scoped>
/* ===== 全局样式 ===== */
.homepage {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  color: #333;
  margin: 0;
  padding: 0;
}

/* ===== Hero 区域样式 ===== */
.hero {
  /* 背景颜色和渐变 */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

  /* 内边距 - 让内容有呼吸空间 */
  padding: 80px 20px;

  /* 文本颜色 */
  color: white;

  /* 文本居中 */
  text-align: center;

  /* 最小高度，确保有足够视觉冲击力 */
  min-height: 60vh;

  /* Flexbox布局 - 垂直居中内容 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  /* 最大宽度限制，避免在宽屏幕上文字过长 */
  max-width: 800px;
}

.hero h1 {
  /* 字体大小 */
  font-size: 3.5rem;

  /* 字体粗细 */
  font-weight: 700;

  /* 外边距 - 标题下方间距 */
  margin: 0 0 20px 0;

  /* 移除默认边距 */
  padding: 0;
}

.hero .tagline {
  /* 副标题样式 */
  font-size: 1.5rem;
  margin: 0 0 20px 0;
  opacity: 0.9; /* 稍微透明一点 */
}

.hero .description {
  /* 描述文字样式 */
  font-size: 1.1rem;
  margin: 0 0 30px 0;
  opacity: 0.8;
  line-height: 1.6;
}

.cta-button {
  /* 按钮样式 */
  background: #ff6b6b;
  color: white;
  border: none;
  padding: 15px 30px;
  font-size: 1.1rem;
  border-radius: 50px; /* 圆角按钮 */
  cursor: pointer; /* 鼠标悬停时显示手型 */
  transition: transform 0.2s ease; /* 平滑过渡效果 */
}

.cta-button:hover {
  transform: translateY(-2px); /* 悬停时向上移动一点 */
}

/* ===== Features 区域样式 ===== */
.features {
  padding: 80px 20px;
  background: #f8f9fa;
  text-align: center;
}

.features h2 {
  font-size: 2.5rem;
  margin-bottom: 50px;
  color: #2c3e50;
}

.feature-list {
  /* 使用Grid布局创建响应式网格 */
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px; /* 网格间距 */
  max-width: 1200px;
  margin: 0 auto;
}

.feature-item {
  background: white;
  padding: 40px 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  transition: transform 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px); /* 悬停时向上移动 */
}

.feature-item h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 15px;
}

.feature-item p {
  color: #7f8c8d;
  margin: 0;
}

/* ===== Projects 区域样式 ===== */
.projects {
  padding: 80px 20px;
  background: white;
  text-align: center;
}

.projects h2 {
  font-size: 2.5rem;
  margin-bottom: 50px;
  color: #2c3e50;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  max-width: 1000px;
  margin: 0 auto;
}

.project-card {
  background: #ffffff;
  border: 2px solid #e1e8ed;
  border-radius: 12px;
  padding: 30px 20px;
  transition: all 0.3s ease;
}

.project-card:hover {
  border-color: #667eea;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
}

.project-card h3 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 12px;
}

.project-card p {
  color: #7f8c8d;
  margin: 0;
  font-size: 0.95rem;
}

/* CSS演示区域 */
.css-demo {
  padding: 80px 20px;
  background: #f8f9fa;
}

.css-demo h2 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #2c3e50;
}

.css-demo p {
  font-size: 1.1rem;
  color: #6c757d;
  margin-bottom: 40px;
}
</style>

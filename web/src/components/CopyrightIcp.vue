<script setup lang="ts">
    const year = new Date().getFullYear()
    const author = "Simon Luo"
    const icpRecord = "粤ICP备2025482229号"
    const gonganIcon = new URL('@/assets/icons/gongan.png', import.meta.url).href
</script>

<template>

    <div class="icp">
        © {{ year }} {{ author }} |
        <img :src="gonganIcon" alt="公安备案图标" class="icp-icon" />
        <a href="http://beian.miit.gov.cn/" target="_blank">{{ icpRecord }}</a>
    </div>
</template>

<style scoped>
.icp {
    /* 移除 absolute 定位，让组件正常参与文档流 */
    width: 100%;
    text-align: center;
    color: #666;
    font-size: 14px;
    padding: 20px 0;
    background: #f8f9fa;
    border-top: 1px solid #e9ecef;
}

.icp-icon {
    width: 14px;
    height: 14px;
    vertical-align: middle;
    margin: 0 4px;
}

.icp a {
    color: #666;
    text-decoration: none;
    transition: color 0.2s ease;
}

.icp a:hover {
    color: #1890ff;
}
</style>

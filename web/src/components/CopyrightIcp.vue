<script setup lang="ts">
    const year = new Date().getFullYear()
    const author = "Simon Luo"
    const icpRecord = "粤ICP备2025482229号"
</script>

<template>
    <div class="icp">
        © {{ year }} {{ author }} |
        <img src="https://w-flac.org.cn/upload/gongan.png" alt="公安备案图标" class="icp-icon" />
        <a href="http://beian.miit.gov.cn/" target="_blank">{{ icpRecord }}</a>
    </div>
</template>

<style scoped>
.icp {
    position: absolute;
    bottom: 0;
    width: 100%;
    text-align: center;
    color: #666;
    font-size: 14px;
    padding: 12px 0;
    z-index: 1000;
}

.icp-icon {
    width: 14px;
    height: 14px;
    vertical-align: middle;
    margin: 0 2px;
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

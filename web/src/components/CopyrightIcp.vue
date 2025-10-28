<script setup lang="ts">
    const year:number = new Date().getFullYear() as number;
    const author:string = "Simon Luo";
    const icpRecord:string = "粤ICP备2025482229号";
</script>


<template>

<div class="icp">
        © {{ year }} {{ author }} - 
        <img src="https://w-flac.org.cn/upload/gongan.png" alt="公安备案图标" />
        <a href="http://beian.miit.gov.cn/" target="_blank">{{ icpRecord }}</a>
</div>

</template>

<style>
.icp {
    position: absolute;
    bottom: 0;
    width: 100%;
    text-align: center;
    color: gray;
    z-index: 1000;
}

.icp a {
    color: gray;
    text-decoration: none;
}

.icp a:hover {
    color: blue;
}
</style>

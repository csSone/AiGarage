import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/',  // Root path deployment
  server: {
    host: '0.0.0.0',
    port: 7016,
    strictPort: true,
    cors: true,  // For nginx proxy
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser',
  },
})

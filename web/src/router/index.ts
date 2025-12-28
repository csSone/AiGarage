import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../view/Home.vue')
    },
    {
      path: '/demo',
      name: 'Demo',
      component: () => import('../view/PositionDemo.vue')
    },
    {
      path: '/position',
      name: 'zPosition',
      component: () => import('../view/ZIndexDemo.vue')
    }
  ]
})

export default router
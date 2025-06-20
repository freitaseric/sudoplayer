import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import HomePage from './views/HomePage.vue'
import LoginPage from './views/LoginPage.vue'

const routes: RouteRecordRaw[] = [
  { name: 'Início', path: '/', component: HomePage },

  { path: '/login', component: LoginPage },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default routes

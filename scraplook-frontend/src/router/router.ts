import { createRouter, createWebHistory } from 'vue-router'
import ViewUsers from '../components/user/ViewUsers.vue'

const routes = [
  { path: '/users', name: 'Users', component: ViewUsers },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import ViewUsers from '../components/user/ViewUsers.vue'
import EmailDetails from '../components/mail/EmailDetails.vue'

const routes = [
  { path: '/users', name: 'Users', component: ViewUsers },
  {
    path: '/email/:emailId',
    name: 'EmailDetail',
    component: EmailDetails,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

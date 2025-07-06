import { createRouter, createWebHistory } from 'vue-router'
import ViewUsers from '../components/user/ViewUsers.vue'
import EmailDetails from '../components/mail/EmailDetails.vue'
import CreateUser from '../components/user/CreateUser.vue'
import CreateMail from '../components/mail/CreateMail.vue'
import SendMessage from '../components/message/SendMessage.vue'

const routes = [
  {
    path: '/users',
    name: 'Users',
    component: ViewUsers
  },
  {
    path: '/email/:emailId',
    name: 'EmailDetail',
    component: EmailDetails,
    props: true
  },
  {
    path: '/create/user',
    name: 'CreateUser',
    component: CreateUser
  },
  {
    path: '/create/mail:userId',
    name: 'CreateMail',
    component: CreateMail,
    props: true
  },
  {
    path: '/message/send/:id_address_mail',
    name: 'SendMessage',
    component: SendMessage,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

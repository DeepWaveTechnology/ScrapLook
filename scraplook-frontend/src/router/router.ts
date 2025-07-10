import { createRouter, createWebHistory } from 'vue-router'
import ViewUsers from '@/components/user/ViewUsers.vue'
import EmailDetails from '@/components/mail/EmailDetails.vue'
import CreateUser from '@/components/user/CreateUser.vue'
import CreateMail from '@/components/mail/CreateMail.vue'
import SendMessage from '@/components/message/SendMessage.vue'
import Home from '@/components/Home.vue'
import LoginPage from '@/components/LoginPage.vue'
import { useAuth } from '@/composables/useAuth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/users',
    name: 'Users',
    component: ViewUsers,
    beforeEnter: [loginGuard]
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    beforeEnter: [loginGuard]
  },
  {
    path: '/email/:emailId',
    name: 'EmailDetail',
    component: EmailDetails,
    props: true,
    beforeEnter: [loginGuard]
  },
  {
    path: '/create/user',
    name: 'CreateUser',
    component: CreateUser,
    beforeEnter: [loginGuard]
  },
  {
    path: '/create/mail:userId',
    name: 'CreateMail',
    component: CreateMail,
    props: true,
    beforeEnter: [loginGuard]
  },
  {
    path: '/message/send/:id_address_mail',
    name: 'SendMessage',
    component: SendMessage,
    props: true,
    beforeEnter: [loginGuard]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

function loginGuard(to: object): string|boolean{
  const { isLoggedIn } = useAuth();
  console.log(!!isLoggedIn.value, to); 

  //if destination is login page, check user is not already logged in
  if (to.fullPath === "/login"){

    //redirect user to users page if user is connected
    if (isLoggedIn.value){
      return '/users';
    }
    
    //user is not connected, accepts redirection
    return true;
  }

  return !!isLoggedIn.value;

}

export default router

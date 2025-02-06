import Vue from 'vue'
import Router from 'vue-router'

import LoginPage from '@/views/LoginPage.vue'
import MainPage from '@/views/MainPage.vue'

Vue.use(Router)

export default new Router({
  mode: 'history', 
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/main',
      name: 'mainPage',
      component: MainPage
    }
  ]
})
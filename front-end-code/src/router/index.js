import Vue from 'vue'
import Router from 'vue-router'

import MainPage from '@/views/MainPage.vue'
import Authentication from '@/views/Authentication.vue'
import Dashboard from '@/views/Dashboard.vue'

Vue.use(Router)

export default new Router({
  // Vue Router for linking views to paths
  mode: 'history', 
  routes: [
    {
      path: '/main',
      name: 'mainPage',
      component: MainPage
    },
    {
      path: '/authentication',
      name: 'authentication',
      component: Authentication
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard
    }
  ]
})
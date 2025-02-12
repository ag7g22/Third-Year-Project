import Vue from 'vue'
import Router from 'vue-router'

// Main Menu
import MainPage from '@/views/MainMenu/MainPage.vue'
import Authentication from '@/views/MainMenu/Authentication.vue'

// Quiz Pages
import Dashboard from '@/views/Dashboard.vue'

// Account Pages
import AccountPage from '@/views/Account/AccountPage.vue'
import AccountUpdate from '@/views/Account/AccountUpdate.vue'

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
    },
    {
      path: '/account',
      name: 'account',
      component: AccountPage
    },
    {
      path: '/update',
      name: 'update',
      component: AccountUpdate
    }

  ]
})
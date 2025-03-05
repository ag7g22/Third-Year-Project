import Vue from 'vue'
import Router from 'vue-router'

// Main Menu
import MainPage from '@/views/MainMenu/MainPage.vue'
import Authentication from '@/views/MainMenu/Authentication.vue'
import Dashboard from '@/views/Dashboard.vue'

// Account Pages
import AccountPage from '@/views/Account/AccountPage.vue'
import AccountUpdate from '@/views/Account/AccountUpdate.vue'

// Social-related pages
import FriendsList from '@/views/Social/FriendsList.vue'
import Leaderboard from '@/views/Social/Leaderboard.vue'
import Lobby from '@/views/Social/Lobby.vue'

// Quiz Pages
import CategoryQuiz from '@/views/Quiz/CategoryQuiz.vue'
import RoadSignQuiz from '@/views/Quiz/RoadSignQuiz.vue'
import Feedback from '@/views/Quiz/Feedback.vue'

// Hazard Perception
import HazardPerception from '@/views/Quiz/HazardPerception.vue'
import HPVideo from '@/views/Quiz/HPVideo.vue'

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
    },
    {
      path: '/friends',
      name: 'friends',
      component: FriendsList
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: Leaderboard
    },
    {
      path: '/lobby',
      name: 'lobby',
      component: Lobby
    },
    {
      path: '/categoryquiz',
      name: 'categoryquiz',
      component: CategoryQuiz
    },
    {
      path: '/roadsignquiz',
      name: 'roadsignquiz',
      component: RoadSignQuiz
    },
    {
      path: '/feedback',
      name: 'feedback',
      component: Feedback
    },
    {
      path: '/hazard',
      name: 'hazard',
      component: HazardPerception
    },
    {
      path: '/HPvideo',
      name: 'HPvideo',
      component: HPVideo
    }

  ]
})
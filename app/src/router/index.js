import Vue from 'vue'
import Router from 'vue-router'
import home from '@/views/home'
import ssInfo from '@/views/ss/ssInfo'
import ssList from '@/views/ss/ssList'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
    },
    {
      path: '/s',
      name: 'ss_list',
      component: ssList
    },
    {
      path: '/s/:ssKey',
      name: 'ss_info',
      component: ssInfo
    }
  ]
})

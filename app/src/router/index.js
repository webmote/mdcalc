import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home'
import ssInfo from '@/components/ss/ssInfo'
import ssList from '@/components/ss/ssList'
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
    { path: '/s/:ssKey', name: 'ss_info', component: ssInfo }
  ]
})

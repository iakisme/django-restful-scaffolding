import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import ClaimArea from '@/components/ClaimArea'
import LoginArea from '@/components/LoginArea'
import UpdateFileArea from '@/components/UpdateFileArea'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/claim-area',
      name: 'ClaimArea',
      component: ClaimArea
    },
    {
      path: '/login',
      name: 'LoginArea',
      component: LoginArea
    },
    {
      path: '/update-file-area',
      name: 'UpdateFileArea',
      component: UpdateFileArea
    }
  ]
})

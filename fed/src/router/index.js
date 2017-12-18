import Vue from 'vue'
import Router from 'vue-router'
const Main = () => import('@/components/Main')
const ClaimArea = () => import('@/components/ClaimArea')
const LoginArea = () => import('@/components/LoginArea')
const UpdateFileArea = () => import('@/components/UpdateFileArea')

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
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

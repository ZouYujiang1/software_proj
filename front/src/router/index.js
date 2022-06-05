import { createRouter, createWebHashHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'Home',
    // redirect: {name: 'Login'}
  },{
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },{
    path: '/charger/:id',
    name: 'Charger',
    component: () => import('../views/Charger.vue'),
    children: [
      {
        path: 'status',
        name: "Ch_status",
        component: () => import('../views/Ch_status')
      },{
        path: 'service',
        name: "Ch_service",
        component: () => import('../views/Ch_service')
      },
      {
        path: 'statistic',
        name: "Ch_statistic",
        component: () => import('../views/Ch_statistic')
      },

      {
        path: "",
        component: () => import('../views/Ch_status')
      }
    ]
  },{

  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

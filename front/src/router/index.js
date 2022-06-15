import { createRouter, createWebHashHistory } from 'vue-router'
import User from "@/views/User";
import Login from "@/views/Login";


const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: {name: 'Login'}
  },{
    path: '/test',
    name: 'Test',
    component: () => import('../views/Test')
  },{
    path: '/index',
    name: 'Index',
    component: () => import('../views/Index')
  },{
    path: '/login',
    name: 'Login',
    component: Login
  },{
    path: '/charger',
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
    path: '/user',
    name: 'User',
    component: User
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

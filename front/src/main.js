import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'
import "./axios"
import $ from 'jquery'

import Particles from 'particles.vue3'
const app=createApp(App)
app.config.globalProperties.$axios=axios
app.config.globalProperties.$=$
app.use(store)
    .use(router)
    .use(ElementPlus)


    .use(Particles)
    .mount('#app')

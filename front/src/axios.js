import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

import store from "./store"
import router from "./router"
import $ from 'jquery'

createApp(App).config.globalProperties.$=$

axios.defaults.baseURL='http://127.0.0.1:5000'
axios.interceptors.request.use(
    function (config) {
        // console.log("进入请求拦截器！")
        // 在发送请求之前做些什么
        return config;
    },
    function (error) {
        // 对请求错误做些什么
        //console.log("请求失败！")
        return Promise.reject(error);
    }),
axios.interceptors.response.use(
    function (response) {
        const res = response.status;
        //console.log("后置拦截")
        //console.log(res.code)
        // 当结果的code是否为200的情况

        if (res === 200) {

            return response
        } else {
            // 弹窗异常信息
            this.$message('这是一条消息提示');

            // 直接拒绝往下面返回结果信息


            return Promise.reject(response.data.msg)
        }


    },
    function (error)  {
        console.log('err' + error)// for debug
        if(error.response.data) {
            error.message = error.response.data.msg
        }
        // 根据请求状态觉得是否登录或者提示其他
        if (error.response.status === 401) {
            store.commit('REMOVE_INFO');
            router.push({
                path: '/index/login'
            })
            error.message = '请重新登录';
        }
        if (error.response.status === 403) {
            error.message = '权限不足，无法访问';
        }


        return Promise.reject(error)
    })

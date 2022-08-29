import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

require("./assets/main.scss")
axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.interceptors.response.use(undefined, function (error) {
    if (error) {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true;
                return router.push('/')
            }
        }
    })
createApp(App).use(store).use(router).mount('#app')

// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'
import ElementUI from 'element-ui' //element-ui的全部组件
import 'element-ui/lib/theme-chalk/index.css'//element-ui的css
const projectConfig = require('../static/config.json')
import axios from 'axios'
axios.defaults.withCredentials=true;
Vue.use(ElementUI) //使用elementUI
Vue.use(VueResource)
const axiosInstance = axios.create({
  withCredentials: true
})

Vue.prototype.$axios = axios
window.axios = axios
Vue.config.productionTip = false
// axios.default.withCredentials = true
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

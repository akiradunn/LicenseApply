import Vue from 'vue'
import Router from 'vue-router'
import LicenseLogin from "../components/LicenseLogin";
import ApplyForm from "../components/ApplyForm";
import LicenseDownload from "../components/LicenseDownload";

Vue.use(Router)

export default new Router({
  mode: 'history',
  baseUrl: '/app',
  routes: [
    {
      path: '/',
      name: 'LicenseLogin',
      component: LicenseLogin
    },
    {
      path:'/applyForm',
      name: 'ApplyForm',
      component:ApplyForm
    },
    {
      path:'/licenseDownload',
      name: 'LicenseDownload',
      component:LicenseDownload
    }
  ]
})

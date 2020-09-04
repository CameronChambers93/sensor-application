import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Chart from 'chart.js'
import Chartkick from 'vue-chartkick'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import PortalVue from 'portal-vue'
import MainContent from './components/MainContent.vue'
import Settings from './components/Settings.vue'

Vue.use(VueRouter)
Vue.use(Chartkick.use(Chart))
Vue.use(VueMaterial)
Vue.use(PortalVue)

const routes = [
  { path: '/', component: MainContent },
  { path: '/settings', component: Settings}
]

const router = new VueRouter({
  routes, // short for routes: routes
  mode: 'history'
})

Vue.config.productionTip = false

new Vue({
  //define the selector for the root component
    el: '#app',
    //pass the template to the root component
    template: '<App/>',
    //declare components that the root component can access
    components: { App },
    //pass in the router to the Vue instance
    router
  }).$mount('#app')//mount the router on the app
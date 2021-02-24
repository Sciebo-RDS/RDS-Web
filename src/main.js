import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import customMethods from "./plugins/customMethods"
import "@/translations"
import store from "./store"
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(customMethods)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')

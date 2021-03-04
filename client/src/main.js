import Vue from 'vue'
import config from "./config"
import integrations from "./plugins/integration"
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import customMethods from "./plugins/customMethods"
import "@/translations"
import storeInstall, { store } from "./store"
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)
Vue.use(config)
Vue.use(integrations)

Vue.prototype.auth.login()

Vue.use(customMethods)
Vue.use(storeInstall)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')

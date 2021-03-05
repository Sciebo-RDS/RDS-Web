import Vue from 'vue'
import config from "./config"
import store from "./store"
import integrations from "./plugins/integration"
import router from './router'
import vuetify from './plugins/vuetify';
import customMethods from "./plugins/customMethods"
import "@/translations"
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App.vue'
import Vuex from 'vuex';

Vue.use(Vuex)
Vue.use(config)
Vue.use(VueAxios, axios)
Vue.use(integrations)

Vue.prototype.auth.login()

Vue.use(customMethods)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')

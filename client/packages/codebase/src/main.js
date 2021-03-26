import config from "./config"
import store from "./store"
import integrations from "./plugins/integration"
import routes from './router'
import customMethods from "./plugins/customMethods"
import translations from "./translations/index.js"
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App.vue'
import Vuex from 'vuex';
import vuetify from './plugins/vuetify';

const vuet = vuetify.vuetify
function install(Vue) {
  Vue.use(Vuex)
  Vue.use(config)
  Vue.use(VueAxios, axios)
  Vue.use(vuetify)
  Vue.use(customMethods)
}

export default {
  install,
  App: App,
  routes: routes,
  store: store,
  translations: translations,
  integrations: integrations,
  vuetify: vuet
}

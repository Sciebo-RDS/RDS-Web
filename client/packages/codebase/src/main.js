import Vue from 'vue'
import config from "./config"
import store from "./store"
import integrations from "./plugins/integration"
import routes from './router'
import customMethods from "./plugins/customMethods"
import translations from "@/translations"
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App.vue'
import Vuex from 'vuex';

Vue.use(Vuex)
Vue.use(config)
Vue.use(VueAxios, axios)

Vue.use(customMethods)

export default {
  App,
  routes,
  store,
  translations,
  integrations,
  config,

}

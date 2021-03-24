import { App, config, integrations, translations, store, routes } from "codebase"

import Vue from 'vue'
import vuetify from './plugins/vuetify';
import axios from 'axios'
import VueAxios from 'vue-axios'
import Vuex from 'vuex';

Vue.use(Vuex)
Vue.use(config)
Vue.use(VueAxios, axios)
Vue.use(integrations)
Vue.use(translations)
Vue.use(store)

Vue.prototype.auth.login()

Vue.use(customMethods)
let router = routes.router
Vue.use(routes)

new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
}).$mount('#app')

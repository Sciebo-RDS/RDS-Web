import { App, routes, store, config, integrations, translations } from "codebase"

import Vue from 'vue'
import vuetify from './plugins/vuetify';
import Vuex from 'vuex';

Vue.use(Vuex)
Vue.use(config)
Vue.use(integrations.classic)
Vue.use(translations)
Vue.use(store)

Vue.prototype.auth.login()

let router = routes.router
Vue.use(routes)

new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
}).$mount('#app')

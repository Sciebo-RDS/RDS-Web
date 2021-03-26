import rds from "@rds/codebase"
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Vuex from 'vuex';

Vue.use(rds)
Vue.use(Vuex)
Vue.use(VueAxios, axios)
Vue.use(rds.integrations)
Vue.use(rds.translations)
Vue.use(rds.store)

const routes = rds.routes
const store = rds.store
const vuetify = rds.vuetify
const App = rds.App
Vue.use(routes)
const router = Vue.prototype.$routers

new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
}).$mount('#app')

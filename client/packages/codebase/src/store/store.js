import Vue from 'vue';
import Vuex from 'vuex';
import Settings from "./modules/Settings"
import RDS from "./modules/RDS"

Vue.use(Vuex)


const store = new Vuex.Store({
    modules: {
        RDSStore: RDS,
        SettingsStore: Settings
    },
    plugins: [],
    strict: process.env.NODE_ENV !== 'production'
})

export default store
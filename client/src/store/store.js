import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from "vuex-persistedstate";
import Settings from "./modules/Settings"
import RDS from "./modules/RDS"

Vue.use(Vuex)


const store = new Vuex.Store({
    modules: {
        RDSStore: RDS,
        SettingsStore: Settings
    },
    plugins: [createPersistedState()],
    strict: process.env.NODE_ENV !== 'production'
})

export default store
import Vue from 'vue';
import Vuex from 'vuex';
import Settings from "./modules/Settings"
import RDS from "./modules/RDS"
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

const store = new Vuex.Store({
    modules: {
        RDSStore: RDS,
        SettingsStore: Settings
    },
    plugins: [ /*createPersistedState()*/ ],
    strict: process.env.NODE_ENV !== 'production'
})

export default store
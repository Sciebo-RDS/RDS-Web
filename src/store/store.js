import Vue from 'vue';
import Vuex from 'vuex';
import VuexPersist from 'vuex-persist';

Vue.use(Vuex)

const vuexLocalStorage = new VuexPersist({
    key: 'vuex',
    storage: window.localStorage,
})

const store = new Vuex.Store({
    plugins: [vuexLocalStorage.plugin],
    strict: process.env.NODE_ENV !== 'production'
})


export default store 
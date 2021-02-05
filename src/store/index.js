import Vue from 'vue';
import Vuex from 'vuex';
import VuexPersist from 'vuex-persist';
import VueAxios from 'vue-axios';
import axios from 'axios';

Vue.use(Vuex)
Vue.use(VueAxios, axios);

const vuexLocalStorage = new VuexPersist({
    key: 'vuex',
    storage: window.localStorage,
})

const getDefaultState = () => {
    return {
        darkMode: false,
        deviceMode: false,
        language: "en",
        lastMessage: ""
    }
}

const store = new Vuex.Store({
    // You can use it as state property
    state: getDefaultState(),

    // You can use it as a state getter function (probably the best solution)
    getters: {
        getLastMessage(state) {
            return state.lastMessage
        },
        getLanguage(state) {
            return state.language;
        },
        isDarkMode(state) {
            if (state.deviceMode) {
                return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            }
            return state.darkMode == true
        },
        usingDeviceMode(state) {
            return state.deviceMode == true
        }
    },

    // Mutation for when you use it as state property
    mutations: {
        resetState(state) {
            // Merge rather than replace so we don't lose observers
            // https://github.com/vuejs/vuex/issues/1118
            Object.assign(state, getDefaultState())
        },
        setLastMessage(state, payload) {
            state.lastMessage = payload.message
        },
        setLanguage(state, payload) {
            state.language = payload.language
        },
        setDarkMode(state, payload) {
            state.darkMode = payload.darkMode
        },
        setDeviceMode(state, payload) {
            state.deviceMode = payload.deviceMode
        }
    },
    actions: {
        SOCKET_getMessage(context, state) {
            context.commit('setLastMessage', {
                message: state.message
            })
        },
        setLanguage(context, state) {
            context.commit('setLanguage', {
                language: state.language
            })
        },
        setDarkMode(context, state) {
            context.commit('setDarkMode', {
                darkMode: state.darkMode
            })
        },
        setDeviceMode(context, state) {
            context.commit('setDeviceMode', {
                deviceMode: state.deviceMode
            })
        }
    },
    plugins: [vuexLocalStorage.plugin]
});

export default store


const getDefaultState = () => {
    return {
        darkMode: false,
        deviceMode: false,
        language: "en",
    }
}


export default {
    getDefaultState,
    name: "SettingsStore",
    store: {
        // You can use it as state property
        state: getDefaultState(),

        // You can use it as a state getter function (probably the best solution)
        getters: {
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
    }
};
const language = () => {
    const ll_CC = navigator.language || navigator.userLanguage;
    return ll_CC.split("-", 1)[0];
}

const getDefaultState = () => {
    return {
        darkMode: false,
        deviceMode: true,
        language: language(),
        finishedWizard: false
    }
}

export default {
    getDefaultState,
    name: "SettingsStore",
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
        },
        isWizardFinished(state) {
            return state.finishedWizard
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
        },
        setWizardFinished(state) {
            state.finishedWizard = true
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
    }
};
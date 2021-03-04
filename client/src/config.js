const config = {
    productionTip: false,
    socket: {
        server: process.env.VUE_APP_SOCKETIO_HOST
    },
    server: process.env.VUE_APP_FRONTENDHOST,
    redirectUrl: process.env.VUE_APP_REDIRECTION_URL,
    skipRedirect: process.env.VUE_APP_SKIP_REDIRECTION === "True" //disables the redirection
}

export default {
    install(Vue) {
        for (const [key, value] of Object.entries(config)) {
            Vue.config[key] = value
        }
        Vue.prototype.$config = Vue.config
    }
}
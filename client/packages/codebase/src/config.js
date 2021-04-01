const config = {
    productionTip: false,
    socket: {
        server: process.env.VUE_APP_SOCKETIO_HOST || ""
    },
    server: process.env.VUE_APP_FRONTENDHOST || "",
    redirectUrl: process.env.VUE_APP_REDIRECTION_URL,
    skipRedirect: (process.env.VUE_APP_SKIP_REDIRECTION || "False") === "True" //disables the redirection
}

export default {
    config,
    install: function (Vue) {
        console.log(config.socket.server)
        for (const [key, value] of Object.entries(config)) {
            Vue.config[key] = value
        }
        Vue.prototype.$config = Vue.config
    }
}
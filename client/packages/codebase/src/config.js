const config = {
    productionTip: false,
    socket: {
        server: process.env.VUE_APP_SOCKETIO_HOST || ""
    },
    server: process.env.VUE_APP_FRONTENDHOST || "",
    describo: process.env.VUE_APP_DESCRIBO_URL || "http://localhost:8100"
}

export default {
    config,
    install: function(Vue) {
        console.log(config.socket.server)
        for (const [key, value] of Object.entries(config)) {
            Vue.config[key] = value
        }
        Vue.prototype.$config = Vue.config
    }
}
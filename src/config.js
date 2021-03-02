const config = {
    socket: {
        server: "http://localhost:8080"
    },
    productionTip: false
}

export default {
    install(Vue) {
        for(const [key, value] of Object.entries(config)) {
            Vue.config[key] = value
        }
        Vue.prototype.$config = Vue.config
    }
}
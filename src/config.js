const config = {
    socket: {
        server: process.env.SOCKETIO_HOST || "http://localhost:8080"
    },
    server: process.env.HOST || "http://localhost:8080",
    productionTip: false,
    redirectUrl: "https://10.14.29.60/owncloud/index.php/apps/oauth2/authorize?response_type=token&client_id=Pb0UGAlNBx0Hr35mhd5DSt0jBpg1YbApwn7Hf61nREiXinZT3ucVg9K1RSKuW4Di&redirect_uri=http://localhost:8080/",
    skipRedirect: true //disables the redirection
}

export default {
    install(Vue) {
        for (const [key, value] of Object.entries(config)) {
            Vue.config[key] = value
        }
        Vue.prototype.$config = Vue.config
    }
}
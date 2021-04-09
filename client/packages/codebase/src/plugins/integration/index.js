import standalone from "./standalone";
import embed from "./embed.js"

export default {
    install(Vue) {
        Vue.prototype.auth = {}
        Vue.prototype.auth.loginMethods = []
        Vue.prototype.auth.prelogin = []

        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('embed')) {
            Vue.use(embed)
        } else {
            Vue.use(standalone)
        }

        Vue.prototype.auth.loggedIn = false

        Vue.prototype.auth.login = function () {
            // First check, if we have already a session
            Vue.prototype.$http.get(`${Vue.config.server}/login`).then(() => {
                Vue.prototype.auth.loggedIn = true
                Vue.prototype.$socket.client.open()
            }).catch(() => {
                //if not, execute all loginMethods
                Vue.prototype.auth.loggedIn = false
                Promise.all(Vue.prototype.auth.loginMethods.map(fn => fn())).then((results) => {
                    if (results.includes(true)) {
                        Vue.prototype.auth.loggedIn = true
                        Vue.prototype.$socket.client.open()
                    } else {
                        if (!Vue.config.skipRedirect) {
                            if (Vue.config.redirectUrl === undefined) {
                                Vue.$http.get(`${Vue.config.server}/api/1.0/informations`).then((response) => {
                                    Vue.config.redirectUrl = response.redirectUrl
                                    Vue.prototype.$config.redirectUrl = Vue.config.redirectUrl
                                    window.location = Vue.config.redirectUrl
                                })
                            }
                        }
                    }
                })
            })
        }
    }
}
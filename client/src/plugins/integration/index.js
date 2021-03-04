import oc_classic from "./oc_classic";
import standalone from "./standalone";

export default {
    install(Vue) {
        Vue.prototype.auth = {}
        Vue.prototype.auth.loginMethods = []

        Vue.use(oc_classic)
        Vue.use(standalone)

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
                            window.location = Vue.config.redirectUrl
                        }
                    }
                })
            })
        }
    }
}
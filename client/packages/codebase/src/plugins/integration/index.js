import standalone from "./standalone";
import embed from "./embed.js"

export default {
    install(Vue) {
        Vue.prototype.auth = {}
        Vue.prototype.auth.loginMethods = []
        Vue.prototype.auth.prelogin = []
        Vue.prototype.auth.isLoading = true

        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('embed')) {
            Vue.use(embed)
        } else {
            Vue.use(standalone)
        }

        Vue.prototype.auth.loggedIn = false

        function loggedIn() {
            Vue.prototype.$socket.$subscribe('connect', () => {
                disableLoadingIndicator()
                Vue.prototype.$socket.$unsubscribe('connect');
            });
            Vue.prototype.auth.loggedIn = true
            Vue.prototype.$socket.client.open()
        }

        function disableLoadingIndicator() {
            Vue.prototype.auth.isLoading = false
        }

        Vue.prototype.auth.login = function () {
            // First check, if we have already a session
            Vue.prototype.$http.get(`${Vue.config.server}/login`).then(() => {
                loggedIn()
            }).catch(() => {
                //if not, execute all loginMethods
                Vue.prototype.auth.loggedIn = false
                Promise.all(Vue.prototype.auth.loginMethods).then((results) => {
                    if (results.includes(true)) {
                        loggedIn()
                    }
                })
            })
        }
    }
}
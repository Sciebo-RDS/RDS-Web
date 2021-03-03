export default {
    install(Vue) {
        Vue.prototype.auth.loginMethods.push(async function () {
            if (typeof OC !== "undefined") {
                try {
                    // eslint-disable-next-line
                    await Vue.prototype.$http.post(`${Vue.config.server}/login`, { token: OC.requesttoken })
                    return true
                } catch {
                    return false
                }
            }
            return false
        })
    }
}
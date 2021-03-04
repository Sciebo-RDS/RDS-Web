
export default {
    install(Vue) {
        Vue.prototype.auth.loginMethods.push(async function () {
            const urlParams = new URLSearchParams(window.location.search);
            const token = urlParams.get("access_token")
            const state = urlParams.get("state")

            if (token !== undefined) {
                try {
                    await Vue.prototype.$http.post(`${Vue.config.server}/login`, { token: token, state: state })
                    return true
                } catch {
                    return false
                }
            }
            return false
        })

    }
}
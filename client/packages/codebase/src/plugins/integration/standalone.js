export default {
    install(Vue) {
        Vue.prototype.auth.loginMethods.push(async function() {
            const urlParams = new URLSearchParams(window.location.search);
            const token = urlParams.get("access_token")
            const state = urlParams.get("state")

            if (token !== undefined) {
                try {
                    await Vue.prototype.$http.post(`${Vue.config.server}/login`, { access_token: token, state: state })
                    return true
                } catch {
                    return false
                }
            }
            return false
        })

        Vue.prototype.showFilePicker = function(projectId) {
            // TODO: Show the filePicker component in overlay or sth. Vue events maybe?
            // Can we find a solution, where this approach does not appear in embed version?
        }
    }
}
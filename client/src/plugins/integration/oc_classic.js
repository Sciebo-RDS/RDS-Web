export default {
    install(Vue) {
        if (typeof OC !== "undefined") {
            Vue.prototype.auth.loginMethods.push(async function () {
                try {
                    let prom1 = new Promise(function (resolve, reject) {
                        let timer = setInterval(function () {
                            clearInterval(timer)
                            reject(new Error('no value through response'))
                        }, 10000)

                        // eslint-disable-next-line no-undef
                        OC.AppConfig.getValue("rds", "cloudURL", function (response) {
                            clearInterval(timer)
                            resolve(response)
                        })
                    })

                    Vue.config.server = await prom1
                    Vue.config.socket.server = Vue.config.server

                    // eslint-disable-next-line no-undef
                    await Vue.prototype.$http.post(`${Vue.config.server}/login`, { token: OC.requesttoken })
                    return true
                } catch {
                    return false
                }
            })
        }
    }
}
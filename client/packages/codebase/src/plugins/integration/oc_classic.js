export default {
    install(Vue) {
        if (typeof OC !== "undefined") {
            Vue.prototype.auth.prelogin.push(async function () {
                try {
                    // eslint-disable-next-line no-undef
                    Vue.prototype.$http.defaults.headers.common['requesttoken'] = oc_requesttoken
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

                    return true
                } catch {
                    return false
                }
            })

            Vue.prototype.auth.loginMethods.push(async function () {
                try {
                    // eslint-disable-next-line no-undef
                    let info = (await Vue.prototype.$http.get(OC.generateUrl("/apps/rds/informations"))).data.jwt
                    await Vue.prototype.$http.post(`${Vue.config.server}/login`, { informations: info })
                    return true
                } catch {
                    return false
                }
            })
        }
    }
}
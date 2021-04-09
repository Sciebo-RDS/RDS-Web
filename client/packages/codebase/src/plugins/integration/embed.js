export default {
    install(Vue) {
        let parWindow = window.parent;
        const self = this;

        //Vue.prototype.auth.prelogin.push(async function () {})
        let prom1 = new Promise(function (resolve, reject) {
            let timer = setInterval(function () {
                clearInterval(timer)
                reject(new Error('no value through response'))
            }, 10000)

            window.addEventListener("message", (event) => {
                if (event.data.length > 0) {
                    var payload = JSON.parse(event.data);
                    switch (payload.event) {
                        case "informations":
                            let info = JSON.parse(payload.data).jwt
                            Vue.prototype.$http.post(`${Vue.config.server}/login`, { informations: info }).then(
                                (resp) => {
                                    clearInterval(timer)
                                    resolve(resp)
                                },
                                (resp) => {
                                    clearInterval(timer)
                                    reject(resp)
                                })
                            break;
                    }
                }
            });
        })

        Vue.prototype.auth.loginMethods.push(async function () {
            parWindow.postMessage(JSON.stringify({
                event: "init"
            }), "*")
        })

        Vue.prototype.showFilePicker = function (projectId, location) {
            parWindow.postMessage(JSON.stringify({
                event: "showFilePicker",
                data: {
                    projectId: projectId,
                    filePath: location
                }
            }), "*")
        }
    }
}
function getConfig() {
    // eslint-disable-next-line no-undef
    let prom1 = new Promise(function (resolve, reject) {
        let timer = setInterval(function () {
            clearInterval(timer)
            reject(new Error('no value through response'))
        }, 10000)

        // eslint-disable-next-line no-undef
        OC.AppConfig.getValue("rds", "cloudURL", function (response) {
            clearInterval(timer)
            resolve({ url: response, server: response })
        })
    })

    return prom1;
}

export default getConfig
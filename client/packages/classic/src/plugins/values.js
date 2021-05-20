function promise() {
    // eslint-disable-next-line no-undef
    let prom1 = new Promise(function (resolve, reject) {
        let timer = setInterval(function () {
            clearInterval(timer)
            reject(new Error('no value through response'))
        }, 10000)

        // eslint-disable-next-line no-undef
        const url = OC.generateUrl("/apps/rds/api/1.0/informations");
        fetch(url, {
            headers: new Headers({
                requesttoken: oc_requesttoken,
                "Content-Type": "application/json",
            })
        }).then((response) => {
            if (response.ok) {
                return response.text();
            }
            throw new Error(`${response.status} ${response.statusText}`);
        }).then((response) => {
            OC.rds.config = { url: response.cloudURL, server: response.cloudURL }
            resolve(OC.rds.config)
        }).catch((error) => {
            console.log("error in informations:", error)
            OC.rds.config = {
                url: "http://localhost:8080",
                server: "http://localhost:8080"
            };
            reject("cloudURL is empty")
        }).finally(() => {
            clearInterval(timer)
        })
    })

    return prom1;
}

function getConfig(context) {
    let prom = promise()
    prom.then((config) => {
        context.config = config;
    })
        .catch(() => {
            context.config = {
                url: "http://localhost:8080",
                server: "http://localhost:8080"
            };
        });
    return prom
}

export default getConfig
import store from '../store.js'
import RDS from "./RDS.js"
import VueSocketIO from 'vue-socket.io-extended';
import { io } from 'socket.io-client';

let modules = ["Settings"] // which modules in this folder should be added to store?

function addModule(moduleStore) {
    if (!store.hasModule(moduleStore.name)) {
        store.registerModule(moduleStore.name, moduleStore.store, { preserveState: !!Object.values(moduleStore.store.state)[0] })
    }
}

function insertModule(modName) {
    let resp = require(`@/store/services/${modName}.js`)
    addModule(resp.default)
}

export default {
    install: function (Vue) {
        const ioInstance = io(Vue.config.socket.server, {
            reconnection: true,
            reconnectionDelay: 3000,
            maxReconnectionAttempts: Infinity,
            transports: ["websocket"],
            autoConnect: false
        });

        Vue.use(VueSocketIO, ioInstance, {
            store,
            actionPrefix: 'SOCKET_',
            mutationPrefix: 'SOCKET_',
            eventToActionTransformer: (actionName) => actionName // cancel camel case
        })

        addModule(RDS)
        modules.forEach(element => {
            insertModule(element)
        });

        Vue.use(RDS)
    }
}

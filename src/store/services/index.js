import Vue from "vue"
import store from '../store.js'
import RDS from "./RDS.js"
import VueSocketIO from 'vue-socket.io-extended';
import { io } from 'socket.io-client';

let modules = ["Settings"] // which modules in this folder should be added to store?

const ioInstance = io('http://localhost:8080', {
    reconnection: true,
    reconnectionDelay: 3000,
    maxReconnectionAttempts: Infinity,
    transports: ["websocket"]
});

Vue.use(VueSocketIO, ioInstance, {
    store,
    actionPrefix: 'SOCKET_',
    mutationPrefix: 'SOCKET_',
    eventToActionTransformer: (actionName) => actionName // cancel camel case
})

function addModule(moduleStore) {
    if (!store.hasModule(moduleStore.name)) {
        store.registerModule(moduleStore.name, moduleStore.store, { preserveState: process.env.NODE_ENV === 'production' })
    }
}

function insertModule(modName) {
    let resp = require(`@/store/services/${modName}.js`)
    addModule(resp.default)
}

addModule(RDS)
modules.forEach(element => {
    insertModule(element)
});

Vue.use(RDS)
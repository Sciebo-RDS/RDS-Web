import Vue from "vue"
import store from '@/store'
import RDS from "./RDS.js"
import VueSocketIO from 'vue-socket.io-extended';
import { io } from 'socket.io-client';

const ioInstance = io('http://localhost:8080', {
    reconnection: true,
    reconnectionDelay: 2000,
    maxReconnectionAttempts: 10,
    reconnectionAttempts: 5,
});

Vue.use(VueSocketIO, ioInstance, {
    store,
    actionPrefix: 'SOCKET_',
    mutationPrefix: 'SOCKET_',
    eventToActionTransformer: (actionName) => actionName // cancel camel case
})
Vue.use(RDS)

let moduleName = "RDSStore"
if (!store.hasModule(moduleName)) {
    store.registerModule(moduleName, RDS.store, { preserveState: true })
}
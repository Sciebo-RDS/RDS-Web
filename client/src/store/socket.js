import VueSocketIO from 'vue-socket.io-extended';
import { io } from 'socket.io-client';
import { config } from "../config"
import store from "./store"

export default {
    install: function (Vue) {
        const ioInstance = io(config.socket.server, {
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

    }
}

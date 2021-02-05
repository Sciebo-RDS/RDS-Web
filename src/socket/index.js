import Vue from "vue"
import VueSocketIO from 'vue-socket.io'
import store from '@/store'

Vue.use(new VueSocketIO({
    debug: true,
    connection: 'http://localhost:8080',
    vuex: {
        store,
        actionPrefix: 'SOCKET_',
        mutationPrefix: 'SOCKET_'
    },
    options: { reconnectionAttempts: 5, reconnectionDelay: 2000 } //Optional options
}))
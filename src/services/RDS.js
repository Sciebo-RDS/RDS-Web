
const getDefaultState = () => {
    return {
        lastMessage: "",
        servicelist: [],
    }
}

export default {
    install: function (Vue) {
        let $socket = Vue.prototype.$socket
        Vue.prototype.$services = Vue.prototype.$services || {}
        Vue.prototype.$services.RDS = {
            requestServiceList() {
                $socket.client.emit("requestServiceList");
            },
            sendService(service) {
                $socket.client.emit("addService", { service: service });
            },
            sendMessage(message) {
                $socket.client.emit("sendMessage", { message: message });
            }
        }
    },
    store: {
        state: getDefaultState(),
        getters: {
            getLastMessage(state) {
                return state.lastMessage
            },
            getServiceList(state) {
                return state.servicelist
            }
        },
        mutations: {
            setLastMessage(state, payload) {
                state.lastMessage = payload.message
            },
            setServiceList(state, payload) {
                state.servicelist = payload.servicelist
            },
        },
        actions: {
            SOCKET_getMessage(context, state) {
                context.commit('setLastMessage', {
                    message: state.message
                })
            },
            SOCKET_ServiceList(context, state) {
                context.commit('setServiceList', {
                    servicelist: state.list
                })
            },
        },
    }
}
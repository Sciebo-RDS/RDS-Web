import store from "../store.js"

const getDefaultState = () => {
    return {
        lastMessage: "",
        userservicelist: [],
        servicelist: [],
    }
}

export default {
    getDefaultState,
    install: function (Vue) {
        let $socket = Vue.prototype.$socket
        Vue.prototype.$services = Vue.prototype.$services || {}
        Vue.prototype.$services.RDS = {
            requestUserServiceList() {
                $socket.client.emit("getUserServices", (response) => {
                    let serviceList = []
                    let list = JSON.parse(response).list

                    list.forEach(element => {
                        serviceList.push(element.informations)
                    });

                    store.dispatch("SOCKET_UserServiceList", { list: serviceList })
                });
            },
            requestServiceList() {
                $socket.client.emit("getServicesList", (response) => {
                    // make it here the same secure like in php classic version
                    let serviceList = []
                    let list = JSON.parse(response)

                    list.forEach(element => {
                        serviceList.push(element.informations)
                    });

                    store.dispatch("SOCKET_ServiceList", { list: serviceList })
                });
            },
            addService(service) {
                $socket.client.emit("addService", { service: service });
            },
            removeService(service) {
                $socket.client.emit("removeService", { service: service });
            },
            sendMessage(message) {
                $socket.client.emit("sendMessage", { message: message });
            }
        }
    },
    name: "RDSStore",
    store: {
        state: getDefaultState(),
        getters: {
            getLastMessage(state) {
                return state.lastMessage
            },
            getUserServiceList(state) {
                return state.userservicelist
            },
            getServiceList(state) {
                return state.servicelist
            }
        },
        mutations: {
            setLastMessage(state, payload) {
                state.lastMessage = payload.message
            },
            setUserServiceList(state, payload) {
                state.userservicelist = payload.servicelist
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
            SOCKET_UserServiceList(context, state) {
                context.commit('setUserServiceList', {
                    servicelist: state.list
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
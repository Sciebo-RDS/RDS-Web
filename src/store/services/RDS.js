import store from "../store.js"

const getDefaultState = () => {
    return {
        lastMessage: "",
        userservicelist: [],
        servicelist: [],
        researchlist: []
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
                    store.dispatch("SOCKET_UserServiceList", { list: JSON.parse(response).list.map(el => el.informations) })
                });
            },
            requestServiceList() {
                $socket.client.emit("getServicesList", (response) => {
                    store.dispatch("SOCKET_ServiceList", { list: JSON.parse(response).map(el => el.informations) })
                });
            },
            requestResearchList() {
                $socket.client.emit("getAllResearch", (response) => {
                    store.dispatch("SOCKET_ResearchList", { list: JSON.parse(response) })
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
            },
            getResearchList(state) {
                return state.researchlist
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
            setResearchList(state, payload) {
                state.researchlist = payload.researchlist
            }
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
            SOCKET_ResearchList(context, state) {
                context.commit('setResearchList', {
                    researchlist: state.list
                })
            }
        },
    }
}
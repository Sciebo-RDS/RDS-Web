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
        Vue.prototype.$requests = Vue.prototype.$requests || {}
        Vue.prototype.$requests.RDS = {
            requestUserServiceList() {
                $socket.client.emit("getUserServices", (response) => {
                    store.dispatch("SOCKET_UserServiceList", { list: response })
                });
            },
            requestServiceList() {
                $socket.client.emit("getServicesList", (response) => {
                    store.dispatch("SOCKET_ServiceList", { list: response })
                });
            },
            requestResearchList() {
                $socket.client.emit("getAllResearch", (response) => {
                    store.dispatch("SOCKET_ResearchList", { list: JSON.parse(response) })
                });
            },
            exchangeCode(data) {
                if (!!data.code && !!data.state) {
                    $socket.client.emit("exchangeCode", JSON.stringify(data), (response) => {
                        console.log("exchangeCode response", response)
                    });
                }
            },
            addServiceWithCredentials(service) {
                $socket.client.emit("addCredentials", JSON.stringify(service), (response) => {
                    console.log("credentials response", response)
                });
            },
            removeService(service) {
                $socket.client.emit("removeServiceForUser", JSON.stringify(service));
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
                    servicelist: JSON.parse(state).list.map(el => el.informations)
                })
            },
            SOCKET_ServiceList(context, state) {
                context.commit('setServiceList', {
                    servicelist: JSON.parse(state).map(el => {
                        el.informations.state = el.jwt
                        return el.informations
                    })
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
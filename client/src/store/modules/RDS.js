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
    name: "RDSStore",
    state: getDefaultState(),
    getters: {
        getUserServiceList: (state) => state.userservicelist,
        getServiceList: (state) => state.servicelist,
        getResearchList: (state) => state.researchlist
    },
    mutations: {
        setUserServiceList: (state, payload) => { state.userservicelist = payload.servicelist },
        setServiceList: (state, payload) => { state.servicelist = payload.servicelist },
        setResearchList: (state, payload) => { state.researchlist = payload.researchlist }
    },
    actions: {
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
        },
        requestUserServiceList(context) {
            this._vm.$socket.client.emit("getUserServices", (response) => {
                context.dispatch("SOCKET_UserServiceList", { list: response })
            });
        },
        requestServiceList(context) {
            this._vm.$socket.client.emit("getServicesList", (response) => {
                context.dispatch("SOCKET_ServiceList", { list: response })
            });
        },
        requestResearchList(context) {
            this._vm.$socket.client.emit("getAllResearch", (response) => {
                context.dispatch("SOCKET_ResearchList", { list: JSON.parse(response) })
            });
        },
        exchangeCode(context, data) {
            if (!!data.code && !!data.state) {
                this._vm.$socket.client.emit("exchangeCode", JSON.stringify(data), (response) => {
                    console.log("exchangeCode response", response)
                });
            }
        },
        addServiceWithCredentials(context, service) {
            this._vm.$socket.client.emit("addCredentials", JSON.stringify(service), (response) => {
                console.log("credentials response", response)
            });
        },
        removeService(context, service) {
            this._vm.$socket.client.emit("removeServiceForUser", JSON.stringify(service));
        },
    },

}
const getDefaultState = () => {
    return {
        userservicelist: [],
        servicelist: [],
        projectlist: []
    }
}

export default {
    getDefaultState,
    name: "RDSStore",
    state: getDefaultState(),
    getters: {
        getUserServiceList: (state) => state.userservicelist,
        getServiceList: (state) => state.servicelist,
        getProjectlist: (state) => state.projectlist
    },
    mutations: {
        setUserServiceList: (state, payload) => { state.userservicelist = payload.servicelist },
        setServiceList: (state, payload) => { state.servicelist = payload.servicelist },
        setProjectList: (state, payload) => { state.projectlist = payload.projectlist }
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
        SOCKET_ProjectList(context, state) {
            context.commit('setProjectList', {
                projectlist: JSON.parse(state)
            })
        },
        setLocation(context, data) {
            // TODO get and remove port-owncloud first and add it with new location!
            const location = data.filePath
            const projectId = data.projectId
            this._vm.$socket.client.emit("setLocation", data);
        },
        createProject() {
            this._vm.$socket.client.emit("createResearch");
        },
        saveProject(context, data) {
            data.researchId = data.id
            this._vm.$socket.client.emit("saveResearch", data);
        },
        removeProject(context, data) {
            data.researchId = data.id
            this._vm.$socket.client.emit("removeResearch", data);
        },
        addPortOut(context, data) {
            data.researchId = data.id
            this._vm.$socket.client.emit("addExport", data)
        },
        removePortOut(context, data) {
            data.researchId = data.id
            this._vm.$socket.client.emit("removeExport", data)
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
        requestProjectList(context) {
            this._vm.$socket.client.emit("getAllResearch", (response) => {
                context.dispatch("SOCKET_ProjectList", { list: JSON.parse(response) })
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
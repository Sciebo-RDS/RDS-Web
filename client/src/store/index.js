import store from "./store.js";
import services from "./services"

export default {
    install(Vue) {
        Vue.use(services)
    }
}

export { store }
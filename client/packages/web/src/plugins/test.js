export default {
    install(Vue) {
        Vue.prototype.showMe = function () {
            console.log("Yeah, it works!!!")
        }
    }
}
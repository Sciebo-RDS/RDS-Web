
export default {
    install: function (Vue) {
        Vue.prototype.parseServicename = function (value) {
            if (typeof value !== "string") return "";
            value = value.replace("port-", "");
            return value.charAt(0).toUpperCase() + value.slice(1);
        }

        Vue.prototype.containsService = function (arr, service) {
            for (const el of arr) {
                if (el.servicename === service.servicename) return true;
            }
            return false
        }

        Vue.prototype.equalServices = function (arr, array) {
            // if the other array is a falsy value or
            // compare lengths - can save a lot of time
            if (!array || arr.length != array.length) return false;

            for (const el of arr) {
                if (!this.containsService(array, el)) return false;
            }

            return true;
        }
    }
}
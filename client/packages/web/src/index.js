import App from "./App.vue"
import test from "./plugins/test"

function $gettext(msg) {
    return msg
}

Vue.use(test)

const appInfo = {
    name: "Hello World",
    id: "hello-world",
    icon: "folder"
}

const routes = [//right top action icon
    {
        path: "",
        name: "Hello",
        components: {
            //fullscreen: App,
            app: App
        }
    }
]

const navItems = [//left sidebar
    {
        name: "Hello",
        iconMaterial: "folder", //next to link
        route: {
            name: "Hello",
            path: appInfo.id
        }
    }
]

export default {
    appInfo,
    routes,
    navItems
}
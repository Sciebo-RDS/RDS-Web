
import App from "../../../client/src/App.vue"

function $gettext(msg) {
    return msg
}

const appInfo = {
    name: "Hello World",
    id: "hello-world",
    icon: "folder"
}

const routes = [
    {
        path: "",
        name: "Hello",
        components: {
            fullscreen: App,
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
import App from "./App.vue"
import test from "./plugins/test"

function $gettext(msg) {
    return msg
}

Vue.use(test)

const appInfo = {
    name: "RDS",
    id: "rds",
    icon: "search",
    extensions: [
        {
            extension: '',
            routeName: 'rds-new-project',
            newFileMenu: {
                menuTitle($gettext) {
                    return $gettext('Create RDS project...')
                }
            },
            routes: [
                'files-personal',
                'files-favorites',
                'files-shared-with-others',
                'files-shared-with-me',
                'files-public-list'
            ]
        },
    ]
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
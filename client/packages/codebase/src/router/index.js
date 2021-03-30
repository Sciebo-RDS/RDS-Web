import VueRouter from 'vue-router'
import Home from "../views/Home.vue"
import Projects from "../views/Projects.vue"
import Settings from "../views/Settings.vue"
import Wizard from "../views/Wizard.vue"

let routes = [
  {
    path: '/',
    name: "Home",
    component: Home,
    icon: "mdi-home"
  },
  {
    path: '/projects',
    name: "Projects",
    component: Projects,
    icon: "mdi-lightbulb-on"
  },
  {
    path: '/settings',
    name: "Settings",
    component: Settings,
    icon: "mdi-cog"
  },
  {
    path: '/wizard',
    name: "Wizard",
    component: Wizard,
    icon: "mdi-wizard-hat",
    hide: true
  },
]

export default {
  install(Vue) {
    Vue.use(VueRouter)

    const titles = {
      "Home": Vue.prototype.$gettext("Home"),
      "Projects": Vue.prototype.$gettext('Projects'),
      "Settings": Vue.prototype.$gettext('Settings'),
      "Wizard": Vue.prototype.$gettext('Wizard')
    }

    for (let index = 0; index < routes.length; index++) {
      const route = routes[index];
      route.title = titles[route.name];
    }

    const router = new VueRouter({
      routes
    })

    Vue.prototype.$routers = router
  },
  routes
}

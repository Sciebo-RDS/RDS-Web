import VueRouter from 'vue-router'
import Home from "@/views/Home.vue"
import Projects from "@/views/Projects.vue"
import Settings from "@/views/Settings.vue"
import Wizard from "@/views/Wizard.vue"


export default {
  install(Vue) {
    Vue.use(VueRouter)

    const routes = [
      {
        path: '/',
        name: "Home",
        title: Vue.prototype.$gettext("Home"),
        component: Home,
        icon: "mdi-home"
      },
      {
        path: '/projects',
        name: "Projects",
        title: Vue.prototype.$gettext('Projects'),
        component: Projects,
        icon: "mdi-lightbulb-on"
      },
      {
        path: '/settings',
        name: "Settings",
        title: Vue.prototype.$gettext('Settings'),
        component: Settings,
        icon: "mdi-cog"
      },
      {
        path: '/wizard',
        name: "Wizard",
        title: Vue.prototype.$gettext('Wizard'),
        component: Wizard,
        icon: "mdi-wizard-hat",
        hide: true
      },
    ]

    const router = new VueRouter({
      routes
    })

    Vue.prototype.$routers = router
  }
}

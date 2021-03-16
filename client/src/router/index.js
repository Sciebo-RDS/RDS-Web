import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

function load(component) {
  return () => import(/* webpackChunkName: "[request]" */ `@/views/${component}.vue`)
}

export default {
  install(Vue) {
    const routes = [
      {
        path: '/',
        name: "Home",
        title: Vue.prototype.$gettext("Home"),
        component: load("Home"),
        icon: "mdi-home"
      },
      {
        path: '/projects',
        name: "Projects",
        title: Vue.prototype.$gettext('Projects'),
        component: load("Projects"),
        icon: "mdi-lightbulb-on"
      },
      {
        path: '/settings',
        name: "Settings",
        title: Vue.prototype.$gettext('Settings'),
        component: load("Settings"),
        icon: "mdi-cog"
      },
      {
        path: '/wizard',
        name: "Wizard",
        title: Vue.prototype.$gettext('Wizard'),
        component: load("Wizard"),
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

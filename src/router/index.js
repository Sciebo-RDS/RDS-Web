import Vue from 'vue'
import VueRouter from 'vue-router'
import "@/translations"

Vue.use(VueRouter)

let vm = new Vue()

function load(component) {
  return () => import(/* webpackChunkName: "[request]" */ `@/views/${component}.vue`)
}

const routes = [
  {
    path: '/',
    name : "Home",
    title: vm.$gettext("Home"),
    component: load("Home"),
    icon: "mdi-home"
  },
  {
    path: '/projects',
    name : "Projects",
    title: vm.$gettext('Projects'),
    component: load("Projects"),
    icon: "mdi-lightbulb-on"
  },
  {
    path: '/settings',
    name : "Settings",
    title: vm.$gettext('Settings'),
    component: load("Settings"),
    icon: "mdi-cog"
  },
  {
    path: '/wizard',
    name : "Wizard",
    title: vm.$gettext('Wizard'),
    component: load("Wizard"),
    icon: "mdi- wizard-hat",
    hide: true
  },
]

const router = new VueRouter({
  routes
})

export default router

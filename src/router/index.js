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
    name: vm.$gettext("Home"),
    component: load("Home"),
    icon: "mdi-home"
  },
  {
    path: '/projects',
    name: vm.$gettext('Projects'),
    component: load("Projects"),
    icon: "mdi-lightbulb-on"
  },
  {
    path: '/settings',
    name: vm.$gettext('Settings'),
    component: load("Settings"),
    icon: "mdi-cog"
  },
]

const router = new VueRouter({
  routes
})

export default router

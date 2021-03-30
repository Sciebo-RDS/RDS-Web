<template>
  <div>
    <v-app id="inspire">
      <!--<v-system-bar app class="d-xl-none">
      <v-spacer></v-spacer>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    </v-system-bar>-->

    <v-app-bar app flat>
      <v-app-bar-nav-icon @click="drawer = !drawer" class="d-lg-none"></v-app-bar-nav-icon>
      <v-toolbar-title></v-toolbar-title>
    </v-app-bar>

      <v-navigation-drawer v-model="drawer" app bottom>
        <v-sheet class="flex-direction row pa-4">
          <v-container fill-height
            ><v-row no-gutters align="center" justify="center">
              <v-col
                ><v-avatar class="mb-4" color="green darken-3" size="64">
                  <v-img src="@/assets/sciebo.png" /></v-avatar
              ></v-col>
              <v-col fill-height="true"><h3>Sciebo RDS</h3></v-col></v-row
            >
          </v-container>
        </v-sheet>

        <v-divider></v-divider>

        <v-list>
          <v-list-item-group v-model="model" mandatory color="indigo">
            <v-list-item v-for="(item, i) in views" :key="i" :to="item.path">
              <v-list-item-icon>
                <v-icon v-text="item.icon" />
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title
                  v-text="$gettext(item.name)"
                ></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>

      <v-main>
        <v-container fluid> <router-view /> </v-container>
      </v-main>

    </v-app>
  </div>
</template>


<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>

<script>
import router from "./router/index.js";
import { mapGetters } from "vuex";
import Vue from "vue";

export default {
  sockets: {
    connect: function () {
      console.log("socket connected");
    },
    disconnect() {
      this.isConnected = false;
      console.log("server disconnected");
    },
  },
  data: () => ({
    drawer: null,
    views: router.options.routes,
    model: null,
  }),
  components: {},
  methods: {},
  computed: {
    ...mapGetters({
      isDarkMode: "isDarkMode",
      getLanguage: "getLanguage",
    }),
  },
  beforeMount: function () {
    let language = this.getLanguage;

    if (language == undefined) {
      const ll_CC = navigator.language || navigator.userLanguage;
      language = ll_CC.split("-", 1)[0];
    }

    if (!Object.prototype.hasOwnProperty.call(Vue.$translations, language)) {
      import("@/translations/" + language + ".json").then((locale) => {
        this.$language.merge(locale);
        this.$language.current = language;
      });
    } else {
      this.$language.current = language;
    }

    this.$vuetify.theme.dark = this.$store.getters.isDarkMode;
  },
};
</script>
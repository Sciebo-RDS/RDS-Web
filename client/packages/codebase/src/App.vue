<template>
  <div>
    <v-app id="inspire">
      <overlay :subtext="overlayText" />

      <v-app-bar app flat class="d-lg-none">
        <v-app-bar-nav-icon
          @click="drawer = !drawer"
          class="d-lg-none"
        ></v-app-bar-nav-icon>
        <v-toolbar-title></v-toolbar-title>
      </v-app-bar>

      <v-navigation-drawer id="v-navigation-drawer" v-model="drawer" app bottom>
        <v-sheet class="flex-direction row pa-4">
          <v-container>
            <v-row no-gutters align="center">
              <v-col>
                <v-avatar class="mb-4" color="green darken-3" size="64">
                  <v-img src="@/assets/sciebo.png" />
                </v-avatar>
              </v-col>
              <v-col>
                <div
                  :class="[
                    'text-h6',
                    auth.loggedIn ? 'primary--text' : 'error--text',
                  ]"
                  v-text="'Sciebo RDS'"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-sheet>

        <v-divider></v-divider>

        <v-list>
          <v-list-item-group v-model="model" mandatory color="indigo">
            <v-list-item
              v-for="(item, i) in views"
              :key="i"
              :to="item.path"
              v-show="
                !$store.getters.isWizardFinished != !item.hide ||
                item.name == 'Home'
              "
            >
              <v-list-item-icon>
                <v-icon v-text="item.icon" />
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title
                  v-text="$gettext(item.title)"
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


<style lang="scss" scoped>
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
import { mapGetters } from "vuex";
import overlay from "./components/Overlay.vue";

export default {
  name: "App",
  props: {
    server: { type: String, default: null },
  },
  sockets: {
    connect: function () {
      console.log("socket connected");
    },
    disconnect() {
      this.isConnected = false;
      console.log("server disconnected");
    },
  },
  data() {
    return {
      drawer: null,
      views: this.$router.options.routes,
      model: null,
      overlayText: null,
    };
  },
  components: { overlay },
  methods: {},
  computed: {
    ...mapGetters({
      isDarkMode: "isDarkMode",
      getLanguage: "getLanguage",
    }),
  },
  beforeCreate() {
    if (!this.$store.getters.isWizardFinished) {
      this.$router.push({ name: "Wizard" });
    }
  },
  beforeMount: function () {
    this.$config.language = this.getLanguage;

    this.$vuetify.theme.dark = this.$store.getters.isDarkMode;
  },
  mounted() {
    this.overlayText = this.$gettext("Wait for login");

    var checkLoginStatus = setInterval(() => {
      this.$emit("showoverlay");
      if (this.auth.loggedIn) {
        clearInterval(checkLoginStatus);
        this.overlayText = null;
        this.$emit("hideoverlay");
      }
    }, 500);
  },
};
</script>
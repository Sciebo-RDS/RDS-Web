<template>
  <v-list>
    <v-list-item-group style="position: absolute; bottom:0px; width:100%">
      <v-menu top offset-y :close-on-click="false" dark max-width="280px">
        <template v-slot:activator="{ on, attrs }">
          <v-list-item v-bind="attrs" v-on="on">
            <v-list-item-icon>
              <v-icon>mdi-cog</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="$gettext('Settings')" />
            </v-list-item-content>
          </v-list-item>
        </template>

        <v-card>
          <v-container fluid>
            <v-subheader>{{ $gettext("Mode") }}</v-subheader>
            <v-btn
              v-for="item in modes"
              :key="item.text"
              @click="item.click"
              class="ma-1"
              style="width:120px"
              :color="item.active() ? 'primary' : ''"
            >
              {{ item.text }} <v-icon right>{{ item.icon }}</v-icon>
            </v-btn>
            <div v-if="!languagePredefined">
              <v-subheader>{{ $gettext("Language") }}</v-subheader>
              <v-btn
                v-for="item in availableLanguages"
                :key="item.text"
                class="ma-1"
                style="width:120px"
              >
                {{ item.long }}
              </v-btn>
            </div>
          </v-container>
        </v-card>
      </v-menu>
    </v-list-item-group>
  </v-list>
</template>

<script>
export default {
  data() {
    return {
      modes: [
        {
          text: "Light",
          icon: "mdi-white-balance-sunny",
          click: () => {
            this.deviceMode = false;
            this.darkMode = false;
            this.timeMode = false;
          },
          active: () => {
            return !this.darkMode && !this.deviceMode && !this.timeMode;
          },
        },
        {
          text: "Dark",
          icon: "mdi-weather-night",
          click: () => {
            this.deviceMode = false;
            this.darkMode = true;
            this.timeMode = false;
          },
          active: () => {
            return this.darkMode && !this.deviceMode && !this.timeMode;
          },
        },
        {
          text: "System",
          icon: "mdi-desktop-classic",
          click: () => {
            this.deviceMode = true;
            this.timeMode = false;
          },
          active: () => {
            return this.deviceMode;
          },
        },
        {
          text: "Mixed",
          icon: "mdi-theme-light-dark",
          click: () => {
            this.deviceMode = false;
            this.timeMode = true;
            this.startTimeMode();
          },
          active: () => {
            return this.timeMode;
          },
        },
      ],
      language: [],
    };
  },
  computed: {
    availableLanguages: function() {
      let res = [];
      for (const [key, value] of Object.entries(this.$language.available)) {
        res.push({ short: key, long: value });
      }

      return res;
    },
    languagePredefined() {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.has("lang");
    },
    darkMode: {
      get() {
        return this.$store.getters.usingDarkMode;
      },
      set(value) {
        this.$vuetify.theme.dark = value;
        this.$store.dispatch("setDarkMode", { darkMode: value });
      },
    },
    deviceMode: {
      get() {
        return this.$store.getters.usingDeviceMode;
      },
      set(value) {
        this.$store.dispatch("setDeviceMode", { deviceMode: value });
      },
    },
    timeMode: {
      get() {
        return this.$store.getters.usingTimeMode;
      },
      set(value) {
        this.$store.dispatch("setTimeMode", { timeMode: value });
      },
    },
  },
  watch: {
    darkMode(newVal) {
      this.$vuetify.theme.dark = newVal;
    },
  },
  methods: {
    loopTimeMode() {
      console.log("exec timemode: ", this.timeMode);
      const today = new Date();
      console.log("darkMode: ", today.getHours() < 8 || today.getHours() > 20);
      this.darkMode = today.getHours() < 8 || today.getHours() > 20;
    },
    startTimeMode() {
      console.log("start timemode");
      if (this.timeMode) {
        this.loopTimeMode();
        let timer = setInterval(() => {
          if (this.timeMode) {
            this.loopTimeMode();
          } else {
            clearInterval(timer);
          }
        }, 1000 * 60 * 5);
      }
    },
  },
  beforeMount() {
    this.startTimeMode();
  },
};
</script>

<style></style>

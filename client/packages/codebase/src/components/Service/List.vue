<template>
  <v-row justify="center">
    <v-expansion-panels inset focusable multiple>
      <v-expansion-panel v-for="(service, i) in services" :key="i">
        <v-expansion-panel-header>
          <v-row>
            <v-col cols="auto"> {{ service.name }}</v-col>
            <v-chip
              v-if="service.state"
              color="light-green lighten-1"
              class="ma-2"
              small
              >connected <v-icon class="ml-2">mdi-link</v-icon>
            </v-chip>
            <v-chip v-else color="grey" class="ma-2" small
              >not connected <v-icon class="ml-2">mdi-link-off</v-icon>
            </v-chip>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ServiceConfiguration :service="service" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-row>
</template>

<script>
import ServiceConfiguration from "./Configuration.vue";

export default {
  components: {
    ServiceConfiguration,
  },
  data() {
    return {
      services: [
        {
          name: "zenodo",
          state: 0,
          description: {
            de:
              "ZENODO AUF DEUTSCH\n Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
            en: "ZENODO AUF ENGLISCH",
          },
          infoUrl: "https://zenodo.org/",
          icon: "",
          helpUrl: "",
          displayName: "",
        },
        {
          name: "datasafe",
          state: 1,
          description: {
            de: "DATASAFE AUF DEUTSCH",
            en: "DATASAFE AUF ENGLISCH",
          },
          infoUrl: "https://datasafe.uni-muenster.de/",
          icon: "",
          helpUrl: "https://datasafe.uni-muenster.de/",
          displayName: "",
        },
        {
          name: "owncloud",
          state: 0,
          description: {
            de: "OWNCLOUD AUF DEUTSCH",
            en: "OWNCLOUD AUF ENGLISCH",
          },
          infoUrl: "https://owncloud.com/de/",
          icon: "",
          helpUrl: "",
          displayName: "",
        },
        {
          name: "reva",
          state: 1,
          description: { de: "REVA AUF DEUTSCH", en: "REVA AUF ENGLISCH" },
          infoUrl: "https://reva.link/",
          icon: "",
          helpUrl: "",
          displayName: "",
        },
      ],
    };
  },
};
</script>

<style lang="scss">
.v-expansion-panel-content__wrap {
  padding: 16px 24px 16px !important;
}

.v-expansion-panel-header--active {
  color: #3f50b5;
}
</style>

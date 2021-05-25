<template>
  <v-main style="padding: 0px">
    <!-- move this into header bar-->
    <v-layout column align-end wrap>
      <v-switch
        v-model="showAll"
        inset
        :label="$gettext('show past projects')"
      ></v-switch>
    </v-layout>
    <ProjectList />
    <!-- put these into their own components -->
    <v-card-text
      style="
        position: fixed;
        z-index: 1000;
        bottom: 70px;
        width: auto;
        right: 5px;
      "
    >
      <v-fab-transition>
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-show="true"
              color="error"
              dark
              absolute
              top
              right
              fab
              @click="collapseProjects"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-arrow-collapse</v-icon>
            </v-btn>
          </template>
          <span v-translate>Collapse all</span>
        </v-tooltip>
      </v-fab-transition>
    </v-card-text>
    <v-card-text
      style="
        position: fixed;
        z-index: 1000;
        bottom: 5px;
        width: auto;
        right: 5px;
      "
    >
      <v-fab-transition>
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-show="true"
              color="success"
              dark
              absolute
              top
              right
              fab
              @click="addProject"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-plus-thick</v-icon>
            </v-btn>
          </template>
          <span><translate>New project</translate></span>
        </v-tooltip>
      </v-fab-transition>
    </v-card-text>
  </v-main>
</template>

<script>
/*import Header from '../components/Header'*/
import ProjectList from "../components/Project/List.vue";

export default {
  components: {
    ProjectList,
  },
  computed: {
    showAll: {
      get() {
        return this.$store.getters.showAllProjects;
      },
      set(val) {
        this.$store.commit("showAllProjects", val);
      },
    },
  },
  methods: {
    collapseProjects() {
      this.$root.$emit("collapseProjects");
    },
    addProject() {
      this.$store.dispatch("createProject");
    },
  },
};
</script>

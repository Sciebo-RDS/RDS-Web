<template>
  <v-main style="padding: 0px">
    <!-- move this into header bar-->
    <v-layout column align-end wrap>
      <v-switch v-model="showAll" inset label="show past projects"></v-switch>
    </v-layout>
    <ProjectList
      v-if="this.showAll"
      @delete-project="deleteProject"
      :projects="projects"
      :panel="panel"
    />
    <ProjectList
      v-else
      @delete-project="deleteProject"
      :projects="activeProjects"
      :panel="panel"
    />
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
          <span><translate>Collapse all</translate></span>
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
import ProjectList from "../components/ProjectList.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    ProjectList,
  },
  data: () => ({
    panel: [],
    showAll: false,
  }),
  computed: {
    activeProjects() {
      return this.projects.filter((project) => project.status < 3);
    },
    ...mapGetters({
      projects: "getProjectlist",
    }),
  },
  methods: {
    deleteProject(id) {
      this.$store.dispatch("removeProject", { id: id });
    },
    addProject() {
      this.$store.dispatch("createProject");
    },
    collapseProjects() {
      this.panel = [];
    },
  },
};
</script>

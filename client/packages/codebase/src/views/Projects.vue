<template>
  <v-main style="padding: 0px">
    <ProjectList @delete-project="deleteProject" :projects="projects" />
    <!-- put this into its own component -->
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
import ProjectList from "../components/ProjectList";
import { mapGetters } from "vuex";

export default {
  components: {
    ProjectList,
  },
  computed: {
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
  },
};
</script>

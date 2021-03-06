<template>
  <v-row justify="center">
    <v-card v-if="projects.length == 0" outlined tile>
      <v-card-title v-translate>No projects found</v-card-title>
      <v-card-text v-translate>
        Set the filter or create a new one project.
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="addProject">
          <translate>Create a new project</translate>
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-expansion-panels inset focusable multiple v-model="panel" v-else>
      <v-expansion-panel v-for="(project, i) in projects" :key="i">
        <v-expansion-panel-header>
          <v-row>
            <v-col cols="auto">
              <translate
                :translate-params="{
                  researchIndex: project.researchIndex + 1,
                }"
              >
                Project %{ researchIndex }
              </translate></v-col
            >
            <ProjectStatusChip v-bind:status="project.status" />
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ProjectSetting
            @delete-project="deleteProject(project.researchIndex)"
            :project="project"
          ></ProjectSetting>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-row>
</template>

<style lang="scss">
.v-expansion-panel-content__wrap {
  padding: 16px 24px 16px !important;
}

.v-expansion-panel-header--active {
  color: #3f50b5;
}
</style>

<script>
import ProjectSetting from "./Setting.vue";
import ProjectStatusChip from "./StatusChip.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    ProjectSetting,
    ProjectStatusChip,
  },
  data() {
    return {
      panel: [],
      projects: [],
    };
  },
  computed: {
    ...mapGetters({
      allProjects: "getProjectlist",
      showAllProjects: "showAllProjects",
    }),
    activeProjects() {
      return this.allProjects.filter((project) => project.status < 3);
    },
  },
  methods: {
    collapseProjects() {
      this.panel = [];
    },
    getProjects() {
      let projects = this.showAllProjects
        ? this.allProjects
        : this.activeProjects;

      return JSON.parse(JSON.stringify(projects)).sort((a, b) => {
        return b.status - a.status;
      });
    },
    deleteProject(researchIndex) {
      this.$store.dispatch("removeProject", { id: researchIndex });
      this.panel = [];
    },
    addProject() {
      this.$store.dispatch("createProject");
    },
  },
  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters.showAllProjects,
      (newValue) => {
        this.projects = this.getProjects();

        let diffCount = this.allProjects.length - this.activeProjects.length;
        this.panel = this.panel.map((val) => {
          let temp = newValue ? val + diffCount : val - diffCount;

          if (temp >= 0) {
            return temp;
          }
        });
      }
    );

    this.unwatch = this.$store.watch(
      (state, getters) => getters.getProjectlist,
      () => {
        this.projects = this.getProjects();
      }
    );
  },
  beforeMount() {
    this.projects = this.getProjects();
    console.log(
      "filter: ",
      this.showAllProjects,
      "active: ",
      this.activeProjects,
      "all: ",
      this.allProjects
    );
  },
  mounted() {
    this.$root.$on("collapseProjects", () => {
      this.collapseProjects();
    });
  },
  beforeDestroy() {
    this.unwatch();
  },
};
</script>

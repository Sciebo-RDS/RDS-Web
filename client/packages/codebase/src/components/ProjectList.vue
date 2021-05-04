<template>
  <v-row justify="center">
    <v-expansion-panels inset focusable multiple v-model="panel">
      <v-expansion-panel v-for="(project, i) in projects" :key="i">
        <v-expansion-panel-header>
          <v-row>
            <v-col cols="auto"> Project {{ project.researchIndex + 1 }} </v-col>
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
import ProjectSetting from "./ProjectSetting.vue";
import ProjectStatusChip from "./ProjectStatusChip.vue";
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
      let diffCount = this.allProjects.length - this.activeProjects.length;
      let projects = this.showAllProjects
        ? this.allProjects
        : this.activeProjects;

      this.panel = this.panel.map((val) => {
        return this.showAllProjects ? val + diffCount : val - diffCount;
      });

      return JSON.parse(JSON.stringify(projects)).sort((a, b) => {
        return b.status - a.status;
      });
    },
    deleteProject(id) {
      this.$store.dispatch("removeProject", { id: id });
    },
  },
  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters.showAllProjects,
      (newValue, oldValue) => {
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

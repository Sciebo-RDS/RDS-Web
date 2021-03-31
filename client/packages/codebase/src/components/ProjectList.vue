<template>
  <v-row justify="center">
    <v-expansion-panels inset focusable multiple v-model="panel">
      <v-expansion-panel v-for="(project, i) in projects" :key="i">
        <v-expansion-panel-header>
          <v-row>
            <v-col cols="auto"> Project {{ project.researchId + 1 }} </v-col>
            <ProjectStatusChip v-bind:status="project.status" />
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ProjectSetting
            @delete-project="$emit('delete-project', project.researchId)"
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

export default {
  components: {
    ProjectSetting,
    ProjectStatusChip,
  },
  props: {
    projects: Array,
    panel: Array,
  },
  methods: {},
};
</script>
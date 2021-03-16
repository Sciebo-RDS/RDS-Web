<template>
    <v-row justify="center">
      <v-expansion-panels inset focusable>
      <v-expansion-panel
        v-for="(project,i) in projects"
        :key="i"
        >
        <v-expansion-panel-header> Project {{ project.researchId+1 }} </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ProjectSetting @delete-project="$emit('delete-project', project.researchId)" :project=project></ProjectSetting>
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
import ProjectSetting from './ProjectSetting'

export default {
  components: {
    ProjectSetting
    },
    props: {
      projects: Array,
    },
    methods: {
    }
}
</script>
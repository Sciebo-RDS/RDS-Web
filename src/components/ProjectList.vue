<template>
    <v-row justify="center">
      <v-expansion-panels inset focusable>
      <v-expansion-panel
        v-for="(project,i) in projects"
        :key="i"
        >
        <v-expansion-panel-header> Project {{ project.researchId+1 }} </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ProjectSetting :project=project></ProjectSetting>
        </v-expansion-panel-content>
      </v-expansion-panel>
      </v-expansion-panels>
      <v-btn @click="addProject">Add</v-btn>
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
      /* hardcoded test data for now */
      addProject () {
        this.projects.push({
        portIn: [
          {
            port: "port-reva",
            properties: {
              type: ["fileStorage"],
              customProperties: {
                filepath: "/RDSTest",
              },
            },
          },
        ],
        portOut: [
          {
            port: "port-zenodo",
            properties: {
              type: ["metadata"],
              customProperties: {
                projectId: "719218",
              },
            },
          },
        ],
        researchId: this.projects.length,
        researchIndex: 0,
        status: 1,
        userId: "admin",
      })
      }
    }
}
</script>
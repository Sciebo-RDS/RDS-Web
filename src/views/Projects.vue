<template>
  <v-main style="padding: 0px">
    <ProjectList @delete-project="deleteProject" :projects="projects"  />
    <!-- put this into its own component -->
    <v-card-text style="position: fixed; z-index: 1000; bottom: 5px; width: auto; right: 5px;">
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
import ProjectList from '../components/ProjectList'

export default {
  components: {
    ProjectList,
  },
  data: () => ({
    projects: [
      {
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
        researchId: 0,
        researchIndex: 0,
        status: 1,
        userId: "admin",
      },
      {
        portIn: [
          {
            port: "port-owncloud",
            properties: {
              type: ["fileStorage"],
              customProperties: {
                filepath: "/rocratetestfolder",
              },
            },
          },
        ],
        portOut: [
          {
            port: "port-datasafe",
            properties: {
              type: ["metadata"],
            },
          },
        ],
        researchId: 1,
        researchIndex: 1,
        status: 1,
        userId: "admin",
      },
      {
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
        researchId: 2,
        researchIndex: 2,
        status: 1,
        userId: "admin",
      },
    ],
  }),
  methods: {
    deleteProject(id) {
      this.projects = this.projects.filter((projects) => projects.researchId !== id)
    },
    /* hardcoded test data for now */
      addProject () {
        this.projects.push({
        portIn: [
          {
            port: "",
            properties: {
              type: [""],
              customProperties: {
                filepath: "none",
              },
            },
          },
        ],
        portOut: [
          {
            port: "",
            properties: {
              type: [""],
              customProperties: {
                projectId: Math.floor(Math.random()*10000),
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
    },
};
</script>

<template>
  <v-main style="padding: 0px">
    <!-- move this into header bar-->
    <v-layout column align-end wrap>
    <v-switch
      v-model="showAll"
      inset
      label="show past projects"
    ></v-switch>
    </v-layout>
    <ProjectList v-if="this.showAll" @delete-project="deleteProject" :projects="projects" :panel="panel" />
    <ProjectList v-else @delete-project="deleteProject" :projects="activeProjects" :panel="panel" />
    <!-- put these into their own components -->
    <v-card-text style="position: fixed; z-index: 1000; bottom: 70px; width: auto; right: 5px;">
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
        status: 3,
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
        status: 0,
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
    panel: [],
    showAll: false
  }),
  computed: {
    activeProjects() {
      return this.projects.filter( project => project.status < 3);
    }
  },
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
        status: 4,
        userId: "admin",
      })
      },
      collapseProjects () {
        this.panel = [];
      },
    },
};
</script>

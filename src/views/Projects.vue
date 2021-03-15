<template>
  <v-main style="padding: 0px">
    <ProjectList :projects="projects"  />
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
};
</script>

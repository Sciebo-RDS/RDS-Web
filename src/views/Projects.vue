<template>
  <v-container>Heyho</v-container>
</template>

<script>
export default {
  data: () => ({
    projects: [
      {
        userId: "admin",
        researchIndex: 0,
        researchId: 0,
        status: 1,
        portIn: [
          {
            port: "port-reva",
            properties: [
              { portType: "fileStorage", value: true },
              {
                portType: "customProperties",
                value: [{ key: "filepath", value: "/RDSTest" }],
              },
            ],
          },
        ],
        portOut: [
          {
            port: "port-zenodo",
            properties: [
              { portType: "metadata", value: true },
              {
                portType: "customProperties",
                value: [{ key: "projectId", value: "719218" }],
              },
            ],
          },
        ],
      },
      {
        userId: "admin",
        researchIndex: 1,
        researchId: 1,
        status: 1,
        portIn: [
          {
            port: "port-owncloud",
            properties: [
              { portType: "fileStorage", value: true },
              {
                portType: "customProperties",
                value: [{ key: "filepath", value: "/rocratetestfolder" }],
              },
            ],
          },
        ],
        portOut: [
          {
            port: "port-datasafe",
            properties: [{ portType: "metadata", value: true }],
          },
        ],
      },
      {
        userId: "admin",
        researchIndex: 2,
        researchId: 2,
        status: 1,
        portIn: [
          {
            port: "port-reva",
            properties: [
              { portType: "fileStorage", value: true },
              {
                portType: "customProperties",
                value: [{ key: "filepath", value: "/RDSTest" }],
              },
            ],
          },
        ],
        portOut: [
          {
            port: "port-zenodo",
            properties: [
              { portType: "metadata", value: true },
              {
                portType: "customProperties",
                value: [{ key: "projectId", value: "719218" }],
              },
            ],
          },
        ],
      },
    ],
  }),
};
</script>
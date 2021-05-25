<template>
  <v-container>
    <v-card flat>
      <v-card-title v-translate> Publish your project </v-card-title>
      <v-card-subtitle v-translate>
        Make sure your settings are correct!
      </v-card-subtitle>
      <v-card-text>
        <!-- replace with logic-->
        PortIn: {{ port(project.portIn) }}<br />
        PortOut: {{ port(project.portOut) }}<br />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  props: ["project"],
  methods: {
    port(ports) {
      if (ports.length > 0) {
        return ports[0].port;
      }
      return "";
    },
  },
};
</script>

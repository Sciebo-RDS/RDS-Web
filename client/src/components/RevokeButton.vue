<template>
  <v-container fluid>
    <v-btn depressed @click="uninstallRDS">
      <translate>Uninstall sciebo RDS</translate>
    </v-btn>
  </v-container>
</template>

<script>
export default {
  name: "RevokeButton",
  methods: {
    uninstallRDS() {
      this.$requests.RDS.removeService(this.getInformations("port-owncloud"));
    },
  },
};
</script>
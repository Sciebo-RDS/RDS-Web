<template>
  <v-container fluid>
    <v-btn depressed @click="logout">
      <translate>Uninstall sciebo RDS</translate>
    </v-btn>
  </v-container>
</template>

<script>
export default {
  name: "RevokeButton",
  methods: {
    logout() {
      this.$store.dispatch("logout");
    },
  },
};
</script>
<template>
  <v-container>{{ researchlist }}</v-container>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState({
      researchlist: (state) => state.RDSStore.researchlist,
    }),
  },
  beforeCreate() {
    this.$services.RDS.requestResearchList();
  },
};
</script>

<template>
  <v-main style="padding: 0px">
    <v-layout column align-center wrap>
      <v-alert dense type="error" class="mb-6" v-show="!this.userservicelist">
        Please connect to at least one <strong>service</strong> to use RDS
      </v-alert>
    </v-layout>
    <ServiceList />
  </v-main>
</template>

<script>
import ServiceList from "../components/Service/List.vue";
export default {
  components: {
    ServiceList,
  },
};
</script>

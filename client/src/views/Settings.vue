<template>
  <v-container flex>
    <v-row>
      <v-col><LanguageSelector /></v-col>
      <v-col><ThemeSelector /></v-col>
      <v-col><ServiceSelector /></v-col>
    </v-row>
    <v-row>
      <v-col class="text-right"><RevokeButton /></v-col
    ></v-row>
  </v-container>
</template>

<script>
import LanguageSelector from "@/components/LanguageSelector.vue";
import ServiceSelector from "@/components/ServiceSelector.vue";
import RevokeButton from "@/components/RevokeButton.vue";
import ThemeSelector from "@/components/ThemeSelector.vue";

export default {
  components: {
    LanguageSelector,
    ServiceSelector,
    RevokeButton,
    ThemeSelector,
  },
};
</script>
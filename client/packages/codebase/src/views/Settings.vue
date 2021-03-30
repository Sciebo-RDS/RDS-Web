<template>
  <v-container flex>
    <v-row>
      <v-col><LanguageSelector /></v-col>
      <v-col><ThemeSelector /></v-col>
    </v-row>
    <v-row>
      <v-col><ServiceEditor /></v-col>
    </v-row>
  </v-container>
</template>

<script>
import LanguageSelector from "../components/LanguageSelector.vue";
import ThemeSelector from "../components/ThemeSelector.vue";
import ServiceEditor from "../components/ServiceEditor.vue";

export default {
  components: {
    LanguageSelector,
    ThemeSelector,
    ServiceEditor,
  },
};
</script>
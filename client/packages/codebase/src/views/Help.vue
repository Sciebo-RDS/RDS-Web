<template>
  <v-row justify="center" class="pt-10">
    <v-expansion-panels inset focusable multiple v-model="panel">
      <v-expansion-panel
        v-for="(item, i) in questions[this.$config.language]"
        :key="i"
      >
        <v-expansion-panel-header>
          {{ item.question }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <span v-html="markdown(item.answer)" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-row>
</template>

<script>
import marked from "marked";

export default {
  name: "Help",
  data() {
    return {
      panel: [],
      questions: {},
    };
  },
  beforeMount() {
    Vue.prototype.$http
      .get(`${Vue.config.server}/faq`)
      .then((response) => {
        this.questions = response.data;
      })
      .catch(() => {});
  },
  methods: {
    markdown(text) {
      console.log(text);
      console.log(marked(text));
      return marked(text);
    },
  },
};
</script>

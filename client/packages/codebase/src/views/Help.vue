<template>
  <v-expansion-panels inset focusable multiple v-model="panel">
    <v-expansion-panel
      v-for="(item, i) in questions[this.$config.language]"
      :key="i"
    >
      <v-expansion-panel-header>
        {{ item.question }}
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        {{ item.answer }}
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  name: "Help",
  data() {
    return {
      panel: [],
    };
  },
  computed: {
    questions() {
      return {
        de: [
          {
            question: "Dies ist die erste Frage.",
            answer: "Dies ist die erste Antwort.",
          },
          {
            question: "Dies ist die zweite Frage.",
            answer: "Dies ist die zweite Antwort.",
          },
        ],
        en: [
          {
            question: "This is the first question.",
            answer: "This is the first answer.",
          },
          {
            question: "This is the second question.",
            answer: "This is the second answer.",
          },
        ],
      };
    },
  },
};
</script>

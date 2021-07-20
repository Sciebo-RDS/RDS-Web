<template>
  <v-row justify="center" class="pt-10">
    <v-progress-circular
      indeterminate
      color="primary"
      size="64"
      v-if="Object.keys(questions).length == 0"
    >
      <translate>Wait</translate>
    </v-progress-circular>
    <v-expansion-panels inset focusable multiple v-model="panel" v-else>
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
import DOMPurify from "dompurify";
import { mapGetters } from "vuex";

const renderer = new marked.Renderer();
const linkRenderer = renderer.link;
renderer.link = (href, title, text) => {
  const localLink = href.startsWith(
    `${location.protocol}//${location.hostname}`
  );
  const html = linkRenderer.call(renderer, href, title, text);
  return localLink
    ? html
    : html.replace(
        /^<a /,
        `<a target="_blank" rel="noreferrer noopener nofollow" `
      );
};

export default {
  name: "Help",
  computed: {
    ...mapGetters({ questions: "getQuestions" }),
  },
  data() {
    return {
      panel: [],
    };
  },
  methods: {
    markdown(text) {
      const html = marked(text, { renderer });

      return DOMPurify.sanitize(html, { ADD_ATTR: ["target"] });
    },
  },
};
</script>

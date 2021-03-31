<template>
  <div class="uk-flex uk-flex-center uk-flex-middle uk-height-1-1 uk-width-1-1">
    <oc-spinner
      v-if="loading"
      :aria-label="this.$gettext('Loading media')"
      class="uk-position-center"
      size="xlarge"
    />
    <iframe
      class="uk-height-1-1 uk-width-1-1"
      v-else
      id="rds-editor"
      ref="rdsEditor"
      :src="iframeSource"
    />
  </div>
</template>

<script>
import queryString from "querystring";
import { mapGetters, mapActions } from "vuex";

export default {
  data: () => ({
    loading: true,
  }),
  computed: {
    ...mapGetters(["getToken"]),
    config() {
      console.log(this.$store.state.apps);
      const { url = "http://localhost:8085" } =
        this.$store.state.apps.fileEditors.find(
          (editor) => editor.app === "rds"
        ).config || {};
      return { url };
    },
    iframeSource() {
      const query = queryString.stringify({
        embed: 1,
      });
      return `${this.config.url}?${query}`;
    },
    rdsWindow() {
      return this.$refs.rdsEditor.contentWindow;
    },
  },
  methods: {
    ...mapActions(["showMessage"]),
  },
  mounted() {
    this.loading = false;
  },
  created() {
    window.addEventListener("message", (event) => {
      if (event.data.length > 0) {
        var payload = JSON.parse(event.data);
        switch (payload.event) {
          case "init":
            this.loading = false;
            break;
        }
      }
    });
  },
};
</script>

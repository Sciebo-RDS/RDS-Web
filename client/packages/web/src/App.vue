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
      const {
        url = "http://localhost:8085",
        server = this.$store.state.config.server,
      } =
        this.$store.state.apps.fileEditors.find(
          (editor) => editor.app === "rds"
        ).config || {};
      return { url, server };
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
    headers() {
      return new Headers({
        Authorization: "Bearer " + this.getToken,
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
      });
    },
  },
  methods: {
    ...mapActions(["showMessage"]),
    error(error) {
      console.log(response);
      this.showMessage({
        title: this.$gettext("The rds could not be loaded…"),
        desc: error,
        status: "danger",
        autoClose: {
          enabled: true,
        },
      });
    },
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
            let url = `${this.config.server}/index.php/apps/rds/api/1.0/informations`;
            fetch(url, { headers: this.headers })
              .then((response) => {
                if (response.ok) {
                  return response.text();
                }

                throw new Error(`${response.status} ${response.statusText}`);
              })
              .then((resp) => {
                this.rdsWindow.postMessage(
                  JSON.stringify({
                    event: "informations",
                    data: resp,
                  }),
                  "*"
                );
              })
              .catch((error) => {
                this.loading = true;
                this.error(error);
              });
            break;
          case "showFilePicker":
            // TODO show FilePicker
            let location = "";
            this.rdsWindow.postMessage(
              JSON.stringify({
                event: "folderLocationSelected",
                data: {
                  projectId: payload.data.projectId,
                  location: location,
                },
              }),
              "*"
            );
            break;
        }
      }
    });
  },
};
</script>

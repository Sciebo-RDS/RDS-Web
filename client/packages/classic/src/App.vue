<template>
  <div
    class="uk-flex uk-flex-center uk-flex-middle uk-height-1-1 uk-width-1-1"
    style="width: 100%; height: 100%"
  >
    <oc-spinner
      v-if="loading"
      aria-label="Loading..."
      class="uk-position-center"
      size="xlarge"
      style="width: 100%; height: 100%"
    />
    <iframe
      class="uk-height-1-1 uk-width-1-1"
      v-else
      id="rds-editor"
      ref="rdsEditor"
      :src="iframeSource"
      style="width: 100%; height: 100%"
    />
  </div>
</template>

<script>
import queryString from "querystring";
import getConfig from "./plugins/values.js";

export default {
  data: () => ({
    loading: true,
    config: {},
  }),
  computed: {
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
        requesttoken: oc_requesttoken,
        "Content-Type": "application/json",
      });
    },
  },
  methods: {
    error(error) {
      console.log(error);
    },
  },
  created() {
    getConfig()
      .then((config) => {
        console.log("huhu");
        this.config = config;
        this.loading = false;
      })
      .catch(() => {
        this.config = {
          url: "http://localhost:8085",
          server: "http://localhost:8085",
        };
        this.loading = false;
      });

    window.addEventListener("message", (event) => {
      if (event.data.length > 0) {
        var payload = JSON.parse(event.data);
        switch (payload.event) {
          case "init":
            const url = OC.generateUrl("/apps/rds/api/1.0/informations");
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
        }
      }
    });
  },
};
</script>

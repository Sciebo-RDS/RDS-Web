<template>
  <div class="text-center">
    <v-container flex v-if="loading">
      <v-row>
        <v-col>
          <v-progress-circular indeterminate color="primary" />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          {{ loadingText }}
        </v-col>
      </v-row>
    </v-container>
    <iframe
      v-show="!loading"
      ref="describoWindow"
      :src="iframeSource"
      height="500px"
      width="100%"
      style="border: 0px;"
    ></iframe>
  </div>
</template>

<script>
import queryString from "querystring";

export default {
  props: ["project"],
  data: () => ({
    loading: true,
    loadingText: "",
  }),
  computed: {
    editor() {
      return this.$refs.describoWindow.contentWindow;
    },
    parent() {
      return window.parent;
    },
    iframeSource() {
      const query = queryString.stringify({
        embed: 1,
        sid: this.$store.getters.getSessionId,
      });
      return `${this.$config.describo}?${query}`;
    },
    filePath() {
      if (this.project.portIn.length == 0) {
        // TODO add port-owncloud default to project!
        // FIXME add port-owncloud, when creating a new project. Not here!
        return "";
      }

      const service = this.getService(this.project.portIn, "port-owncloud");
      if (service !== undefined) {
        return service.properties.customProperties.filepath;
      }

      return "";
    },
  },
  methods: {
    eventloop(event) {
      if (event.data.length > 0) {
        var payload = JSON.parse(event.data);
        switch (payload.event) {
          case "init":
          case "load":
            this.parent.postMessage(
              JSON.stringify({
                event: "load",
                data: {
                  projectId: this.project.projectId,
                  filePath: this.filePath,
                },
              }),
              "*"
            );
            break;
          case "save":
          case "autosave":
            this.parent.postMessage(
              JSON.stringify({
                event: "save",
                data: {
                  projectId: this.project.projectId,
                  filePath: this.filePath,
                  fileData: this.fileData,
                },
              }),
              "*"
            );
            break;
          case "loaded":
            this.editor.postMessage(
              JSON.stringify({
                event: "loaded",
                data: payload.data,
              })
            );
            break;
          case "filesList":
            this.editor.postMessage(
              JSON.stringify({
                event: "filesList",
                data: payload.data,
              })
            );
        }
      }
    },
  },
  mounted() {
    this.standardLoadingText = this.$gettext("Editor loading");
    this.loadingText = this.standardLoadingText;
    let counter = 0;
    let loader = setInterval(() => {
      if (counter > 30) {
        this.loadingText = this.$gettext(
          "Error while loading. Please contact an administator."
        );
        clearInterval(loader);
      } else {
        if (counter % 4 > 0) {
          this.loadingText += ".";
        } else {
          this.loadingText = this.standardLoadingText;
        }
        counter += 1;
      }
    }, 1000);

    this.$refs.describoWindow.addEventListener("load", () => {
      this.loading = false;
      clearInterval(loader);
    });
  },
  created() {
    window.addEventListener("message", this.eventloop);
  },
  beforeDestroy() {
    window.removeEventListener("message", this.eventloop);
  },
};
</script>

<style></style>

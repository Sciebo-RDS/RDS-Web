<template>
  <div class="uk-flex uk-flex-center uk-flex-middle uk-height-1-1 uk-width-1-1">
    <oc-spinner
      v-if="loading"
      :aria-label="$gettext('Loading media')"
      class="uk-position-center"
      size="xlarge"
    />
    <iframe
      class="uk-height-1-1 uk-width-1-1"
      v-else
      id="rds-editor"
      ref="rdsEditor"
      :src="iframeSource"
      :disabled="showFilePicker"
    />
    <div style="position: absolute;" v-if="showFilePicker">
      <div class="app-background"></div>
      <div class="app app-variations-passive uk-position-relative">
        <div class="oc-modal-title">
          <h2 v-text="$gettext(`Select a folder`)" />
        </div>
        <file-picker
          ref="file-picker"
          variation="location"
          :bearerToken="getToken"
          :is-sdk-provided="true"
          :config-object="{}"
          :cancel-btn-label="$gettext(`Close`)"
          @selectResources="handleFilePick"
          @cancel="hideFilePicker"
        />
      </div>
    </div>
  </div>
</template>

<script>
import queryString from "querystring";
import { mapGetters, mapActions } from "vuex";
import FilePicker from "@ownclouders/file-picker";

export default {
  components: {
    FilePicker,
  },
  data: () => ({
    loading: true,
    showFilePicker: true,
    latestPayloadFromFrame: {},
    active: true,
  }),
  computed: {
    ...mapGetters(["getToken"]),
    config() {
      const {
        url = "http://localhost:8085",
        server = this.$store.state.config.server,
        autosave = false,
        describo = "http://localhost:8100",
      } =
        this.$store.state.apps.fileEditors.find(
          (editor) => editor.app === "rds"
        ).config || {};
      return { url, server, autosave, describo };
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
    load(filePath) {
      this.$client.files
        .getFileContents(filePath, { resolveWithResponseObject: true })
        .then((resp) => {
          this.rdsWindow.postMessage(
            JSON.stringify({
              action: "load",
              xml: resp.body,
              autosave: this.config.autosave,
            }),
            "*"
          );
        })
        .catch((error) => {
          this.error(error);
        });
    },
    save(filePath, payload) {
      this.$client.files
        .putFileContents(filePath, payload.xml, {
          previousEntityTag: this.currentETag,
        })
        .then((resp) => {
          this.currentETag = resp.ETag;
          this.rdsWindow.postMessage(
            JSON.stringify({
              action: "status",
              modified: false,
            }),
            "*"
          );
        })
        .catch((error) => {
          this.error(error);
        });
    },
    exit() {
      window.close();
    },
    hideFilePicker() {
      this.showFilePicker = false;
    },
    handleFilePick(event) {
      this.hideFilePicker();
      const location = event[0].path;
      this.rdsWindow.postMessage(
        JSON.stringify({
          event: "filePathSelected",
          data: {
            projectId: this.latestPayloadFromFrame.projectId,
            filePath: location,
          },
        }),
        "*"
      );
    },
    eventloop(event) {
      if (event.data.length > 0) {
        let payload = JSON.parse(event.data);
        let data = payload.data;
        this.latestPayloadFromFrame = data;

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
            this.showFilePicker = true;
            break;
          case "load":
            this.rdsWindow.postMessage(
              JSON.stringify({
                event: "loaded",
                data: {
                  projectId: data.projectId,
                  filePath: data.filePath,
                  fileData: this.load(data.filePath),
                },
              }),
              "*"
            );
            break;
          case "save":
            this.save(data.filePath, data.fileData);
            break;
          case "exit":
            this.exit();
            break;
        }
      }
    },
  },
  mounted() {
    this.loading = false;
    window.addEventListener("message", this.eventloop);
  },
  beforeDestroy() {
    window.removeEventListener("message", this.eventloop);
  },
};
</script>

<style lang="scss">
@mixin oc-modal-variation($color) {
  border-top-color: $color;
  span {
    color: $color;
  }
}

.app {
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 1);
  border-top: 10px solid var(--oc-color-swatch-passive-default);
  box-shadow: 0 2px 4px rgba(14, 30, 37, 0.25);
  max-width: 500px;
  overflow: hidden;
  width: 100%;
  z-index: 5;
  &:focus {
    outline: none;
  }
  &-background {
    align-items: center;
    background-color: rgba(255, 255, 255, 0.3);
    display: flex;
    flex-flow: row wrap;
    height: 100%;
    justify-content: center;
    left: 0;
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 4;
  }
  &-primary {
    @include oc-modal-variation(var(--oc-color-swatch-primary-default));
  }
  &-success {
    @include oc-modal-variation(var(--oc-color-swatch-success-default));
  }
  &-warning {
    @include oc-modal-variation(var(--oc-color-swatch-warning-default));
  }
  &-danger {
    @include oc-modal-variation(var(--oc-color-swatch-danger-default));
  }
  &-title {
    align-items: center;
    background-color: var(--oc-color-text-inverse);
    display: flex;
    flex-flow: row wrap;
    padding: var(--oc-space-small) var(--oc-space-medium);
    > .oc-icon {
      margin-right: var(--oc-space-small);
    }
    > h2 {
      font-size: 1rem;
      font-weight: bold;
      margin: 0;
    }
  }
  &-body {
    background-color: var(--oc-color-background-muted);
    color: var(--oc-color-text-default);
    padding: var(--oc-space-medium);
    &-message {
      margin-bottom: var(--oc-space-medium);
    }
    &-input {
      /* FIXME: this is ugly, but required so that the bottom padding doesn't look off when reserving vertical space for error messages below the input. */
      margin-bottom: -20px;
      padding-bottom: var(--oc-space-medium);
    }
    &-actions {
      text-align: right;
      .oc-button {
        border-radius: 4px;
        &.uk-button-default {
          background-color: var(--oc-color-text-inverse);
          color: var(--oc-color-text-default);
        }
      }
    }
  }
}
</style>

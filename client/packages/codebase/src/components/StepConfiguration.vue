<template>
  <v-container>
    <v-card flat>
      <v-card-title>Configure your Project</v-card-title>
      <!--<v-card-subtitle>Please select the services you want to publish to: </v-card-subtitle>-->
      <v-row>
        <v-col>
          <v-card flat>
            <v-card-subtitle
              >1. Which folder do you want to publish?</v-card-subtitle
            >
            <v-card-actions
              ><v-btn @click="togglePicker"
                >Select Folder</v-btn
              ></v-card-actions
            >
            <v-card-subtitle
              style="padding-top: 0px"
              v-if="!!filepath(project) || !!currentFilePath"
              >Current Folder: {{ currentFilePath }}</v-card-subtitle
            >
          </v-card>
        </v-col>
        <v-col>
          <v-card flat>
            <v-card-subtitle
              >2. Which Services do you want to publish to?</v-card-subtitle
            >
            <v-card-text>
              <v-select
                v-model="selectedPorts"
                @change="emitChanges"
                :items="
                  ports.filter((i) => i['servicename'] !== 'port-owncloud')
                "
                :item-text="(item) => parseServicename(item.servicename)"
                :item-value="(item) => item"
                :label="$gettext('Select your Services')"
                multiple
                chips
              >
                <template v-slot:prepend-item>
                  <v-list-item ripple @click="toggle">
                    <v-list-item-action>
                      <v-icon
                        :color="
                          selectedPorts.length > 0 ? 'indigo darken-4' : ''
                        "
                      >
                        {{ icon }}
                      </v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title> Select All </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-divider class="mt-2"></v-divider>
                </template>
              </v-select>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data: () => ({
    selectedPorts: [],
    currentFilePath: "",
  }),
  computed: {
    ...mapGetters({
      ports: "getUserServiceList",
    }),
    selectAllPorts() {
      return this.selectedPorts.length === this.ports.length;
    },
    selectSomePorts() {
      return this.selectedPorts.length > 0 && !this.selectAllPorts;
    },
    icon() {
      if (this.selectAllPorts) return "mdi-close-box";
      if (this.selectSomePorts) return "mdi-minus-box";
      return "mdi-checkbox-blank-outline";
    },
  },
  beforeMount() {
    function portHas(ports, servicename) {
      for (const port of ports) {
        if (port.port === servicename) {
          return true;
        }
      }
      return false;
    }

    this.userPorts = this.selectedPorts = this.ports.filter((port) =>
      portHas(this.project.portOut, port.servicename)
    );

    this.currentFilePath = this.filepath(this.project);
    window.addEventListener("message", this.eventloop);
    if (!this.project.portIn.length) {
      this.emitChanges();
    }
  },
  beforeDestroy() {
    window.removeEventListener("message", this.eventloop);
  },
  methods: {
    eventloop(event) {
      if (event.data.length > 0) {
        var payload = JSON.parse(event.data);
        switch (payload.event) {
          case "filePathSelected":
            let data = payload.data;
            if (data.projectId == this.project.projectId) {
              this.currentFilePath = data.filePath;
              this.emitChanges();
            }
            break;
        }
      }
    },
    togglePicker() {
      this.showFilePicker(this.project.projectId, this.currentFilePath);
    },
    computeChanges() {
      let strippedRemoveOut = this.computeStrippedOut(this.computeRemoveOut());
      let strippedAddOut = this.computeStrippedOut(this.computeAddOut());
      let importAdd = this.setImportAdd();
      let changes = {
        researchIndex: this.project["researchIndex"],
        import: {
          add: importAdd,
          remove: [],
          change: [],
        },
        export: {
          add: strippedAddOut,
          remove: strippedRemoveOut,
          change: [],
        },
      };
      return changes;
    },
    computeRemoveOut() {
      return this.userPorts.filter((i) => !this.selectedPorts.includes(i));
    },
    computeAddOut() {
      return this.selectedPorts.filter((i) => !this.userPorts.includes(i));
    },
    computeStrippedOut(pOut) {
      let strippedOut = [];
      for (let i of pOut) {
        strippedOut.push({ servicename: i.servicename });
      }
      return strippedOut;
    },
    setImportAdd() {
      let add = [];
      if (this.project.portIn.length == 0) {
        return [
          { servicename: "port-owncloud", filepath: this.currentFilePath },
        ];
      }
      for (let i of this.project["portIn"]) {
        if (!!this.currentFilePath) {
          add = [
            {
              servicename: i["port"],
              filepath: this.currentFilePath,
            },
          ];
        }
      }
      return add;
    },
    emitChanges() {
      let payload = this.computeChanges();
      this.$emit("changePorts", payload);
      this.changes = {};
    },
    filepath(project) {
      if (!!project.portIn.length) {
        return "";
      }
      const service = this.getService(project.portIn, "port-owncloud");
      if (service !== undefined) {
        return service.properties.customProperties.filepath;
      }

      return "";
    },
    toggle() {
      this.$nextTick(() => {
        if (this.selectAllPorts) {
          this.selectedPorts = [];
        } else {
          this.selectedPorts = this.ports.slice();
        }
      });
    },
    alert(msg) {
      alert(msg);
    },
  },
  props: ["project"],
};
</script>

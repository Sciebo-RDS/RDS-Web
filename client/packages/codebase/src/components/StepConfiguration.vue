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
              v-if="filepath(project) !== ``"
              >Current Folder: {{ filepath(project) }}</v-card-subtitle
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
                :items="ports"
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

    this.selectedPorts = this.ports.filter((port) =>
      portHas(this.project.portOut, port.servicename)
    );
  },
  methods: {
    togglePicker() {
      this.showFilePicker(this.project.projectId, this.filepath(this.project));
    },
    filepath(project) {
      if (project.portIn.length == 0) {
        // TODO add port-owncloud default to project!
        // FIXME add port-owncloud, when creating a new project. Not here!
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
    savePorts(research) {
      function filterPortsWhichNotContained(ports, filterports) {
        let distinctPorts = [];
        for (const port of ports) {
          let found = false;
          for (const newPort of filterports) {
            if (port.port == newPort.port) {
              found = true;
            }
          }
          if (!found) {
            distinctPorts.push(port);
          }
        }
        return distinctPorts;
      }

      function applyFnOnPorts(ports, fn) {
        for (const port of ports) {
          fn(research, port);
        }
      }

      applyFnOnPorts(
        filterPortsWhichNotContained(research.portOut, this.selectedPorts),
        this.removePort
      );

      applyFnOnPorts(
        filterPortsWhichNotContained(this.selectedPorts, research.portOut),
        this.addPort
      );
    },
    addPort(research, port) {
      port.researchId = research.researchIndex;
      this.$store.dispatch("addPortOut", port);
    },
    removePort(research, port) {
      port.researchId = research.researchIndex;
      this.$store.dispatch("removePortOut", port);
    },
  },
  props: ["project"],
};
</script>
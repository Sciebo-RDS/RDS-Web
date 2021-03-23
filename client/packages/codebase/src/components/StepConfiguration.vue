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
              ><v-btn @click="alert('this will open a file browser')"
                >Select Folder</v-btn
              ></v-card-actions
            >
            <v-card-subtitle style="padding-top: 0px"
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
    filepath(project) {
      if (project.portIn.length > 0) {
        return project.portIn[0].properties.customProperties.filepath;
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
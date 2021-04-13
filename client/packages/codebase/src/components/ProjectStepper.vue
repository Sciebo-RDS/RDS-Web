<template>
  <v-stepper v-model="e1" alt-labels>
    <v-stepper-header>
      <v-stepper-step :complete="e1 > 1" step="1">
        Configuration
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step :complete="e1 > 2" step="2"> Metadata </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step step="3"> Publish </v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">
        <v-card class="mb-12" height="auto" flat>
          <StepConfiguration :project="project" @changePorts="receiveChanges" />
        </v-card>

        <v-btn text disabled> Back </v-btn>

        <v-btn color="primary" @click="[e1 = 2, sendChanges()]"> Continue </v-btn>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-card
          class="d-flex flex-column justify-center mb-12"
          min-height="500px"
        >
          <StepMetadataEditor :project="project" />
        </v-card>

        <v-btn text @click="e1 = 1"> Back </v-btn>

        <v-btn color="primary" @click="e1 = 3"> Continue </v-btn>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-card class="mb-12" height="auto" flat>
          <StepPublish :project="project" />
        </v-card>

        <v-btn text @click="e1 = 2"> Back </v-btn>

        <v-btn color="success" @click="publishProject">
          Publish
        </v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<style scoped>
/*.v-stepper__header {
  box-shadow: none;
} 
.v-stepper {
  box-shadow: none;
}*/
</style>

<script>
import StepConfiguration from "./StepConfiguration.vue";
import StepPublish from "./StepPublish.vue";
import StepMetadataEditor from "./StepMetadataEditor.vue";

export default {
  components: {
    StepConfiguration,
    StepPublish,
    StepMetadataEditor,
  },
  data() {
    return {
      e1: 1,
    };
    changes: {}
  },
  props: ["project"],
  methods: {
    alert(msg) {
      alert(msg);
    },
    receiveChanges(pChanges) {
      this.changes = pChanges
    },
    sendChanges() {
      this.$store.dispatch("changePorts", this.changes)
    },
    publishProject() {
      this.$store.dispatch("triggerSynchronization", {'researchIndex' : this.project["researchIndex"]})
    }
  },
};
</script>
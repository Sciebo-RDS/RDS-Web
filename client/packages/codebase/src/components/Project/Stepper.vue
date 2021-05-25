<template>
  <v-stepper v-model="e1" alt-labels>
    <v-stepper-header>
      <v-stepper-step :complete="e1 > 1" step="1">
        <translate>Configuration</translate>
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step :complete="e1 > 2" step="2">
        <translate>Metadata</translate>
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step step="3"><translate>Publish</translate> </v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">
        <v-card class="mb-12" height="auto" flat>
          <StepConfiguration :project="project" @changePorts="receiveChanges" />
        </v-card>

        <v-btn text disabled><translate>Back</translate></v-btn>

        <v-btn color="primary" @click="[sendChanges(), (e1 = 2)]">
          <translate>Continue</translate>
        </v-btn>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-card
          v-if="e1 == 2"
          class="d-flex flex-column justify-center mb-12"
          min-height="500px"
        >
          <StepMetadataEditor :project="project" />
        </v-card>

        <v-btn text @click="e1 = 1">
          <translate>Back</translate>
        </v-btn>

        <v-btn color="primary" @click="e1 = 3">
          <translate>Continue</translate>
        </v-btn>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-card class="mb-12" height="auto" flat>
          <StepPublish :project="project" />
        </v-card>

        <v-btn text @click="e1 = 2">
          <translate>Back</translate>
        </v-btn>

        <v-btn color="success" @click="publishProject" ref="publishBtn">
          <translate>Publish</translate>
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
import StepConfiguration from "./Step/Configuration.vue";
import StepPublish from "./Step/Publish.vue";
import StepMetadataEditor from "./Step/MetadataEditor.vue";

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
    changes: {
    }
  },
  props: ["project"],
  methods: {
    publishProject() {
      this.$refs.publishBtn.value = this.$gettext("In progress...");
      this.$refs.publishBtn.disabled = false;
      this.$socket.client.emit(
        "triggerSynchronization",
        {
          researchIndex: this.project.researchIndex,
        },
        () => {
          this.$refs.publishBtn.value = this.$gettext("Publishing done");
        }
      );
    },
    receiveChanges(pChanges) {
      this.changes = pChanges;
    },
    sendChanges() {
      this.$store.dispatch("changePorts", this.changes);
    },
  },
};
</script>

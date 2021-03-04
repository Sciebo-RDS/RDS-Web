<template>
    <v-stepper v-model="e1" alt-labels>
    <v-stepper-header>
      <v-stepper-step
        :complete="e1 > 1"
        step="1"
      >
        Configuration
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step
        :complete="e1 > 2"
        step="2"
      >
        Metadata
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step step="3">
        Publish
      </v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">
        <v-card
          class="mb-12"
          color="white"
          height="auto"
          flat
        >
            <StepConfiguration/>
        </v-card>

        <v-btn text
        disabled>
          Back
        </v-btn>

        <v-btn
          color="primary"
          @click="e1 = 2"
        >
          Continue
        </v-btn>

      </v-stepper-content>

      <v-stepper-content step="2">
        <v-card
          class="mb-12"
          color="grey lighten-1"
          height="200px"
        ></v-card>

        <v-btn text
        @click="e1 = 1">
          Back
        </v-btn>

        <v-btn
          color="primary"
          @click="e1 = 3"
        >
          Continue
        </v-btn>

      </v-stepper-content>

      <v-stepper-content step="3">
        <v-card
          class="mb-12"
          color="white"
          height="auto"
          flat
        >
        <StepPublish/>
        </v-card>

        <v-btn text
        @click="e1 = 2">
          Back
        </v-btn>

        <v-btn
          color="success"
        >
          Publish
        </v-btn>

      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script>
import StepConfiguration from "./StepConfiguration"
import StepPublish from "./StepPublish"

  export default {
    components: {
        StepConfiguration,
        StepPublish
    },
    data () {
      return {
        e1: 1,
      }
    },
  }
</script>
<template>
  <div>
    <v-container>
      <v-row>
        <v-col>
          <ProjectStepper :project="project" />
        </v-col>
      </v-row>

      <v-row align-content="end" justify="space-around">
        <v-col cols="auto" class="mr-auto" />
        <v-col
          v-if="project.status != '3' && project.status != '4'"
          cols="auto"
        >
          <v-progress-circular
            indeterminate
            color="primary"
            v-if="loading"
            class="mr-2"
          />
          <v-btn
            :disabled="loading"
            tile
            color="error"
            @click="onDelete(project.researchIndex)"
          >
            <translate>delete project</translate>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import ProjectStepper from "./Stepper.vue";
export default {
  components: {
    ProjectStepper,
  },
  data() {
    return {
      loading: false,
    };
  },
  props: ["project"],
  methods: {
    onDelete(id) {
      this.loading = true;
      this.$emit("delete-project", id);
    },
  },
};
</script>

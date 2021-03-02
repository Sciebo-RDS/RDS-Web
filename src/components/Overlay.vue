<template>
  <div class="text-center">
    <v-overlay :value="visible">
      <v-container flex>
        <v-row align="center" justify="center">
          <v-col>
            <v-progress-circular indeterminate size="64"
              ><translate>Wait</translate>
            </v-progress-circular>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-col>
            <translate>Service activation in progress</translate>
          </v-col>
        </v-row>
      </v-container>
    </v-overlay>
  </div>
</template>

<script>
export default {
  data: () => ({
    visible: false,
  }),
  mounted() {
    this.$root.$on("showoverlay", () => {
      this.show();
    });

    this.$root.$on("hideoverlay", () => {
      this.hide();
    });
  },
  methods: {
    triggerOverlay() {
      this.visible = !this.visible;
    },
    hide() {
      this.visible = false;
    },
    show() {
      this.visible = true;
    },
  },
};
</script>
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
          <v-col>{{ subtext }}</v-col>
        </v-row>
      </v-container>
    </v-overlay>
  </div>
</template>

<script>
import Vue from "vue";

export default {
  data: () => ({
    visible: false,
  }),
  props: {
    subtext: {
      type: String,
      default: Vue.prototype.$gettext("Service activation in progress"),
    },
  },
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
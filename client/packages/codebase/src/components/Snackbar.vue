<template>
  <v-snackbar v-model="snackbar" :multi-line="multiLine">
    {{ text }}

    <template v-slot:action="{ attrs }">
      <v-btn color="red" text v-bind="attrs" @click="snackbar = false">
        <translate>Close</translate>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  components: {
    text: "Hey there, i am the snackbar.",
    snackbar: false,
    multiLine: true,
  },
  methods: {
    show() {
      this.snackbar = true;
    },
    hide() {
      this.snackbar = false;
    },
    toggle() {
      this.snackbar = !this.snackbar;
    },
  },
  onMounted() {
    this.$root.$on("showsnackbar", (text) => {
      this.text = text;
      this.show();
    });
    this.$root.$on("hidesnackbar", () => {
      this.hide();
    });
  },
};
</script>

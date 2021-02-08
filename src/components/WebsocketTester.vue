<template>
  <v-card class="mx-auto pa-4" min-width="400px"
    ><v-text-field
      v-model="message"
      label="Enter your message here"
      @keydown.enter="sendSocket"
    ></v-text-field>
    <v-btn @click="sendSocket">Send socket</v-btn>
    <v-subheader translate>Last message</v-subheader>
    <v-divider />
    <v-card-text>{{ lastMessage }}</v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "WebsocketTester",
  data: () => ({
    message: "",
  }),

  computed: {
    lastMessage: {
      get() {
        return this.$store.getters.getLastMessage;
      },
    },
  },
  methods: {
    sendSocket() {
      this.$services.RDS.sendMessage(this.message);
    },
  },
};
</script>

<style>
</style>
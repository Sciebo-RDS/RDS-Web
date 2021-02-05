<template>
  <v-container flex>
    <v-row>
      <v-col><LanguageSelector /></v-col>
      <v-col><ThemeSelector /></v-col>
      <v-col><ServiceSelector /></v-col>
    </v-row>
    <v-row>
      <v-col class="text-right"><RevokeButton /></v-col
    ></v-row>
    <v-row
      ><v-col
        ><v-card class="mx-auto pa-4" min-width="400px"
          ><v-text-field
            v-model="message"
            label="Enter your message here"
            @keydown.enter="sendSocket"
          ></v-text-field>
          <v-btn @click="sendSocket">Send socket</v-btn>
          <v-subheader translate>Last message</v-subheader>
          <v-divider />
          <v-card-text>{{ lastMessage }}</v-card-text>
        </v-card></v-col
      ></v-row
    >
  </v-container>
</template>

<script>
import LanguageSelector from "@/components/LanguageSelector.vue";
import ServiceSelector from "@/components/ServiceSelector.vue";
import RevokeButton from "@/components/RevokeButton.vue";
import ThemeSelector from "@/components/ThemeSelector.vue";
import { mapGetters } from "vuex";

export default {
  data: () => ({
    message: "",
  }),

  computed: {
    ...mapGetters({
      getLastMessage: "getLastMessage",
    }),
    lastMessage: {
      get() {
        return this.getLastMessage;
      },
    },
  },
  methods: {
    sendSocket() {
      this.$socket.emit("sendMessage", { message: this.message });
    },
  },
  components: {
    LanguageSelector,
    ServiceSelector,
    RevokeButton,
    ThemeSelector,
  },
};
</script>
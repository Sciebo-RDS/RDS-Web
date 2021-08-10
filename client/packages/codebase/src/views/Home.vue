<template>
  <div class="home">
    <!--<v-layout column align-end wrap v-if="userHasServicesConnected">
      at least one service is connected
    </v-layout>-->
    <v-layout>
      <Frame :source="'/frames/' + $config.language + '/welcome.html'"></Frame>
    </v-layout>
  </div>
</template>

<script>
// @ is an alias to /src
import Frame from "../components/Frame.vue";

export default {
  name: "Home",
  components: {
    Frame,
  },
  data() {
    return {
      gettingStarted: "https://localhost:8000",
    };
  },
  computed: {
    userHasServicesConnected() {
      //hardcoded filter for owncloud, change
      if (this.userservicelist.length > 1) {
        return true;
      }
      return false;
    },
  },
  mounted() {
    window.addEventListener("message", this.receiveMessage);
  },
  beforeDestroy() {
    window.removeEventListener("message", this.receiveMessage);
  },
  methods: {
    receiveMessage(event) {
      if (event.data.func === "redirect") {
        this.$router.push(event.data.target);
      }
    },
  },
};
</script>

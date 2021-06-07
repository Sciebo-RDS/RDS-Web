<template>
  <div class="help">
    <Frame source="https://www.research-data-services.de">
      Click here to
      <v-btn color="primary" :href="gettingStarted">Getting started</v-btn>
    </Frame>
  </div>
</template>

<script>
// @ is an alias to /src
import Frame from "../components/Frame.vue";

export default {
  name: "Help",
  components: {
    Frame,
  },
  data() {
    return {
      gettingStarted: "https://localhost:8000",
    };
  },
};
</script>

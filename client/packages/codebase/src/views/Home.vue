<template>
  <div class="home">
    <Frame :source="'/frames/' + $config.language + '/start.html'"></Frame>
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
};
</script>

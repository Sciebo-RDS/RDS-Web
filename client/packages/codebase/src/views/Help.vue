<template>
  <div class="help">
    <Frame source="https://www.research-data-services.de" />
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

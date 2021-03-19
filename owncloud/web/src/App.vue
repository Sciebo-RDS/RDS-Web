<template>
  <div class="uk-flex uk-flex-center uk-flex-middle">
    <div class="uk-flex">
      <oc-button @click="sayHi" variation="primary">Say it</oc-button>
    </div>
    <h1 v-if="isMsgDisplayed">huhu Welcome to my extension!</h1>
  </div>
</template>

<script>
export default {
  name:"Hello",
  data: () => ({
    isMsgDisplayed: false,
  }),
  methods: {
    sayHi() {
      this.isMsgDisplayed = true;
    },
  },
};
</script>

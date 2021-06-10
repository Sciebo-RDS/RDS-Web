<template>
  <div class="ma-0 pa-0 fill-height height:100%; width:100%;">
    <iframe
      :src="source"
      class="ma-0 pa-0"
      frameborder="0"
      height="100%"
      width="100%"
    />

    <v-card
      class="text-center pa-2"
      style="width:100%; position: absolute; bottom: 0px;"
      tile
      flat
      v-if="!!$slots.default"
    >
      <slot></slot>
    </v-card>
  </div>
</template>

<script>
export default {
  props: {
    source: String,
  },
};
</script>
<style>
iframe {
  position: absolute;
  top: 0px;
  height: 100%;
  width: 100%;
  border: none;
  overflow-x: hidden;
}
</style>

<template>
  <v-container>
    <v-row class="fill-height">
      <v-col>
        <iframe :src="source" />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <slot></slot>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Frame",
  props: {
    source: String,
  },
};
</script>

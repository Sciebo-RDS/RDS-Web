<template>
  <v-card flat color="transparent">
    <v-chip
      v-if="this.status == '0'"
      color="grey lighten-3"
      class="ma-2"
      small
      v-translate
    >
      created
    </v-chip>
    <v-chip
      v-else-if="this.status == '1' || this.status == '2'"
      color="blue lighten-3"
      class="ma-2"
      small
      v-translate
    >
      modified
    </v-chip>
    <v-chip
      v-else-if="this.status == '3'"
      color="light-green lighten-1"
      class="ma-2"
      small
      v-translate
    >
      published
    </v-chip>
    <v-chip
      v-else-if="this.status == '4'"
      color="red lighten-3"
      class="ma-2"
      small
      v-translate
    >
      deleted
    </v-chip>
  </v-card>
</template>

<script>
export default {
  props: ["status"],
};
</script>

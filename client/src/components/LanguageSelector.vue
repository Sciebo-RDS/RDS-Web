<template>
  <v-card class="mx-auto pa-4" min-width="250px">
    <v-card-title v-translate>Settings for language</v-card-title>
    <v-select
      :value="$language.current"
      :items="availableLanguages"
      item-text="long"
      item-value="short"
      :label="$gettext('Select language')"
      @change="onChange"
    ></v-select>
  </v-card>
</template>

<script>
import Vue from "vue";

export default {
  name: "LanguageSelector",
  computed: {
    currentLanguage: function () {
      if (this.$language != undefined) {
        return "en";
      }
      return this.$language.current;
    },
    availableLanguages: function () {
      let res = [];
      for (const [key, value] of Object.entries(this.$language.available)) {
        res.push({ short: key, long: value });
      }

      return res;
    },
  },
  methods: {
    onChange(value) {
      this.$store.dispatch("setLanguage", { language: value });
      // Only load locale translation if not previously loaded
      if (!Object.prototype.hasOwnProperty.call(Vue.$translations, value)) {
        import("@/translations/" + value + ".json").then((locale) => {
          this.$language.merge(locale);
          this.$language.current = value;
        });
      } else {
        this.$language.current = value;
      }
    },
  },
};
</script>
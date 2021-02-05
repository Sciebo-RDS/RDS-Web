<template>
  <v-card class="mx-auto pa-4" min-width="400px">
    <v-card-title v-translate>Settings for services</v-card-title>
    <v-select
      v-model="selectedItems"
      :items="items"
      :label="$gettext('Select services')"
      multiple
    >
      <template v-slot:prepend-item>
        <v-list-item ripple @click="toggle">
          <v-list-item-action>
            <v-icon :color="selectedItems.length > 0 ? 'indigo darken-4' : ''">
              {{ icon }}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-translate> Select All </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
    </v-select>
    <v-btn
      depressed
      :disabled="!selectedServicesChanged"
      color="error"
      class="mr-3"
      @click="saveSelection"
    >
      <translate>Save selection and activate services</translate>
    </v-btn>
    <v-btn
      depressed
      :disabled="!selectedServicesChanged"
      @click="resetSelection"
    >
      <translate>Cancel service selection</translate>
    </v-btn>
  </v-card>
</template>

<script>
export default {
  name: "ServiceSelector",
  data: () => ({
    selectedItems: [],
    activatedItems: [],
  }),
  computed: {
    items: function () {
      return ["Zenodo", "OSF", "Reva"];
    },
    selectedServicesChanged() {
      function compare(arr, array) {
        // if the other array is a falsy value, return
        if (!array) return false;

        // compare lengths - can save a lot of time
        if (arr.length != array.length) return false;

        for (var i = 0, l = arr.length; i < l; i++) {
          // Check if we have nested arrays
          if (arr[i] instanceof Array && array[i] instanceof Array) {
            // recurse into the nested arrays
            if (!arr[i].equals(array[i])) return false;
          } else if (arr[i] != array[i]) {
            // Warning - two different object instances will never be equal: {x:20} != {x:20}
            return false;
          }
        }
        return true;
      }
      let res = !compare(this.selectedItems, this.activatedItems);
      return res;
    },
    selectedAllItems() {
      return this.selectedItems.length === this.items.length;
    },
    selectedSomeItems() {
      return this.selectedItems.length > 0 && !this.selectedAllItems;
    },
    icon() {
      if (this.selectedAllItems) return "mdi-close-box";
      if (this.selectedSomeItems) return "mdi-minus-box";
      return "mdi-checkbox-blank-outline";
    },
  },
  methods: {
    toggle: function () {
      this.$nextTick(() => {
        if (this.selectedAllItems) {
          this.selectedItems = [];
        } else {
          this.selectedItems = this.items.slice();
        }
      });
    },
    resetSelection: function () {
      this.$nextTick(() => {
        this.selectedItems = this.activatedItems;
      });
    },
    saveSelection: function () {
      if (this.selectedItems.length == 0) {
        // change text
      }
      this.activatedItems = this.selectedItems;
    },
  },
};
</script>
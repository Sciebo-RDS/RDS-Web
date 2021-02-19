<template>
  <v-card class="mx-auto pa-4" min-width="400px">
    <v-card-title v-translate>Settings for services</v-card-title>
    <v-select
      v-model="selectedItems"
      :items="servicelist"
      :label="$gettext('Select services')"
      multiple
      :disabled="!firstRunFinished"
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
      :disabled="!selectedServicesChanged || !firstRunFinished"
      color="error"
      class="mr-3"
      @click="saveSelection"
    >
      <translate>Save selection and activate services</translate>
    </v-btn>
    <v-btn
      depressed
      :disabled="!selectedServicesChanged || !firstRunFinished"
      @click="resetSelection"
    >
      <translate>Cancel service selection</translate>
    </v-btn>
  </v-card>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ServiceSelector",
  data: () => ({
    selectedItems: [],
    firstRunFinished: false,
  }),
  watch: {
    activatedItems(newVal) {
      if (!this.firstRunFinished) {
        this.selectedItems = newVal;
        this.firstRunFinished = true;
      }
    },
  },
  computed: {
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
      servicelist: (state) => state.RDSStore.servicelist,
    }),
    activatedItems: {
      get() {
        return this.userservicelist;
      },
      set(servicelist) {
        servicelist.forEach((service) => {
          if (!this.userservicelist.includes(service))
            this.$services.RDS.sendService(service);
        });
        this.$services.RDS.requestUserServiceList();
      },
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
      return this.selectedItems.length === this.servicelist.length;
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
  beforeMount() {
    this.$services.RDS.requestServiceList();
    this.$services.RDS.requestUserServiceList();
  },
  methods: {
    toggle() {
      this.$nextTick(() => {
        if (this.selectedAllItems) {
          this.selectedItems = [];
        } else {
          this.selectedItems = this.servicelist.slice();
        }
      });
    },
    resetSelection() {
      this.$nextTick(() => {
        this.selectedItems = this.activatedItems;
      });
    },
    saveSelection() {
      if (this.selectedItems.length == 0) {
        // change text
      }
      this.activatedItems = this.selectedItems;
    },
  },
};
</script>
<template>
  <div class="help">
    <Frame source="https://www.research-data-services.de">
      <translate>
        Confirm the checkbox and click the button to remove the RDS account.
      </translate>

      <v-container fluid>
        <v-row>
          <v-spacer />
          <v-col md="2" class="d-flex align-center">
            <v-checkbox
              v-model="checked"
              :label="
                $gettext('Yes, i confirm that i want to delete my RDS account.')
              "
            />
          </v-col>
          <v-col md="2" class="d-flex align-center">
            <v-btn @click="uninstallRDS" :disabled="!checked" color="error">
              <translate>Delete RDS account</translate>
            </v-btn>
          </v-col>
          <v-spacer />
        </v-row>
      </v-container>
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
      checked: false,
      gettingStarted: "https://localhost:8000",
    };
  },
  methods: {
    uninstallRDS() {
      this.$store.dispatch(
        "removeService",
        this.getInformations("port-owncloud")
      );
      this.$store.commit("setWizardFinished", { wizard: false });
      this.$router.push({ name: "Wizard" });
    },
  },
};
</script>

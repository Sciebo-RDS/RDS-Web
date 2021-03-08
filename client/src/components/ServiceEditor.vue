<template>
  <div>
    <v-card>
      <v-card-title v-translate>Manage your access to services</v-card-title>

      <v-tabs>
        <v-tab>
          <v-icon left> mdi-account </v-icon>
          <translate>Informations</translate>
        </v-tab>
        <v-tab>
          <v-icon left>mdi-plus-circle</v-icon>
          <translate>Add service</translate>
        </v-tab>
        <v-tab v-if="filteredUserService.length > 0">
          <v-icon left> mdi-minus-circle </v-icon>
          <translate>Remove service</translate>
        </v-tab>

        <v-tab-item>
          <v-card flat>
            <v-card-text>
              <p>
                <translate>
                  In this card, you manage your access to services via RDS.
                </translate>
              </p>
              <p>
                <translate>
                  If you want to remove all access in once or remove the access
                  for your ownCloud account, click the "revoke button".
                </translate>
              </p>
            </v-card-text>
          </v-card>
          <v-card class="d-flex justify-end">
            <RevokeButton />
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-container flex>
            <v-row justify="start">
              <v-col v-for="(service, index) in filteredServices" :key="index">
                <v-card class="mb-12 pa-2" max-width="500">
                  <v-container>
                    <v-row>
                      <v-col>
                        <translate
                          :translate-params="{
                            name: parseServicename(service.servicename),
                          }"
                        >
                          Connect your %{name} account with RDS
                        </translate>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-btn color="primary" @click="grantAccess(service)">
                          <translate>Grant access</translate>
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-tab-item>
        <v-tab-item v-if="filteredUserService.length > 0">
          <v-container flex>
            <v-row>
              <v-col
                v-for="(service, index) in filteredUserService"
                :key="index"
              >
                <v-card class="mb-12 pa-2" max-width="500">
                  <v-container>
                    <v-row>
                      <v-col>
                        <translate
                          :translate-params="{
                            name: parseServicename(service.servicename),
                          }"
                        >
                          Delete %{name} from your account.
                        </translate>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-btn color="error" @click="removeAccess(service)">
                          <translate>Remove access</translate>
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-tab-item>
      </v-tabs>
    </v-card>
    <v-dialog
      v-model="overlay"
      persistent
      max-width="500px"
      :z-index="zIndex"
      @keydown.esc="overlay = false"
    >
      <v-card shaped outlined raised>
        <CredentialsInput
          ref="credinput"
          :showUsername="username"
          :showPassword="password"
          :servicename="servicename"
          :visible="overlay"
          v-on:closecredentials="overlay = false"
        />
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import CredentialsInput from "@/components/CredentialsInput";
import { mapState } from "vuex";
import RevokeButton from "@/components/RevokeButton.vue";

export default {
  components: { CredentialsInput, RevokeButton },
  computed: {
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
      servicelist: (state) => state.RDSStore.servicelist,
    }),
    filteredServices() {
      return this.excludeServices(this.servicelist, this.userservicelist);
    },
    filteredUserService() {
      return this.excludeServices(this.userservicelist, [
        {
          servicename: "port-owncloud",
        },
      ]);
    },
  },
  data: () => ({
    popup: undefined,
    overlay: false,
    username: "",
    password: "",
    servicename: "",
    zIndex: 1000,
  }),
  methods: {
    grantAccess(service) {
      if (!service.credentials) {
        this.openPopup(service, this);
      } else {
        this.servicename = service.servicename;
        this.username = service.credentials.userId;
        this.password = service.credentials.password;
        this.overlay = true;
      }
    },
    removeAccess(service) {
      console.log(service);
      this.$store.dispatch("removeService", service);
    },
  },
};
</script>
<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <translate>
          Enter your credentials for %{ parsedServicename }.
        </translate>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
          v-if="showUsername"
          v-model="username"
          :rules="rules"
          :label="$gettext(`Username`)"
          @keydown.enter="saveCredentials"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
          ref="passwordInput"
          v-if="showPassword"
          v-model="password"
          :rules="rules"
          :label="$gettext(`Password`)"
          @keydown.enter="saveCredentials"
        >
        </v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn @click="saveCredentials" color="primary">
          <translate>Save credentials</translate>
        </v-btn>
      </v-col>
      <v-col>
        <v-btn @click="$emit('closecredentials')" color="error">
          <translate>Cancel input</translate>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    showUsername: Boolean,
    showPassword: Boolean,
    servicename: String,
  },

  data: () => ({
    rules: [
      (value) => !!value || "Required.",
      (value) => (value && value.length >= 3) || "Min 3 characters",
    ],
    username: "",
    password: "",
  }),
  computed: {
    parsedServicename() {
      return this.parseServicename(this.servicename);
    },
  },
  methods: {
    checkInputs() {
      if (!this.showUsername && !this.showPassword) {
        this.saveCredentials();
      }
    },
    saveCredentials() {
      this.$requests.RDS.addServiceWithCredentials({
        username: this.username,
        password: this.password,
        servicename: this.servicename,
      });
      this.$emit("closecredentials");
    },
  },
};
</script>
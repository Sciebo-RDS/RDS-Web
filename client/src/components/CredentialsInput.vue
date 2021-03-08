<template>
  <v-container fluid>
    <v-row><v-col class="headline" translate>Add server</v-col></v-row>
    <v-row>
      <v-col>
        <div v-show="noInput">
          <translate>
            The service %{ parsedServicename } does not need any inputs, because
            it can inherate the credentials on another way.
          </translate>
        </div>
        <div v-show="!noInput">
          <translate>
            Enter your credentials for %{ parsedServicename }.
          </translate>
        </div>
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
          :append-icon="passwordShow ? 'mdi-eye' : 'mdi-eye-off'"
          :type="passwordShow ? 'text' : 'password'"
          @click:append="passwordShow = !passwordShow"
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
    visible: Boolean,
  },
  data: () => ({
    rules: [
      (value) => !!value || "Required.",
      (value) => (value && value.length >= 3) || "Min 3 characters",
    ],
    username: "",
    password: "",
    passwordShow: false,
  }),
  computed: {
    parsedServicename() {
      return this.parseServicename(this.servicename);
    },
    noInput() {
      return !this.showUsername && !this.showPassword;
    },
  },
  methods: {
    checkInputs() {
      if (!this.showUsername && !this.showPassword) {
        this.saveCredentials();
      }
    },
    saveCredentials() {
      this.$store.dispatch("addServiceWithCredentials", {
        username: this.username,
        password: this.password,
        servicename: this.servicename,
      });
      this.$emit("closecredentials");
    },
  },
};
</script>
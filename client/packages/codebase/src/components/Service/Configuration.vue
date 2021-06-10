<template>
  <v-container>
    <v-row>
      <v-col md="8" sm="12" xs="12">
        <v-card flat>
          <v-card-title>{{ service.name }}</v-card-title>
          <v-card-subtitle v-show="!!service.infoUrl || !!service.helpUrl">
            <a
              :href="service.infoUrl"
              target="_blank"
              class="text-decoration-none"
              v-show="!!service.infoUrl"
            >
              <translate>
                Website
              </translate>
            </a>
            <v-spacer v-show="!!service.infoUrl && !!service.helpUrl" />
            <a
              :href="service.infoUrl"
              target="_blank"
              class="text-decoration-none"
              v-show="!!service.helpUrl"
            >
              <translate>
                Help
              </translate>
            </a>
          </v-card-subtitle>
          <v-card-text class="respect-linebreak">
            {{ service.description[this.$config.language] }}
          </v-card-text>
        </v-card>
      </v-col>
      <v-col md="4">
        <v-card flat>
          <v-card-actions>
            <v-col class="text-right">
              <v-btn @click="1" color="warning" v-if="!!service.state">
                <v-icon class="mr-2">mdi-link-variant-off</v-icon>
                <translate class="mr-1">
                  Disconnect
                </translate>
                {{ service.name }}
              </v-btn>
              <v-btn @click="grantAccess(service)" color="primary" v-else>
                <v-icon class="mr-2">mdi-link-variant</v-icon>
                <translate class="mr-1">
                  Connect
                </translate>
                {{ service.name }}
              </v-btn>
            </v-col>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: ["service"],
  methods: {},
};
</script>

<style>
.respect-linebreak {
  white-space: pre-line;
}
</style>

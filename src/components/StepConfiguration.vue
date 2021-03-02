<template>
    <v-container>
        <v-card flat >
            <v-card-title>What and where to publish?</v-card-title>
            <v-card-subtitle>Please select the services you want to publish to: </v-card-subtitle>
            <v-card-text>
                        <!--<p>{{ selected }}</p>-->
                        <v-checkbox
                        v-model="selected"
                        label="reva"
                        value="port-reva"
                        ></v-checkbox>
                        <v-checkbox
                        v-model="selected"
                        label="datasafe"
                        value="port-datasafe"
                        ></v-checkbox>
                        <v-checkbox
                        v-model="selected"
                        label="zenodo"
                        value="port-zenodo"
                        ></v-checkbox>
            </v-card-text>
            <v-card-actions><v-btn>Select Folder</v-btn> </v-card-actions>
            <v-card-subtitle style="padding-top:0px">Current Folder: /path/to/current/folder</v-card-subtitle>
            
        </v-card>
    </v-container>
</template>

<script>
  export default {
    data () {
      return {
        selected: [],
      }
    },
  }
</script>
<template>
    <div>
        <!-- white in production-->
        <v-container class="grey lighten-5">
            <v-row>
            <v-col>
      <ProjectStepper />
            </v-col>
            </v-row>
            
            <v-row align-content="end" justify="space-around">
                <v-col cols="auto" class="mr-auto"/>
<v-col cols="auto">
                <v-btn tile color="error" >delete project</v-btn>
</v-col>
            </v-row>
  </v-container>
</div>
</template>

<script>
import ProjectStepper from "./ProjectStepper"
export default {
    components: {
        ProjectStepper
    }
}
</script>
<template>
    <div>
        <!-- white in production-->
        <v-container class="grey lighten-5"> 

      <ProjectStepper />
    
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
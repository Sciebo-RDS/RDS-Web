<template>
    <div>
        <v-container>
            <v-row>
                <v-col>
                    <ProjectStepper :project="project" />
                </v-col>
            </v-row>
            
            <v-row align-content="end" justify="space-around">
                <v-col cols="auto" class="mr-auto"/>
                <v-col v-if="project.status != '3' && project.status != '4'" cols="auto">
                    <v-btn tile color="error" @click="onDelete(project.researchId)">delete project</v-btn>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import ProjectStepper from "./ProjectStepper.vue"
export default {
    components: {
        ProjectStepper
    },
    props: ['project'],
    methods: {
        onDelete(id) {
            this.$emit('delete-project', id)
        }
    }
}
</script>
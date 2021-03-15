<template>
    <v-container>
        <v-card flat>
            <v-card-title>
                Publish your project
            </v-card-title>
            <v-card-subtitle>
                Make sure your settings are correct!
            </v-card-subtitle>
            <v-card-text>
                <!-- replace with logic-->
                PortIn: {{project.portIn[0].port}}<br>
                PortOut: {{project.portOut[0].port}}<br>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script>
export default {
    props: ['project'],
}
</script>
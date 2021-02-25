<template>
    <v-row justify="center">
      <v-expansion-panels inset focusable>
      <v-expansion-panel
        v-for="(item,i) in 5"
        :key="i"
        >
        <v-expansion-panel-header> Project {{ item }} </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ProjectSetting></ProjectSetting>
        </v-expansion-panel-content>
      </v-expansion-panel>
      </v-expansion-panels>
    </v-row>
</template>

<style lang="scss">

.v-expansion-panel-content__wrap {
  padding: 16px 24px 16px !important;
}

</style>

<script>
import ProjectSetting from './ProjectSetting'

export default {
  components: {
    ProjectSetting
    }
}
</script>
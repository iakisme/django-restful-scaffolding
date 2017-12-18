<template lang="html">
  <v-app>
    <v-tabs fixed centered>
    <v-toolbar color="primary">
      <v-text-field
        solo
        label="Search"
        prepend-icon="search"
      ></v-text-field>
      <v-tabs-bar color="transparent" slot="extension" dark>
        <v-tabs-slider color="yellow"></v-tabs-slider>
        <v-tabs-item href="claimed">已认领</v-tabs-item>
        <v-tabs-item href="unclaimed">未认领</v-tabs-item>
      </v-tabs-bar>
    </v-toolbar>
    <v-tabs-items>
      <v-tabs-content id="claimed">已认领</v-tabs-content>
      <v-tabs-content id="unclaimed">未认领</v-tabs-content>
    </v-tabs-items>
  </v-tabs>
  </v-app>
</template>

<script>
import 'material-design-icons/iconfont/material-icons.css'

export default {
  name: 'Main'
}
</script>

<style lang="css">
</style>

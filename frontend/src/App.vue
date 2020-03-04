<template>
  <!-- <v-app :style="{background: $vuetify.theme.themes[theme].background}"> -->
  <v-app>
    <Navbar/>
    <v-content >
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import Navbar from './components/Navbar';

export default {
  name: 'App',

  components: {
    Navbar,
  },

  data: () => ({
    //
  }),
};
</script>

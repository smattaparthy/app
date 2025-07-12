<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" width="100">
    <h1>My Single Page App</h1>
    <DataDisplay />
  </div>
</template>

<script>
import DataDisplay from './components/DataDisplay.vue';

export default {
  name: 'App',
  components: {
    DataDisplay,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

<template>
  <div id="app">
    <img src="./assets/LicenseSysLogo.png" style="margin-bottom:10px">
    <router-view/>
  </div>
</template>


<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /*margin-top: 60px;*/
}

html,body,#app{
  height: 100%;
  margin: 0px;
}
</style>

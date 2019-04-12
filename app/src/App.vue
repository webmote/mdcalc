<template>
  <div id="app">
    <section>
      <nav>
        <a href="/" class="brand">
          <img src="./assets/logo.png" style="height: 5em; width: auto;">
        </a>
        <router-link to="/s">About</router-link>
      </nav>
    </section>
    <router-view/>
  </div>
</template>

<script>
import 'normalize.css'
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  /* margin-top: 60px; */
}
nav {
  height: 5em;
  background-color: #2c3e50;
}
</style>

<template>
  <div id="app">
    <section>
      <nav>
        <a href="/" class="brand">
          <img src="./assets/logo.png" style="height: 5em; width: auto;">
        </a>
        <div class="search-wrap">
          <div class="search-input">
            <button>q</button><input v-model="keyword" v-on="inputListeners" type="text" placeholder="Search QT or EKG"><button v-on:click="closeSearch" v-show="isShowSearch" class="close">x</button>
          </div>
        </div>
        <div class="menus-wrap"></div>
      </nav>
    </section>
    <div class="search-results-wrap" v-show="isShowSearch"></div>
    <router-view v-show="!isShowSearch"/>
  </div>
</template>

<script>
import 'normalize.css'
export default {
  name: 'App',
  data () {
    return {
      isShowSearch: false,
      keyword: null
    }
  },
  computed: {
    inputListeners: function () {
      var vm = this
      return Object.assign({}, this.$listeners, {
        input: function (event) {
          vm.$emit('input', event.target.value)
          vm.search(event.target.value)
        },
        focus: function (event) {
          vm.isShowSearch = true
        }
      })
    }
  },
  methods: {
    closeSearch: function (event) {
      this.isShowSearch = false
      this.keyword = null
    },
    search: function (keyword) {
      console.log(keyword)
    }
  }
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
  border-top: solid .2em #1BB193;
  border-bottom: solid 1px #f0f0f0;
  display: flex;
}
.brand {
  flex: 1 1 20%
}
.search-wrap {
  display: inline-block;
  flex: 1 1 60%;
}
.search-input {
  height: 3em;
  border: 1px solid #1BB193;
  margin-top: .8em;
  display: flex;
}
.search-input * {
  vertical-align: middle;
}
.search-input button {
  height: 100%;
  width: 3em;
  border: none;
  background-color: #F5BC17;
  color: white;
  flex-shrink: 0;
}
.search-input button.close {
  margin-right: .5em;
  margin-top: .55em;
  height: 2em;
  width: 2em;
  border-radius: 1em;
}
.search-input input {
  border: none;
  font-size: 1.6em;
  flex: auto;
  padding-left: .4em;
}
.menus-wrap {
  flex: 1 1 20%;
}
</style>

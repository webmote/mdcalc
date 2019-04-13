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
    <div class="search-results-wrap" v-show="isShowSearch">
      <div class="results">
        <section :key="s.key" v-for="s in ss">
          <h3><router-link v-on:click.native="closeSearch" :to="{ name: 'ss_info', params: { ssKey: s.key }}">{{s.name}}</router-link></h3>
        </section>
      </div>
      <div class="type">
        <button>Hot</button>
      </div>
    </div>
    <transition name="fade">
      <router-view v-show="!isShowSearch"/>
    </transition>
    <section>
      <footer></footer>
    </section>
  </div>
</template>

<script>
import { getSs } from '@/apis'
import 'normalize.css'
export default {
  name: 'App',
  data () {
    return {
      isShowSearch: false,
      keyword: null,
      ss: []
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
  mounted: function () {

  },
  methods: {
    closeSearch: function (event) {
      this.isShowSearch = false
      this.keyword = null
      this.ss = []
    },
    search: function (kw) {
      getSs(kw).then(res => {
        this.ss = res.data
      })
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
footer {
  margin-top: 2em;
  border-top: 1px solid #f0f0f0;
  height: 7em;
}
nav {
  height: 5em;
  border-top: solid .2em #1BB193;
  border-bottom: solid 1px #f0f0f0;
  display: flex;
}
.brand {
  flex: 1 1 20%;
  margin-left: 2em;
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
  margin-right: 2em;
}
.search-results-wrap {
  display: flex;
  min-height: 25em;
}
.search-results-wrap .results {
  flex: 1 1 60%;
  margin-left: 2em;
}
h3 a {
  text-decoration: none;
  color:#1BB193;
}
h3 a:hover {
  color:#2c3e50;
}
.search-results-wrap .type {
  flex: 1 1 40%;
  margin-right: 2em;
  margin-left: 1em;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>

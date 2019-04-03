<template>
  <div class="hello">
    <section :key="s.key" v-for="s in ss">
      <h1><router-link :to="{ name: 'ss_info', params: { ssKey: s.key }}">{{s.name}}</router-link></h1>
    </section>
  </div>
</template>

<script>
import { getHotSs } from '@/apis'
export default {
  name: 'home',
  data () {
    return {
      ss: []
    }
  },
  mounted: function () {
    this.getSs()
  },
  methods: {
    getSs: function () {
      getHotSs().then(res => {
        this.ss = res.data
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

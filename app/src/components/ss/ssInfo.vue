<template>
  <div class="ss">
    <h1>{{ss.name}}</h1>
    <p v-show="ss.note">{{ss.note}}</p>
    <section v-for="i in ss.items" :key="i.key">
      <div>
        <div>
          <label>{{i.name}}</label>
        </div>
        <div>
          <button v-show="i.options&&i.options.length>0" v-for="o in i.options" :key="o.key">{{o.name}}</button>
        </div>
      </div>
    </section>
    <hr>
    <section v-for="f in ss.formulas" :key="f.key">
      <div>
        <label>{{f.name}}</label>
      </div>
    </section>
  </div>
</template>

<script>
import { getInfoSs } from '@/apis'
export default {
  name: 'ss_info',
  data () {
    return {
      ss: null
    }
  },
  mounted: function () {
    this.getSs(this.$route.params.ssKey)
  },
  methods: {
    getSs: function (ssKey) {
      getInfoSs(ssKey).then(res => {
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

<template>
  <div class="ssInput">
    <div v-if="ss.options&&ss.options.length>0">
      <button v-bind:value="o.key" v-bind:class="classOpiton" v-for="o in ss.options" v-bind:key="o.key" v-on="optionListeners">{{o.name}}</button>
    </div>
    <div v-else>
      <input v-bind="$attrs" v-bind:value="value" type="text" v-on="inputListeners">
      <button v-if="ss.unit">{{ss.unit}}</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SsInput',
  model: {
    prop: 'value',
    event: 'input'
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    ss: {
      type: Object,
      default: function () {
        return {}
      }
    }
  },
  computed: {
    classOpiton: function (o) {
      return {
        active: this.value === o.key
      }
    },
    optionListeners: function () {
      var vm = this
      return Object.assign({}, this.$listeners, {
        click: function (event) {
          vm.$emit('input', event.target.value)
        }
      })
    },
    inputListeners: function () {
      var vm = this
      return Object.assign({}, this.$listeners, {
        input: function (event) {
          vm.$emit('input', event.target.value)
        }
      })
    }
  },
  mounted: function () {
  },
  methods: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

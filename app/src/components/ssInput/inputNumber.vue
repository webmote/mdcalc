<template>
  <div class="input-number">
    <input v-bind="$attrs" v-bind:value="value" type="text" v-on="inputListeners">
  </div>
</template>

<script>
export default {
  name: 'inputNumber',
  model: {
    prop: 'value',
    event: 'input'
  },
  props: {
    value: Number
  },
  computed: {
    inputListeners: function() {
      var vm = this
      return Object.assign({},this.$listeners,{
        input: function(event) {
          vm.$emit('input', event.target.value)
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

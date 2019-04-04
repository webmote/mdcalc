<template>
  <div class="ssInput">
    <div v-if="ss.options&&ss.options.length>0">
      <button v-bind:value="o.key" v-bind:class="{active: value == o.key}" v-for="o in ss.options" v-bind:key="o.key" v-on="optionListeners">{{o.name}}</button>
    </div>
    <div v-else>
      <input v-bind="$attrs" v-bind:value="value" type="text" v-on="inputListeners">
      <button v-bind:value="unit.unit" v-bind:unit="unit.unit" v-if="unit.unit" v-on="unitListeners">{{unit.unit}}</button>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { unitConvert } from '@/utils/convert'
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
    convert: {
      type: Object,
      default: function () {
        return {}
      }
    },
    unit: {
      type: Object,
      default: function () {
        return {}
      }
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
    },
    unitListeners: function () {
      var vm = this
      return Object.assign({}, this.$listeners, {
        click: function (event) {
          var unit = event.target.value
          if (vm.unit.units && vm.unit.units.length > 1) {
            var unitSize = vm.unit.units.length
            var index = _.indexOf(vm.unit.units, unit)
            var nextIndex = index + 1
            if (nextIndex >= unitSize) {
              nextIndex = 0
            }
            var nextUnit = vm.unit.units[nextIndex]
            var newValue = unitConvert(unit + '-' + nextUnit, vm.value, vm.convert)
            if (newValue !== undefined) {
              vm.unit['unit'] = nextUnit
              vm.$emit('input', '' + newValue)
            }
          }
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.active {
  border-color: #2c3e50;
  background-color: #2c3e50;
  color: #fff;

}
</style>

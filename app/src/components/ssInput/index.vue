<template>
  <div>
    <div class="input-options" v-bind:class="{wrap: ss.options&&ss.options.length>3}" v-if="ss.options&&ss.options.length>0">
      <button tabindex="-1" v-bind:value="o.key" v-bind:class="{active: value == o.key}" v-for="o in ss.options" v-bind:key="o.key" v-on="optionListeners">{{o.name}}</button>
    </div>
    <div class="input" v-else>
      <input v-bind="$attrs" v-bind:tabindex="index" v-bind:value="value" type="text" v-on="inputListeners">
      <button tabindex="-1" v-bind:value="unit.unit" v-bind:unit="unit.unit" v-if="unit.unit" v-on="unitListeners">{{ unit.units && unit.units.length>0 ? '⇌&nbsp;'+unit.unit:unit.unit}}</button>
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
    index: { Number },
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
.input, .input-options {
  min-width: 20em;
  display: flex;
}
.input {
  border: 1px solid #1BB193;
}
.input input {
  /* width: 20em; */
  flex: 1 1 auto;
  border: none;
  padding: .2em;
  height: 1.5em;
}
.input button {
  flex: 0 0 auto;
  border: none;
  background-color: #1BB193;
  color: white;
}
.input-options {
  flex-wrap: wrap;
}
.input-options button {
  flex-grow: 1;
  line-height: 2em;
  border: solid 1px #ccc;
  background-color: #f0f0f0;
  color: #323232;
  margin-right: -1px;
}
.input-options button:last-child {
  margin-right: 0;
}
.input-options button.active {
  border: 1px solid #1BB193;
  background-color: #1BB193;
  color: white;
}
.wrap {
  flex-direction: column;
}
.wrap button {
  margin-bottom: -1px;
  margin-right: 0;
  text-align: left;
}
.wrap button:last-child {
  margin-bottom: 0;
}
</style>

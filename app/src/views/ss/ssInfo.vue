<template>
  <div class="ss">
    <h1>{{ss.name}}</h1>
    <p v-show="ss.note">{{ss.note}}</p>
    <div class="items">
      <section v-show="!i.when||(i.when&&model[i.when]===i.when_eq)" v-for="i in ss.items" :key="i.key">
        <div class="row">
          <div class="label">
            <label>{{i.name}}</label><span class="score" v-show="score[i.key]>0||score[i.key]<0">{{score[i.key]}}</span>
          </div>
          <div class="input">
            <ss-input v-model="model[i.key]" :convert="ss.unit_convert" :unit="unit[i.key]" :ss="i"></ss-input>
          </div>
        </div>
      </section>
    </div>
    <section v-for="(f, k) in result" :key="k">
      <div>
        <div>
        <label>{{f.name}}</label><strong :title="k" v-show="f.ret">{{f.ret}}</strong>
        </div>
        <p v-show="f.result">{{f.result}}</p>
      </div>
    </section>
  </div>
</template>

<script>
import { getInfoSs } from '@/apis'
import _ from 'lodash'
import SsInput from '@/components/ssInput'
import { unitConvert } from '@/utils/convert'
export default {
  name: 'ss_info',
  components: {
    SsInput
  },
  data () {
    return {
      ss: {},
      model: {},
      unit: {},
      score: {},
      result: {}
    }
  },
  watch: {
    model: {
      handler: function (val, oldVal) {
        if (!_.isEmpty(val)) {
          this.emitScore()
        }
      },
      deep: true
    }
  },
  mounted: function () {
    this.getSs(this.$route.params.ssKey)
  },
  methods: {
    emitScore: function () {
      _.each(this.model, this.calcScore)
      var values = _.values(this.model)
      if (_.indexOf(values, null, '') < 0) {
        this.calcFormulas()
      }
    },
    calcScore: function (val, key) {
      var item = _.find(this.ss.items, {key: key})
      if (item) {
        if (item.when && item.when_eq) {
          var isEq = (this.model[item.when] === item.when_eq)
          if (!isEq) {
            this.score[key] = 0
            val = null
            this.model[key] = val
          }
        }
        if (item.scores && val) {
          var ret = this.chooseScore(val, key, item.scores)
          // console.log(ret)
          if (ret && ret.score) {
            if (/^[0-9.]*$/.test(ret.score)) {
              this.score[key] = _.toNumber(ret.score || ret.value || val)
            } else {
              console.info(key, ret.score)
              this.score[key] = eval(ret.score.replace('this', val).replace('value', val))
            }
          } else {
            // console.log(ret)
            this.score[key] = null
          }
        }
      }
    },
    chooseScore: function (val, key, scores) {
      // 优先相等和正则匹配
      var score = _.find(scores, o => {
        var value = o.value
        if (value === val) { // eq 相等
          return true
        } else if ((new RegExp(value)).test(val)) { // regexp 正则匹配
          return true
        }
      })
      if (score) {
        return score
      }
      return _.find(scores, o => {
        var value = o.value.replace('–', '-')
        // range 范围
        // < ≤ -< | > ≥ >- | -
        const symbol = {
          gt: '>',
          gte: '>=',
          lt: '<',
          lte: '<=',
          eq: '=',
          range: '-'
        }
        const rangeRegExp = /(\d+\.?\d{0,3})?(<|>|≤|≥)?(-)?(<|>|≤|≥)?(\d+\.?\d{0,3})/
        var matchs = value.match(rangeRegExp)
        if (!matchs) {
          console.info(value, matchs)
        }
        var range = {
          check: function () {
            var c = []
            // sn start number
            // en end number
            // sw start way
            // ew end way
            if (this.sn && this.sw) {
              c.push('value')
              c.push(this.sw)
              c.push(this.sn)
              if (this.en && this.ew) {
                c.push('&&')
                c.push('value')
                c.push(this.ew)
                c.push(this.en)
              }
            } else if (this.en && this.ew) {
              c.push('value')
              c.push(this.ew)
              c.push(this.en)
            } else if (this.en && this.sw) {
              c.push('value')
              c.push(this.sw)
              c.push(this.en)
            }
            return c.join(' ').replace('≥', symbol.gte).replace('≤', symbol.lte)
          }
        }
        if (matchs[1]) {
          range['sn'] = matchs[1]
        }
        if (matchs[5]) {
          range['en'] = matchs[5]
        }
        if (matchs[3] && (matchs[3] === symbol.range || matchs[3] === symbol.eq)) {
          range['r'] = true
          if (matchs[2] && matchs[2] === symbol.gt) {
            range['sw'] = symbol.gt
          } else {
            range['sw'] = symbol.gte
          }
          if (matchs[4] && matchs[4] === symbol.lt) {
            range['ew'] = symbol.lt
          } else {
            range['ew'] = symbol.lte
          }
        } else {
          if (matchs[2]) {
            range['sw'] = matchs[2]
          }
          if (matchs[4]) {
            range['ew'] = matchs[4]
          }
        }
        var jsValue = o['js_value'] = range.check()
        jsValue = _.replace(jsValue, new RegExp('value', 'g'), val)
        // TODO other and model eq
        console.log(range, jsValue)
        return eval(jsValue)
      })
    },
    calcFormulas: function () {
      _.each(this.ss.formulas, this.calcFormula)
    },
    calcFormula: function (formula) {
      var vm = this
      const key = formula.key
      var jsFormula = formula.js_formulas
      _.each(this.model, function (val, key) {
        // 转换计算单位
        if (_.has(vm.unit, key)) {
          var vUnit = vm.unit[key].unit
          var cUnit = formula.calc_unit[key]
          if (vUnit !== cUnit) {
            val = unitConvert(vUnit + '-' + cUnit, val, vm.ss.unit_convert)
          }
        }
        jsFormula = _.replace(jsFormula, new RegExp(key, 'g'), val)
      })
      console.info(key, jsFormula)
      var value = eval(jsFormula)
      value = Math.floor(value * 100) / 100 // 保留两位小数点
      if (formula.scores) {
        var ret = this.chooseScore(value, key, formula.scores)
        if (ret) {
          this.result[key] = _.assign({ret: value}, _.pick(formula, ['key', 'name', 'unit']), ret)
        } else {
          this.result[key] = _.assign({ret: value}, _.pick(formula, ['key', 'name', 'unit']), ret)
        }
      } else {
        this.result[key] = _.assign({ret: value}, _.pick(formula, ['key', 'name', 'unit']))
      }
    },
    getSs: function (ssKey) {
      getInfoSs(ssKey).then(res => {
        this.ss = res.data
        if (this.ss && this.ss.items) {
          var model = {}
          var unit = {}
          this.ss.items.map(i => {
            model[i.key] = null
            unit[i.key] = _.pick(i, ['unit', 'units'])
          })
          this.model = model
          this.unit = unit
          var result = {}
          this.ss.formulas.map(i => {
            result[i.key] = _.pick(i, ['key', 'name', 'unit'])
          })
          this.result = result
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.items {
  margin-bottom: 2em;
  margin-top: 2em;
}
.items section {
  border-top: 1px solid #f0f0f0;
}
.items section:last-child {
  border-bottom: 1px solid #f0f0f0;
}
.row {
  display: block;
  padding: .5em;
  position: relative;
  text-align: left;
}
.row::after {
  clear: both;
  content: "";
  display: block;
}
.row::before {
  clear: both;
  content: "";
  display: block;
}
.row .label {
  min-width: 16em;
  text-align: left;
  display: inline-block;
}
.row .input {
  top: 0;
  float: right;
  text-align: right;
  margin-left: 17em;
}
.row .input button {
  display: inline-block;
}
.label .score {
  float: right;
  color: brown;
}
</style>

<template>
  <div class="ss-info">
    <div class="ss">
      <h1>{{ss.name}}</h1>
      <p v-show="ss.note">{{ss.note}}</p>
      <div class="items">
        <section v-show="!i.when||(i.when&&model[i.when]===i.when_eq)" v-for="(i, index) in ss.items" :key="i.key">
          <div class="row">
            <div class="label-wrap">
              <label>{{i.name}}</label><span class="score" v-show="score[i.key]>0||score[i.key]<0">{{score[i.key]}}</span>
            </div>
            <div class="input-wrap">
              <ss-input v-model="model[i.key]" :index="index + 1" :convert="ss.unit_convert" :unit="unit[i.key]" :ss="i"></ss-input>
            </div>
          </div>
        </section>
      </div>
      <div class="results">
        <section v-bind:class="resultClassObject">
          <div class="box" v-for="(f, k) in result" :key="k">
            <div>
              <div class="result">
                <div>
                  <strong class="score_num" :title="k" v-show="f.ret">{{f.ret}}</strong><label class="score_label" v-show="f.ret">{{f.name}}</label>
                </div>
                <div>
                  <span v-show="f.ret && typeof(f.result) == 'string' ">{{f.result || f.note}}</span>
                </div>
                <div v-show="!f.ret">
                  <strong class="score_num">Results:</strong>
                </div>
                <div v-show="!f.ret">
                  <label>&nbsp;</label>
                </div>
              </div>
              <div class="type" v-if="typeof(f.result) == 'object'">
                <div v-for="r in f.result" :key="r.type">
                  <label>{{r.type_name}}</label>
                  <strong>{{r.score}}</strong>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
    <div class="info"></div>
  </div>
</template>

<script>
import { getInfoSs } from '@/apis'
import _ from 'lodash'
import SsInput from '@/components/ssInput'
import { unitConvert } from '@/utils/convert'
import { NUMBER_REG, CALC_REG } from '@/utils/regexp'
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
    '$route': 'fatchData',
    model: {
      handler: function (val, oldVal) {
        // TODO change key $emit 延后执行
        if (!_.isEmpty(val)) {
          this.emitScore()
        }
      },
      deep: true
    }
  },
  computed: {
    resultClassObject: function () {
      var obj = {}
      var keys = _.keys(this.result)
      obj['col-' + keys.length + '-row'] = true
      return obj
    }
  },
  mounted: function () {
    this.fatchData()
  },
  methods: {
    fatchData: function () {
      this.getSs(this.$route.params.ssKey)
    },
    emitScore: function () {
      _.each(this.model, this.calcScore)
      var values = _.values(this.model)
      if (_.indexOf(values, null, '') < 0) {
        this.calcFormulas()
      }
    },
    calcScore: function (val, key) {
      var item = _.find(this.ss.items, {key: key})
      var score = 0
      var del = false
      if (item) {
        // when_eq
        if (item.when && item.when_eq) {
          var isEq = (this.model[item.when] === item.when_eq)
          if (!isEq) {
            val = null
            delete this.model[key]
          }
        }
        if (item.scores && val) {
          var ret = this.chooseScore(val, key, item.scores)
          // console.log(ret)
          if (ret && ret.score) {
            if (NUMBER_REG.test(ret.score)) {
              score = _.toNumber(ret.score || ret.value || val)
            } else {
              // TODO eval
              console.debug(key, ret.score)
              if (CALC_REG.test(ret.score)) {
                score = eval(ret.score.replace('this', val).replace('value', val))
              } else {
                score = parseInt(ret.score)
              }
            }
          }
        } else {
          del = true
        }
      }
      this.score[key] = score
      if (del) {
        delete this.score[key]
      }
    },
    chooseScore: function (val, key, scores) {
      const vm = this
      var scoreCheck = []
      var score = _.filter(scores, o => {
        var jsCheck
        if (NUMBER_REG.test('' + val) === false) {
          // console.log('not number', key, val, NUMBER_REG.test('' + val))
          var check = []
          if (_.has(o, 'js_reg_check')) {
            check.push('(' + o.js_reg_check + ')')
          }
          if (_.has(o, 'js_eq_check')) {
            check.push('(' + o.js_eq_check + ')')
          }
          jsCheck = check.join(' || ')
        } else {
          if (_.has(o, 'js_check')) {
            jsCheck = o.js_check
          } else {
            console.warn(key, 'no js_check')
          }
        }
        // console.debug(key, jsCheck)
        jsCheck = _.replace(jsCheck, new RegExp('value', 'g'), val)
        _.each(vm.model, (value, key) => {
          if (!NUMBER_REG.test(value)) {
            jsCheck = _.replace(jsCheck, new RegExp('\'' + key + '\'', 'g'), '\'' + value + '\'')
          } else {
            jsCheck = _.replace(jsCheck, new RegExp(key, 'g'), value)
          }
        })
        // console.debug(key, jsCheck)
        var bool = eval(jsCheck)
        if (bool) {
          scoreCheck.push(jsCheck)
        }
        return bool
      })
      if (score) {
        if (score.length === 1) {
          score = score[0]
        }
        console.debug('check:', key, scoreCheck, score)
      } else {
        console.warn('check:', key, scoreCheck)
      }
      return score
    },
    calcFormulas: function () {
      _.each(this.ss.formulas, this.calcFormula)
    },
    calcFormula: function (formula) {
      var vm = this
      const key = formula.key
      const calcKeys = _.keys(this.model)
      var jsFormula = formula.js_formulas
      if (jsFormula === '+') { // all count
        jsFormula = calcKeys.join(' + ')
      }
      // replace key->value
      _.each(calcKeys, function (key) {
        // 分值转换
        var val = vm.model[key]
        if (_.has(vm.score, key)) {
          val = vm.score[key]
        }
        // 换算单位
        if (_.has(vm.unit, key) && _.has(formula, 'calc_unit') && _.has(formula.calc_unit, key)) {
          var vUnit = vm.unit[key].unit
          var cUnit = formula.calc_unit[key]
          if (vUnit !== cUnit) {
            val = unitConvert(vUnit + '-' + cUnit, val, vm.ss.unit_convert)
          }
        }
        jsFormula = _.replace(jsFormula, new RegExp(key, 'g'), val)
      })

      console.debug(key, jsFormula)
      var value = eval(jsFormula)
      var ret
      value = Math.floor(value * 100) / 100 // 保留两位小数点
      if (formula.scores) {
        ret = this.chooseScore(value, key, formula.scores)
      }
      var baseResult = _.pick(formula, ['key', 'name', 'unit', 'note'])
      if (_.isArray(ret) && ret.length > 0) {
        this.result[key] = _.assign({ret: value}, baseResult)
        var rs = []
        _.each(ret, r => {
          rs.push(_.pick(r, ['type', 'type_name', 'score', 'result']))
        })
        this.result[key]['result'] = rs
      } else {
        this.result[key] = _.assign({ret: value}, baseResult, ret)
      }
    },
    getSs: function (ssKey) {
      getInfoSs(ssKey).then(res => {
        this.ss = res.data
        if (this.ss && this.ss.items) {
          var model = {}
          var unit = {}
          this.ss.items.map(i => {
            if (!_.has(i, 'when_eq')) {
              model[i.key] = null
            }
            unit[i.key] = _.pick(i, ['unit', 'units'])
          })
          this.model = model
          this.unit = unit
          var result = {}
          this.ss.formulas.map(i => {
            result[i.key] = _.pick(i, ['key', 'name', 'unit', 'note'])
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
.ss-info {
  margin-left: 2em;
  margin-right: 2em;
  display: flex;
}
.ss {
  flex: 1 1 60%;
}
.info {
  flex: 1 1 40%;
}
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
.items section:nth-of-type(odd) {
  background-color: #f0f0f0;
  background-color: white;
}
.row {
  padding: .5em;
  position: relative;
  text-align: left;
  display: flex;
  line-height: 2em;
}
.row .label-wrap {
  flex: 1 1 50%;
}
.row .input-wrap {
  flex: 1 1 50%;
}
.row .input-wrap button {
  display: inline-block;
}
.label-wrap .score {
  color: brown;
  display: none;
}
.results section {
  display: flex;
}
.results .box {
  position: relative;
  display: inline-block;
  vertical-align: top;
  min-width: 10em;
  background-color: #2c3e50;
  color: #fff;
  height: 6em;
  border-right: 1px solid #45566A;
  border-left: 1px solid #45566A;
  margin-left: -1px;
  margin-right: -1px;
}
.results .box:last-child {
  border-right: none;
}
.results .box:first {
  border-left: none;
}
.results .box > div {
  padding: 1em;
}
.col-1-row .box {
  width: 100%;
}
.col-2-row .box {
  width: 50%;
}
.col-3-row .box {
  width: 33.33%;
}
.col-4-row .box {
  width: 25%;
}
.score_num {
  font-size: 2em;
  font-weight: bold;
}
.score_label {
  margin-left: .5em;
  font-size: .8em;
  color: #ccc;
}
.type div {
  display: inline-block;
  min-width: 10em;
}
</style>

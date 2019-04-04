import re
from .base import BaseModel
from mdcalc.utils import del_none

class SsModel(BaseModel):
    def list(self):
        c = self.db.cursor()
        c.execute("SELECT * FROM v_ss")
        ret = list(c.fetchall())
        c.close()
        return del_none(ret)
    
    def unit_convert(self):
        c = self.db.cursor()
        c.execute("SELECT key,name,norm FROM keys WHERE type='unit'")
        ret = del_none(c.fetchall())
        # m: 1m=100cm to value * 100
        units = {}
        for u in ret:
            if 'norm' in u and u['norm']:
                norm = u['norm'] # 1m=10dm,1m=100cm,1m=1000mm
                for n in str.split(norm, ','):
                    r = re.search(r'(\d+\.?\d{0,})([^=\n]*)=(\d+\.?\d{0,})([^\n]*)', n)
                    if r:
                        num1, unit1, num2, unit2 = r.groups()
                        if u['key'] == unit1:
                            units[unit1+'-'+unit2] = 'value * ' + str( float(num2) / float(num1) )
                        if u['key'] == unit2:
                            units[unit2+'-'+unit1] = 'value * ' + str( float(num1) / float(num2) )
        return units
    
    def info(self, ss_key):
        c = self.db.cursor()
        where = (ss_key,)
        c.execute("SELECT * FROM v_ss WHERE key=? LIMIT 1", where)
        ret = del_none(c.fetchone())
        if not ret:
            return ret
        items = c.execute("SELECT * FROM v_items WHERE ss_key=?", where).fetchall()
        formulas = c.execute("SELECT * FROM v_formulas WHERE ss_key=?", where).fetchall()
        self.compile_calc_unit(formulas)
        self.set_scores(formulas)
        ret['items'] = self.compile_items(items)
        ret['formulas'] = del_none(formulas)
        ret['unit_convert'] = self.unit_convert()
        c.close()
        return ret
    
    def set_scores(self, items):
        for item in items:
            c = self.db.cursor()
            where = {'key':item['key'],'ss_key':item['ss_key']}
            scores = c.execute("SELECT value,score,type,type_name,result FROM v_scores WHERE ss_key=:ss_key and key=:key", where).fetchall()
            c.close()
            self.compile_scores_value(scores)
            if len(scores)>0:
                item['scores'] = del_none(scores)
        return items
    
    def js_check_value(self, value, score):
        check = []
        eq = self.js_eq_value(value)
        reg = self.js_regexp_value(value)
        rg = self.js_range_value(value)
        if reg:
            check.append("(%s)" % reg)
            score['js_reg_check'] = reg
        elif eq:
            check.append("(%s)" % eq)
            score['js_eq_check'] = eq
        if rg:
            check.append("(%s)" % rg)
            score['js_range_check'] = rg
        
        return " || ".join(check)
        
    def js_regexp_value(self, value):
        if '|' in value or '*' in value:
            return "(new RegExp('{val}')).test('value') ".format(val=value)
    
    def js_eq_value(self, value):
        if '=' in value:
            r = re.search(r'(.*)=(.*)', value)
            if r:
                k, v = r.groups()
                return "'{k}' == '{v}'".format(k=k, v=v)
        else:
            return "'value' == '{val}'".format(val=value)

    def js_range_value(self, value):
        r = re.search(r'^(\d+\.?\d{0,})?(<|>|≤|≥|gt|gte|lt|lte)?(-)?(<|>|≤|≥|gt|gte|lt|lte)?(\d+\.?\d{0,})$', value)
        if r:
            num1, rl1, rg, rl2, num2 = r.groups()
            c = []
            # print(value, r.groups())
            if num1 and num2:
                c.append('value')
                c.append('>' if rl1 else '>=')
                c.append(num1)
                c.append('&&')
                c.append('value')
                c.append('<' if rl2 else '<=')
                c.append(num2)
            elif num2 and rl2:
              c.append('value')
              c.append(rl2)
              c.append(num2)
            elif num2 and rl1:
              c.append('value')
              c.append(rl1)
              c.append(num2)
            rg = " ".join(c)
            rg = re.sub(r'gt',' >', rg)
            rg = re.sub(r'gte|≥', '>=', rg)
            rg = re.sub(r'lt', '<', rg)
            rg = re.sub(r'lte|≤', '<=', rg)
            return "{rg}".format(val=value, rg=rg)
    
    def compile_scores_value(self, scores):
        for score in scores:
            if 'value' in score and score['value']:
                value = score['value']
                value = value.replace('–', '-')
                if ' and ' in value or '&&' in value:
                    ands = []
                    for v in re.split(r' and |&&', value):
                        rg = self.js_check_value(v, score)
                        if rg:
                            ands.append("({rg})".format(rg=rg))
                    if 'js_reg_check' in score:
                        del score['js_reg_check']
                    if 'js_range_check' in score:
                        del score['js_range_check']
                    if 'js_eq_check' in score:
                        del score['js_eq_check']

                    score['js_and'] = True
                    score['js_check'] = " && ".join(ands)
                else:
                    score['js_check'] = self.js_check_value(value, score)

    def compile_calc_unit(self, items):
        for item in items:
            if 'calc_unit' in item and item['calc_unit']:
                calc_unit_str = item['calc_unit']
                calc_unit = {}
                for s in str.split(calc_unit_str, ','):
                    ku = str.split(s, ':')
                    calc_unit[ku[0]] = ku[1]
                if calc_unit:
                    item['calc_unit'] = calc_unit

    def compile_items(self, items):
        self.set_scores(items)
        for item in items:
            # units
            if 'units' in item and item['units']:
                item['units'] = str.split(item['units'], ',')
            # option
            options = [i for i in items if i['type']=='option' and i['p_key']==item['key']]
            if len(options)>0:
                item['options'] = del_none(options)
        for item in items:
            sub_items = [i for i in items if i['type']=='item' and i['p_key']==item['key']]
            if len(sub_items)>0:
                item['items'] = del_none(sub_items)
        first = [i for i in items if not i['p_key']]
        return del_none(first)
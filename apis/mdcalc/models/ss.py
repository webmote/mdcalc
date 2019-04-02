from .base import BaseModel
from mdcalc.utils import del_none

class SsModel(BaseModel):
    def list(self):
        c = self.db.cursor()
        c.execute("SELECT * FROM v_ss")
        ret = list(c.fetchall())
        return ret

    def info(self, ss_key):
        c = self.db.cursor()
        where = (ss_key,)
        c.execute("SELECT * FROM v_ss WHERE key=? LIMIT 1", where)
        ret = del_none(c.fetchone())
        items = c.execute("SELECT * FROM v_items WHERE ss_key=?", where).fetchall()
        formulas = c.execute("SELECT * FROM v_formulas WHERE ss_key=?", where).fetchall()
        self.set_scores(formulas)
        ret['items'] = self.compile_items(items)
        ret['formulas'] = del_none(formulas)
        return ret
    def set_scores(self, items):
        for item in items:
            c = self.db.cursor()
            where = {'key':item['key'],'ss_key':item['ss_key']}
            scores = c.execute("SELECT value,score,type,result FROM ss_scores WHERE ss_key=:ss_key and key=:key", where).fetchall()
            if len(scores)>0:
                item['scores'] = del_none(scores)
        return items
    def compile_items(self, items):
        self.set_scores(items)
        for item in items:
            options = [i for i in items if i['type']=='option' and i['p_key']==item['key']]
            if len(options)>0:
                item['options'] = del_none(options)
        for item in items:
            sub_items = [i for i in items if i['type']=='item' and i['p_key']==item['key']]
            if len(sub_items)>0:
                item['items'] = del_none(sub_items)
        first = [i for i in items if not i['p_key']]
        return del_none(first)
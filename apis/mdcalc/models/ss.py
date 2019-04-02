from .base import BaseModel
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
        ret = c.fetchone()
        return ret
class BaseModel(object):
    def __init__(self, *args, **kwargs):
        self.db = kwargs['db']
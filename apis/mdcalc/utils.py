def del_none(obj):
    if isinstance(obj, dict):
        for i,v in list(obj.items()):
            if not v:
                del obj[i]
    if isinstance(obj, list):
        for i in obj:
            del_none(i)
    return obj
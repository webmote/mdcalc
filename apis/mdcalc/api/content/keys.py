#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from sanic import Blueprint
from sanic.response import json
from mdcalc.db import db
keys = Blueprint('content_keys', url_prefix="/keys")

@keys.route('/')
async def keys_root(request):
    c = db.cursor()
    c.execute("select * from keys")
    return json(c.fetchall())

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from sanic import Blueprint
from sanic.response import json
from mdcalc.models.ss import SsModel
from mdcalc.db import db

model = SsModel(db=db)
ss = Blueprint('content_ss', url_prefix='/ss')

@ss.route('/', methods=['GET', 'OPTIONS'])
async def ss_list(request):
    return json(model.list())

@ss.route('/<ss_key>', methods=['GET', 'OPTIONS'])
async def ss_info(request, ss_key):
    return json(model.info(ss_key))
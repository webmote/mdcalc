#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
from sanic import Sanic
from sanic_cors import CORS

app = Sanic('MDCALC', load_env='MDCALC_')
CORS(app)
if os.getenv('MDCALC_CONFIGS'):
    app.config.from_envvar('MDCALC_CONFIGS')

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print('Server successfully started!')

@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('Server shutting down!')

from .api import api
app.blueprint(api)
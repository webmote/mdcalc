#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
from .app import app

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def db_setup(app):
    import sqlite3 as sqlite
    db_file = None
    if 'DB_FILE' in app.config:
        db_file = app.config.DB_FILE
    else:
        here = os.path.abspath(os.path.dirname(__file__))
        db_file = os.path.join(here,'ss.db')
    print(db_file)
    conn = sqlite.connect(db_file)
    conn.row_factory = dict_factory
    return conn
# make db
db = db_setup(app)

@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db = db
@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.db.close()
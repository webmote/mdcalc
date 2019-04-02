#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from sanic import Blueprint

from .keys import keys
from .ss import ss

content = Blueprint.group(keys, ss, url_prefix='/content')
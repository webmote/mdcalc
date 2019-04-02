#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from sanic import Blueprint

from .content import content

api = Blueprint.group(content, url_prefix='/api')
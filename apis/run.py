#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
here = os.path.abspath(os.path.dirname(__file__))
config = os.path.join(here, 'config')
print(config)
os.putenv('MDCALC_CONFIGS', config)
print(os.getenv('MDCALC_CONFIGS'))
from mdcalc import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

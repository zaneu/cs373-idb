#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Run the application with the following command:
# python wsgi.py
# Note that this must be run in a virtualenv (which is specified in
# requirements.txt)


import os

from FreeSpirits import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

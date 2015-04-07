#!/usr/bin/env bash
# this script setups a developer environment for the project
# run python wsgi.py and navigate to localhost:5000 to test
# the database should be generated in app.db

export PORT=5000

cd ..
python populate.py

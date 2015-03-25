# -*- coding: utf-8 -*-

from . import app
from flask import render_template


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/builder')
def builder():
    return render_template("builder.html")


# -*- coding: utf-8 -*-

from . import app
from flask import render_template


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/builder')
def builder():
    return render_template("builder.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/caribou-lou')
def ingredient():
    args = {
        "name": "Caribou Lou",
        "ingredients": ["Rum", "Vodka", "So forth"]
    }
    return render_template("ingredient.html", **args)

# -*- coding: utf-8 -*-

from . import app
from flask import render_template


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/builder')
def builder():
    return render_template("builder.html")

@app.route('/drinks/<drink>')
def drinks(drink):
    return render_template(drink + ".html")

@app.route('/ingredients/<ingredient>')
def ingredients(ingredient):
    return render_template(ingredient + ".html")

@app.route('/users/<username>')
def users(username):
    print(username)
    return render_template(username + ".html")

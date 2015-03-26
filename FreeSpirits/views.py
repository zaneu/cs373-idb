# -*- coding: utf-8 -*-

from . import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/builder')
def builder():
    return render_template("builder.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/drinks')
def drinks_listing():
    return render_template("drinks.html")
  
@app.route('/drinks/<drink>')
def drinks(drink):
    return render_template(drink + ".html")

@app.route('/ingredients')
def ingredients_listing():
    return render_template("ingredients.html")
  
@app.route('/ingredients/<ingredient>')
def ingredients(ingredient):
    return render_template(ingredient + ".html")

@app.route('/users')
def users_listing():
    return render_template("users.html")

@app.route('/users/<username>')
def users(username):
    return render_template(username + ".html")

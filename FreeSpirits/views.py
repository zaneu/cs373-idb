# -*- coding: utf-8 -*-

from . import app
from .models import *

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
@app.route('/drinks/<drink_id>')
def drinks(drink_id=None):
    if drink_id == None:
        return render_template("drinks.html", drinks=Drink.query.order_by(Drink.name))
    return render_template("drink.html", drink=Drink.query.filter_by(id=drink_id).first())

@app.route('/ingredients')
@app.route('/ingredients/<ingredient_id>')
def ingredients(ingredient_id=None):
    if ingredient_id is None:
        return render_template("ingredients.html", ingredients=Ingredient.query.order_by(Ingredient.name))
    return render_template("ingredient.html", ingredient=Ingredient.query.filter_by(id=ingredient_id).first())

@app.route('/users')
def users_listing():
    return render_template("users.html")

@app.route('/users/<username>')
def users(username):
    return render_template(username + ".html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

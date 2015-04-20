# -*- coding: utf-8 -*-

import subprocess
import os

from . import app
from .models import *

from flask import render_template
from flask import jsonify


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
    if drink_id is None:
        return render_template("drinks.html",
                               drinks=Drink.query.order_by(Drink.name))

    query = Drink.query.filter_by(id=drink_id)
    if query.first():
        quantities, ingredients = Drink.get_ingredients_by_id(drink_id)
        return render_template("drink.html",
                               drink=query.first(),
                               quantities=quantities,
                               ingredients=ingredients)
    else:
        return page_not_found(404)


@app.route('/ingredients')
@app.route('/ingredients/<ingredient_id>')
def ingredients(ingredient_id=None):
    if ingredient_id is None:
        return render_template("ingredients.html",
                               ingredients=Ingredient.query.
                               order_by(Ingredient.name))

    query = Ingredient.query.filter_by(id=ingredient_id)
    if query.first():
        drinks = Ingredient.get_drinks_by_id(ingredient_id, 5)
        return render_template("ingredient.html",
                               ingredient=query.first(),
                               drinks=drinks)
    else:
        return page_not_found(404)


@app.route('/users')
@app.route('/users/<user_id>')
def users(user_id=None):
    if user_id is None:
        return render_template("users.html",
                               users=User.query.order_by(User.name))

    query = User.query.filter_by(id=user_id)
    if query.first():
        return render_template("user.html", user=query.first())
    else:
        return page_not_found(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

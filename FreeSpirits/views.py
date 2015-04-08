# -*- coding: utf-8 -*-

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
@app.route('/drinks/')
@app.route('/drinks/<drink_id>')
def drinks(drink_id=None):
    if drink_id is None:
        return render_template("drinks.html", drinks=Drink.query.order_by(Drink.name))
    ingredients = []
    for ingredient in IngredientToDrink.query.filter_by(drink_id=drink_id):
        ingredients.append(ingredient.quantity + " " + Ingredient.query.filter_by(id=ingredient.ingredient_id).first().name)
    return render_template("drink.html", drink=Drink.query.filter_by(id=drink_id).first(), ingredients=ingredients)

@app.route('/ingredients')
@app.route('/ingredients/')
@app.route('/ingredients/<ingredient_id>')
def ingredients(ingredient_id=None):
    if ingredient_id is None:
        return render_template("ingredients.html", ingredients=Ingredient.query.order_by(Ingredient.name))
    return render_template("ingredient.html", ingredient=Ingredient.query.filter_by(id=ingredient_id).first())

@app.route('/users')
@app.route('/users/')
@app.route('/users/<user_id>')
def users(user_id=None):
    if user_id is None:
        return render_template("users.html", users=User.query.order_by(User.name))
    return render_template("user.html", user=User.query.filter_by(id=user_id).first())

@app.route('/api/drinks')
@app.route('/api/drinks/')
@app.route('/api/drinks/<drink_id>')
def api_drinks(drink_id=None):
    if drink_id is None:
        drinks_name = Drink.query.all().name
        drinks_id   = Drink.query.all().id
        drinks = dict(zip(drinks_name, drinks_id))
	return jsonify(**drinks)
    return None


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

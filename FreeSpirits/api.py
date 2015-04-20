
# -*- coding: utf-8 -*-

import subprocess
import os

from . import app
from .models import *

from flask import render_template
from flask import jsonify

@app.route('/api/drinks')
@app.route('/api/drinks/')
@app.route('/api/drinks/<drink_id>')
def api_drinks(drink_id=None):
    if drink_id is None:
        drinks_name = Drink.query.values(Drink.name)
        drinks_id   = Drink.query.values(Drink.id)

        drinks_zip = zip(drinks_name, drinks_id)
        drinks = {k[0]: v[0] for (k, v) in drinks_zip}

        return jsonify(drinks)
    else:
        drink_name = list(Drink.query.filter_by(id=drink_id).values(Drink.name))
        if len(drink_name) <= 0:
            return page_not_found(404)
        drink = {drink_name[0][0]: drink_id}

        return jsonify(drink)
    return page_not_found(404)


@app.route('/api/ingredients')
@app.route('/api/ingredients/')
@app.route('/api/ingredients/<ingredient_id>')
def api_ingredients(ingredient_id=None):
    if ingredient_id is None:
        ingredients_name = Ingredient.query.values(Ingredient.name)
        ingredients_id   = Ingredient.query.values(Ingredient.id)

        ingredients_zip = zip(ingredients_name, ingredients_id)
        ingredients = {k[0]: v[0] for (k, v) in ingredients_zip}

        return jsonify(ingredients)
    else:
        ingredient_name = list(Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.name))
        if len(ingredient_name) <= 0:
            return page_not_found(404)
        ingredient = {ingredient_name[0][0]: ingredient_id}

        return jsonify(ingredient)
    return page_not_found(404)


@app.route('/api/users')
@app.route('/api/users/')
@app.route('/api/users/<user_id>')
def api_users(user_id=None):
    if user_id is None:
        users_name = User.query.values(User.name)
        users_id = User.query.values(User.id)
        users = {k[0]: v[0] for (k, v) in zip(users_name, users_id)}

        return jsonify(users)
    else:
        user = User.query.filter_by(id=user_id)
        if user:
            user = user.first()
            return jsonify({
                "id": user.id,
                "name": user.name,
                "email": user.email
            })
        else:
            return "{}"


@app.route('/api/tests')
def api_tests():
    basedir = os.path.abspath(os.path.dirname(__file__))
    basedir = os.path.abspath(os.path.join(basedir, os.pardir))

    output = subprocess.check_output(['python', basedir + '/tests.py'],
                                     stderr=subprocess.STDOUT)

    return output


# -*- coding: utf-8 -*-

import subprocess
import os

from . import app
from .models import *

from flask import render_template, jsonify
from flask.ext import restful

api = restful.Api(app)


class DrinksListing(restful.Resource):
    """
    the class that returns the entire listing of drinks
    these drinks are provided in name, id value pairs
    if it is necessary to know more about an individual drink,
    refer to the DrinkId class below
    """
    def get(self):
        drinks_name = Drink.query.values(Drink.name)
        drinks_id = Drink.query.values(Drink.id)
        drinks = {k[0]: v[0] for (k, v) in zip(drinks_name, drinks_id)}

        return jsonify(drinks)

api.add_resource(DrinksListing, '/api/drinks')


class DrinkId(restful.Resource):
    """
    this is the class that queries an individual drink by id
    a drink will return all of it's associated fields in it
    plus the ingredients that the drink uses
    """

    def get(self, drink_id):
        drink = Drink.query.filter_by(id=drink_id)
        if drink:
            drink = drink.first()
            result = {
                "id": drink.id,
                "name": drink.name,
                "description": drink.description,
                "recipe": drink.recipe
            }

            quantities, ingredients = Drink.get_ingredients_by_id(drink_id)

            result["quantities"] = quantities
            result["ingredients"] = [x.name for x in ingredients]

            return jsonify(result)
        else:
            return "{}"

api.add_resource(DrinkId, '/api/drinks/<int:drink_id>')

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

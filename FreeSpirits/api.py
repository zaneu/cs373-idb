
# -*- coding: utf-8 -*-

import subprocess
import os

from . import app
from .models import *

from flask import render_template, jsonify
from flask.ext import restful

api = restful.Api(app)


class DrinkListing(restful.Resource):
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

api.add_resource(DrinkListing, '/api/drinks/')


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


class IngredientListing(restful.Resource):
    """
    This is the ingredients listing viewW
    This class is identical in design to the earlier DrinkListing
    """

    def get(self):
        ingredients_name = Ingredient.query.values(Ingredient.name)
        ingredients_id = Ingredient.query.values(Ingredient.id)
        ingredients = {k[0]: v[0] for (k, v) in
                       zip(ingredients_name, ingredients_id)}
        return jsonify(ingredients)

api.add_resource(IngredientListing, '/api/ingredients/')


class IngredientId(restful.Resource):
    """
    The endpoint to get an ingredient by id
    This returns all of the fields that the ingredient contains
    plus all the drinks that this ingredient is associated with
    """

    def get(self, ingredient_id):
        ingredient = Ingredient.query.filter_by(id=ingredient_id)
        if ingredient:
            ingredient = ingredient.first()
            result = {
                "id": ingredient.id,
                "name": ingredient.name,
                "description": ingredient.description,
                "calories": ingredient.calories,
                "energy": ingredient.energy,
                "fats": ingredient.fats,
                "carbohydrates": ingredient.carbohydrates,
                "protein": ingredient.protein,
                "fiber": ingredient.fiber,
                "sugars": ingredient.sugars,
                "cholesterol": ingredient.cholesterol,
                "sodium": ingredient.sodium,
                "alcohol": ingredient.alcohol
            }

            drinks = Ingredient.get_drinks_by_id(ingredient_id, -1)
            drinks = [x.name for x in drinks]
            result["drinks"] = drinks

            return jsonify(result)
        else:
            return "{}"

api.add_resource(IngredientId, '/api/ingredients/<int:ingredient_id>')

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

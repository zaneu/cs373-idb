# -*- coding: utf-8 -*-

import subprocess
import os

from . import app
from .models import *

from flask import render_template
from flask import jsonify
from json import dumps

from collections import OrderedDict

#app.config["JSON_SORT_KEYS"] = False

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
    if IngredientToDrink.query.filter_by(drink_id=drink_id).first() is None:
        return page_not_found(404)
    quantities = []
    ingredients = []
    for ingredient in IngredientToDrink.query.filter_by(drink_id=drink_id):
        quantities.append(ingredient.quantity)
        ingredients.append(Ingredient.query.filter_by(id=ingredient.ingredient_id).first())
    return render_template("drink.html", drink=Drink.query.filter_by(id=drink_id).first(), quantities=quantities, ingredients=ingredients)

@app.route('/ingredients')
@app.route('/ingredients/')
@app.route('/ingredients/<ingredient_id>')
def ingredients(ingredient_id=None):
    if ingredient_id is None:
        return render_template("ingredients.html", ingredients=Ingredient.query.order_by(Ingredient.name))
    ingredient_page = Ingredient.query.filter_by(id=ingredient_id).first()
    if ingredient_page is None:
        return page_not_found(404)
    return render_template("ingredient.html", ingredient=ingredient_page)

@app.route('/users')
@app.route('/users/')
@app.route('/users/<user_id>')
def users(user_id=None):
    if user_id is None:
        return render_template("users.html", users=User.query.order_by(User.name))
    user_page = User.query.filter_by(id=user_id).first()
    if user_page is None:
        return page_not_found(404)
    return render_template("user.html", user=user_page)

@app.route('/api/drinks')
@app.route('/api/drinks/')
@app.route('/api/drinks/<drink_id>')
def api_drinks(drink_id=None):
    if drink_id is None:
        drinks_name = Drink.query.values(Drink.name)
        drinks_id   = Drink.query.values(Drink.id)
        drinks_desc = Drink.query.values(Drink.description)
        drinks_recipe = Drink.query.values(Drink.recipe)

        drinks_zip = zip(drinks_id, drinks_name, drinks_desc, drinks_recipe)
        
        drinks = []
        for k, *v in drinks_zip :
            drink_dict = {'id': k[0], 'name': v[0][0], 'description': v[1][0], 'recipe': v[2][0]}
            drinks.append(drink_dict);
        #drinks = {k[0]: v[0][0] for (k, *v) in drinks_zip, k[0]: v[1][0]}
        
        
        return jsonify(r=drinks)
    else :
        drink_name = list(Drink.query.filter_by(id=drink_id).values(Drink.name))
        drink_desc = list(Drink.query.filter_by(id=drink_id).values(Drink.description))
        drink_recipe = list(Drink.query.filter_by(id=drink_id).values(Drink.recipe))
        ingredients = []
        quantities = []

        for ingredient in IngredientToDrink.query.filter_by(drink_id=drink_id):
            ingredients.append(Ingredient.query.filter_by(id=ingredient.ingredient_id).first())
            quantities.append(ingredient.quantity)

        if len(drink_name) <= 0:
            return page_not_found(404)
        
        all_ingredients = ""
        ingred_elem = []
        for i in ingredients:
            all_ingredients += i.name + ', '
            ingred_elem.append(i.name)
#        all_ingredients = " ".join(ingredients.name)

        c = ', '.join('%s %s' % t for t in zip(quantities, ingred_elem))

        drink_dict = OrderedDict()
        drink_dict['id'] = drink_id
        drink_dict['name'] = drink_name[0][0]
        drink_dict['description'] = drink_desc[0][0]
        drink_dict['instructions'] = drink_recipe[0][0]
#        drink_dict['quantities'] = str(quantities).strip('[]')
        drink_dict['recipe'] = c
        drink_dict['ingredients'] = all_ingredients[:-2]
        
#        {'id': drink_id, 'name': drink_name[0][0], 'description': drink_desc[0][0], 'recipe': drink_recipe[0][0], 'quantities': str(quantities).strip('[]'), 'ingredient': all_ingredients}
#        drink = {drink_name[0][0]: drink_id}

        return jsonify(drink_dict)
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
    else :
        ingredient_name = list(Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.name))
        ingredient_desc = list(Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.description))

        
        in_calo = Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.calories)
        in_ener = Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.energy)
        in_fats = Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.fats)
        in_carb = Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.carbohydrates)
        in_prot = Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.protein)
        in_fibe = Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.fiber)
        in_suga = Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.sugars)
        in_chol = Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.cholesterol)
        in_sodi = Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.sodium)
        in_alco = Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.alcohol)
        
        if len(ingredient_name) <= 0:
            return page_not_found(404)
        ingredient = {'id': ingredient_id, 'name': ingredient_name[0][0], 'description': ingredient_desc[0][0], 'calories': next(in_calo)[0], 'energy': next(in_ener)[0], 'fats': next(in_fats)[0], 'carbohydrates': next(in_carb)[0], 'protein': next(in_prot)[0], 'fiber': next(in_fibe)[0], 'sugars': next(in_suga)[0], 'cholesterol': next(in_chol)[0], 'sodium': next(in_sodi)[0], 'alcohol': next(in_alco)[0]}

        return jsonify(ingredient)
    return page_not_found(404)

@app.route('/api/tests')
@app.route('/api/tests/')
def api_tests():
    basedir = os.path.abspath(os.path.dirname(__file__))
    basedir = os.path.abspath(os.path.join(basedir, os.pardir))

    output = subprocess.check_output(['python', basedir + '/tests.py'], stderr=subprocess.STDOUT)

    return output

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

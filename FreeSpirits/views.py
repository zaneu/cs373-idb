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
            ingredients = []
            quantities = []
            for ingredient in IngredientToDrink.query.filter_by(drink_id=k[0]):
                ingredients.append(Ingredient.query.filter_by(id=ingredient.ingredient_id).first())
                quantities.append(ingredient.quantity)
                
            all_ingredients = ""
            ingred_elem = []
            for i in ingredients:
                all_ingredients += i.name + ', '
                ingred_elem.append(i.name)
            c = ', '.join('%s %s' % t for t in zip(quantities, ingred_elem))
            
            drink_dict = {'id': k[0], 'name': v[0][0], 'description': v[1][0], 'instructions': v[2][0]}
            drink_dict['recipe'] = c
            drink_dict['ingredients'] = all_ingredients[:-2]
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
        ins_name = Ingredient.query.values(Ingredient.name)
        ins_id   = Ingredient.query.values(Ingredient.id)
        
        ins_desc   = Ingredient.query.values(Ingredient.description)
        ins_calo   = Ingredient.query.values(Ingredient.calories)
        ins_ener   = Ingredient.query.values(Ingredient.energy)
        ins_fats   = Ingredient.query.values(Ingredient.fats)
        ins_carb   = Ingredient.query.values(Ingredient.carbohydrates)
        ins_prot   = Ingredient.query.values(Ingredient.protein)
        ins_fibe   = Ingredient.query.values(Ingredient.fiber)
        ins_suga   = Ingredient.query.values(Ingredient.sugars)
        ins_chol   = Ingredient.query.values(Ingredient.cholesterol)
        ins_sodi   = Ingredient.query.values(Ingredient.sodium)
        ins_alco   = Ingredient.query.values(Ingredient.alcohol)
        
        ingredients_zip = zip(ins_name, ins_id, ins_desc, ins_calo, ins_ener, ins_fats, ins_carb, ins_prot, ins_fibe, ins_suga, ins_chol, ins_sodi, ins_alco)
        ingredients_list = []
        for k, *v in ingredients_zip: # TODO: fix the key to id not name
            ingred_dict = {'id': v[0][0], 'name': k[0], 'description': v[1][0], 'calories': v[2][0], 'energy': v[3][0], 'fats': v[4][0], 'carbohydrates': v[5][0], 'protein': v[6][0], 'fiber': v[7][0], 'sugars': v[8][0], 'cholesterol': v[9][0], 'sodium': v[10][0], 'alcohol': v[11][0]}
            ingredients_list.append(ingred_dict)
        
        return jsonify(r=ingredients_list)
    else :
        in_name = list(Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.name))
        in_desc = list(Ingredient.query.filter_by(id=ingredient_id).values(Ingredient.description))

        
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
        
        if len(in_name) <= 0:
            return page_not_found(404)
        ingredient = {'id': ingredient_id, 'name': in_name[0][0], 'description': in_desc[0][0], 'calories': next(in_calo)[0], 'energy': next(in_ener)[0], 'fats': next(in_fats)[0], 'carbohydrates': next(in_carb)[0], 'protein': next(in_prot)[0], 'fiber': next(in_fibe)[0], 'sugars': next(in_suga)[0], 'cholesterol': next(in_chol)[0], 'sodium': next(in_sodi)[0], 'alcohol': next(in_alco)[0]}

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

# -*- coding: utf-8 -*-

import subprocess
import os

from . import app
from .models import *

from flask import render_template
from flask import jsonify
from json import dumps

from collections import OrderedDict
import flask.ext.whooshalchemy


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


@app.route('/signup')
def signup():
    return render_template("signup.html")

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


@app.route('/search')
@app.route('/search/<query>')
def search(query=None):
    if query is None:
        return render_template("search.html", results=[], query="\"\"")
    else:
        terms = query.lower().split()
        query = "\"" + query.lower() + "\""
        and_term = ""
        or_term = ""
        results = []

        for i, term in enumerate(terms):
            if i != 0:
                and_term += " AND " + term
                or_term += " OR " + term
            else:
                and_term += term
                or_term += term

        and_results = Drink.query.whoosh_search(and_term).all()
        or_results = Drink.query.whoosh_search(or_term).all()

        for drink in and_results:
            drink_dict = {'id': drink.id, 'name': drink.name}
            results.append(drink_dict)
        for drink in or_results:
            drink_dict = {'id': drink.id, 'name': drink.name}
            results.append(drink_dict)

        return render_template("search.html", results=results, query=query)


@app.route('/api/search')
@app.route('/api/search/<query>')
def api_search(query=None):
    if query is None:
        return page_not_found(404)
    else:
        terms = query.lower().split()
        print(terms)
        and_term = ""
        or_term = ""
        results = []

        for i, term in enumerate(terms):
            if i != 0:
                and_term += " AND " + term
                or_term += " OR " + term
            else:
                and_term += term
                or_term += term

        and_results = Drink.query.whoosh_search(and_term).all()
        or_results = Drink.query.whoosh_search(or_term).all()

        for drink in and_results:
            drink_dict = {'id': drink.id, 'name': drink.name}
            results.append(drink_dict)
        for drink in or_results:
            drink_dict = {'id': drink.id, 'name': drink.name}
            results.append(drink_dict)

        return jsonify(results=results)


@app.route('/api/drinks')
@app.route('/api/drinks/')
@app.route('/api/drinks/<drink_id>')
def api_drinks(drink_id=None):
    if drink_id is None:
        drinks_id   = Drink.query.values(Drink.id)

        drinks_list = []
        for d_id in drinks_id :
            drink_id = d_id[0]
            drink_obj = Drink.query.filter_by(id=drink_id)
            drink_name = drink_obj.values(Drink.name)
            drink_desc = drink_obj.values(Drink.description)
            drink_recipe = drink_obj.values(Drink.recipe)
            ingredients = []
            quantities = []

            for ingredient in IngredientToDrink.query.filter_by(drink_id=drink_id):
                ingredients.append(Ingredient.query.filter_by(id=ingredient.ingredient_id).first())
                quantities.append(ingredient.quantity)

            all_ingredients = ""
            ingred_elem = []
            for i in ingredients:
                all_ingredients += i.name + ', '
                ingred_elem.append(i.name)
            c = ', '.join('%s %s' % t for t in zip(quantities, ingred_elem))

            drink_dict = {'id': drink_id, 'name': next(drink_name)[0], 'description': next(drink_desc)[0], 'instructions': next(drink_recipe)[0]}
            drink_dict['recipe'] = c
            drink_dict['ingredients'] = all_ingredients[:-2]
            drinks_list.append(drink_dict)

        return jsonify(drinks=drinks_list)
    else:
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

        c = ', '.join('%s %s' % t for t in zip(quantities, ingred_elem))

        drink_dict = OrderedDict()
        drink_dict['id'] = drink_id
        drink_dict['name'] = drink_name[0][0]
        drink_dict['description'] = drink_desc[0][0]
        drink_dict['instructions'] = drink_recipe[0][0]
        drink_dict['recipe'] = c
        drink_dict['ingredients'] = all_ingredients[:-2]

        return jsonify(drink_dict)
    return page_not_found(404)


@app.route('/api/ingredients')
@app.route('/api/ingredients/')
@app.route('/api/ingredients/<ingredient_id>')
def api_ingredients(ingredient_id=None):
    if ingredient_id is None:
        ins_id = Ingredient.query.values(Ingredient.id)

        ingredients_list = []
        for i_id in ins_id:
            ingredient_id = i_id[0]
            in_ingr = Ingredient.query.filter_by(id=ingredient_id)
            in_name = in_ingr.values(Ingredient.name)
            in_desc = in_ingr.values(Ingredient.description)
            in_calo = in_ingr.values(Ingredient.calories)
            in_ener = in_ingr.values(Ingredient.energy)
            in_fats = in_ingr.values(Ingredient.fats)
            in_carb = in_ingr.values(Ingredient.carbohydrates)
            in_prot = in_ingr.values(Ingredient.protein)
            in_fibe = in_ingr.values(Ingredient.fiber)
            in_suga = in_ingr.values(Ingredient.sugars)
            in_chol = in_ingr.values(Ingredient.cholesterol)
            in_sodi = in_ingr.values(Ingredient.sodium)
            in_alco = in_ingr.values(Ingredient.alcohol)

            ingred_dict = {'id': ingredient_id, 'name': next(in_name)[0], 'description': next(in_desc)[0], 'calories': next(in_calo)[0], 'energy': next(in_ener)[0], 'fats': next(in_fats)[0], 'carbohydrates': next(in_carb)[0], 'protein': next(in_prot)[0], 'fiber': next(in_fibe)[0], 'sugars': next(in_suga)[0], 'cholesterol': next(in_chol)[0], 'sodium': next(in_sodi)[0], 'alcohol': next(in_alco)[0]}
            ingredients_list.append(ingred_dict)

        return jsonify(ingredients=ingredients_list)
    else:
        in_ingr = Ingredient.query.filter_by(id=ingredient_id)
        in_name = list(in_ingr.values(Ingredient.name))
        in_desc = list(in_ingr.values(Ingredient.description))

        in_calo = in_ingr.values(Ingredient.calories)
        in_ener = in_ingr.values(Ingredient.energy)
        in_fats = in_ingr.values(Ingredient.fats)
        in_carb = in_ingr.values(Ingredient.carbohydrates)
        in_prot = in_ingr.values(Ingredient.protein)
        in_fibe = in_ingr.values(Ingredient.fiber)
        in_suga = in_ingr.values(Ingredient.sugars)
        in_chol = in_ingr.values(Ingredient.cholesterol)
        in_sodi = in_ingr.values(Ingredient.sodium)
        in_alco = in_ingr.values(Ingredient.alcohol)

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

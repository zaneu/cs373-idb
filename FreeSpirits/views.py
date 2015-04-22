# -*- coding: utf-8 -*-

from . import app, login_manager
from .models import *
from .forms import *

from flask import render_template, jsonify, flash, redirect, url_for, \
    request
from flask.ext.login import login_user, logout_user, login_required


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


@login_manager.user_loader
def load_user(user_id):
    user_id = int(user_id)
    return User.query.get(user_id)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignupForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Welcome to Free Spirits, " + user.first_name)
        return redirect(url_for('index'))

    return render_template("signup.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        login_user(user)
        flash("Welcome back, " + user.first_name)
        return redirect(url_for('index'))

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out")

    return redirect(url_for('index'))


@app.route('/drinks')
@app.route('/drinks/<page>')
def drinks(page=1):
    page = int(page)
    pagination = Drink.query.order_by(Drink.name)
    if request.args.get("sort_by") == "favorites":
        pagination = Drink.query.order_by(Drink.favorites.desc())

    pagination = pagination.paginate(page, 100)

    return render_template("drinks.html",
                           page=page,
                           pagination=pagination)


@app.route('/drink/<drink_id>')
def drink(drink_id=1):
    query = Drink.query.filter_by(id=drink_id)
    if query.first():
        quantities, ingredients = Drink.get_ingredients_by_id(drink_id)
        return render_template("drink.html",
                               drink=query.first(),
                               quantities=quantities,
                               ingredients=ingredients)
    else:
        return page_not_found(404)


@app.route('/ingredients/')
@app.route('/ingredients/<page>')
def ingredients(page=1):
    page = int(page)
    pagination = Ingredient.query.order_by(Ingredient.name)
    if request.args.get("sort_by") == "favorites":
        pagination = Ingredient.query.order_by(Ingredient.favorites.desc())

    pagination = pagination.paginate(page, 100)

    return render_template("ingredients.html",
                           page=page,
                           pagination=pagination)


@app.route('/ingredient/<ingredient_id>')
def ingredient(ingredient_id=1):
    query = Ingredient.query.filter_by(id=ingredient_id)
    if query.first():
        drinks = Ingredient.get_drinks_by_id(ingredient_id, 10)
        return render_template("ingredient.html",
                               ingredient=query.first(),
                               drinks=drinks)
    else:
        return page_not_found(404)


@app.route('/users')
@app.route('/users/<page>')
def users(page=1):
    page = int(page)
    pagination = User.query.order_by(User.first_name,
                                     User.last_name).paginate(page, 100)

    return render_template("users.html",
                           page=page,
                           pagination=pagination)


@app.route('/user/<user_id>')
def user(user_id=1):
    query = User.query.filter_by(id=user_id)
    if query.first():
        return render_template("user.html", user=query.first())
    else:
        return page_not_found(404)


@app.route('/search')
@app.route('/search/<query>')
def search_drinks(query=None):
    if query is None:
        return render_template("search.html", drinks_results=[], ingredients_results = [], users_results = [], query="\"\"")
    else:
        terms = query.lower().split()
        query = "\"" + query.lower() + "\""
        and_term = ""
        or_term = ""
        drinks = []
        ingredients = []
        users = []

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
            drinks.append(drink_dict)
        for drink in or_results:
            drink_dict = {'id': drink.id, 'name': drink.name}
            drinks.append(drink_dict)

        and_results = Ingredient.query.whoosh_search(and_term).all()
        or_results = Ingredient.query.whoosh_search(or_term).all()

        for ingredient in and_results:
            ingredient_dict = {'id': ingredient.id, 'name': ingredient.name}
            ingredients.append(ingredient_dict)
        for ingredient in or_results:
            ingredient_dict = {'id': ingredient.id, 'name': ingredient.name}
            ingredients.append(ingredient_dict)

        and_results = User.query.whoosh_search(and_term).all()
        or_results = User.query.whoosh_search(or_term).all()

        for user in and_results:
            user_dict = {'id': user.id, 'name': user.name}
            users.append(user_dict)
        for drink in or_results:
            user_dict = {'id': user.id, 'name': user.name}
            users.append(user_dict)

        return render_template("search.html", drinks=drinks, ingredients=ingredients, users=users, pillar=pillar, query=query)


@app.route('/api/search')
@app.route('/api/search/<query>')
def api_search_drinks(query=None):
    if query is None:
        return page_not_found(404)
    else:
        terms = query.lower().split()
        query = "\"" + query.lower() + "\""
        and_term = ""
        or_term = ""
        drinks = []
        ingredients = []
        users = []

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
            drinks.append(drink_dict)
        for drink in or_results:
            drink_dict = {'id': drink.id, 'name': drink.name}
            drinks.append(drink_dict)

        and_results = Ingredient.query.whoosh_search(and_term).all()
        or_results = Ingredient.query.whoosh_search(or_term).all()

        for ingredient in and_results:
            ingredient_dict = {'id': ingredient.id, 'name': ingredient.name}
            ingredients.append(ingredient_dict)
        for ingredient in or_results:
            ingredient_dict = {'id': ingredient.id, 'name': ingredient.name}
            ingredients.append(ingredient_dict)

        and_results = User.query.whoosh_search(and_term).all()
        or_results = User.query.whoosh_search(or_term).all()

        for user in and_results:
            user_dict = {'id': user.id, 'name': user.first_name + " " + user.last_name}
            users.append(user_dict)
        for drink in or_results:
            user_dict = {'id': user.id, 'name': user.first_name + " " + user.last_name}
            users.append(user_dict)

        results = []
        results.append(drinks)
        results.append(ingredients)
        results.append(users)

        return jsonify(results=results)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

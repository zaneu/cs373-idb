# -*- coding: utf-8 -*-

from . import app, db
import hashlib

from werkzeug.security import generate_password_hash, \
     check_password_hash

import flask.ext.whooshalchemy as whooshalchemy
from flask.ext.login import UserMixin


def parse_query(query):
    """
    Helper method to parse the queries
    This function is invoked in Drink, Ingredient, and Users' search functions
    """
    terms = query.lower().split()
    query = "\"" + query.lower() + "\""
    and_term = ""
    or_term = ""

    for i, term in enumerate(terms):
        if i != 0:
            and_term += " AND " + term
            or_term += " OR " + term
        else:
            and_term += term
            or_term += term

    return (and_term, or_term)


def parse_results(and_results, or_results):
    """
    A helper function that takes in the results lists
    and returns the id: name key pair values
    """

    result = []
    for item in and_results:
        result.append({'id': item.id, 'name': item.name})
    for drink in or_results:
        result.append({'id': item.id, 'name': item.name})

    return result


class User(db.Model, UserMixin):
    """
    The User model
    As of now, this class is not related to the database at all
    This will be done in the later phases
    So, the instance variables will have to be replaced with Columns and so
    forth to accomodate for SQL-Alchemy

    The associations will be done by join tables and are thus excluded here

    The required variables of this class are:
    the name
    the email
    """
    __tablename__ = "User"
    __searchable__ = ["first_name", "last_name", "email"]

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    pw_hash = db.Column(db.String(120))

    @staticmethod
    def search(query, limit=50):
        if query is None or not query.strip():
            return []

        and_term, or_term = parse_query(query)
        and_results = User.query.whoosh_search(and_term) \
                                .limit(50).all()
        or_results = User.query.whoosh_search(or_term) \
                               .limit(50).all()
        or_results = list(set(and_results).symmetric_difference(or_results))

        result = []
        for item in and_results:
            result.append({'id': item.id, 'name': item.first_name + " " +
                           item.last_name})
        for drink in or_results:
            result.append({'id': item.id, 'name': item.first_name + " " +
                           item.last_name})

        return result

    def get_image(self):
        size = 200
        email = str(self.email).strip().lower().encode('utf-8')
        return "http://www.gravatar.com/avatar/" + \
            hashlib.md5(email).hexdigest() + "?s=" + str(size)

    def get_drinks(self):
        rows = UserToDrink.query.filter_by(user_id=self.id).all()
        drinks = []
        for row in rows:
            drink_id = row.drink_id
            drinks.append(Drink.query.get(drink_id))
        return drinks

    def get_ingredients(self):
        rows = UserToIngredient.query.filter_by(user_id=self.id).all()
        ingredients = []
        for row in rows:
            ingredient_id = row.ingredient_id
            ingredients.append(Ingredient.query.get(ingredient_id))
        return ingredients

    def star_drink(self, drink):
        row = UserToDrink(
            user_id=self.id,
            drink_id=drink.id
        )
        db.session.add(row)
        drink.favorites += 1
        db.session.commit()

    def remove_drink(self, drink):
        row = UserToDrink.query.filter_by(user_id=self.id) \
                               .filter_by(drink_id=drink.id).first()
        db.session.delete(row)
        drink.favorites -= 1
        db.session.commit()

    def has_starred_drink(self, drink):
        row = UserToDrink.query.filter_by(user_id=self.id) \
                               .filter_by(drink_id=drink.id).first()
        return row is not None

    def star_ingredient(self, ingredient):
        row = UserToIngredient(
            user_id=self.id,
            ingredient_id=ingredient.id
        )
        db.session.add(row)
        ingredient.favorites += 1
        db.session.commit()

    def remove_ingredient(self, ingredient):
        row = UserToIngredient.query.filter_by(user_id=self.id) \
                                    .filter_by(ingredient_id=ingredient.id) \
                                    .first()
        db.session.delete(row)
        ingredient.favorites -= 1
        db.session.commit()

    def has_starred_ingredient(self, ingredient):
        row = UserToIngredient.query.filter_by(user_id=self.id) \
                                    .filter_by(ingredient_id=ingredient.id) \
                                    .first()
        return row is not None

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def has_favorited(self, drink_id):
        return True

    def __repr__(self):
        return "<User %r>" % (self.email)

whooshalchemy.whoosh_index(app, User)


class UserToDrink(db.Model):
    """
    This is the join table between users and drinks representing favorites
    Queries are not to be made directly on this class, but to instead use
    the User instance methods
    """
    __tablename__ = "UserDrink"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                        primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('Drink.id'),
                         primary_key=True)


class UserToIngredient(db.Model):
    """
    This is the join table between users and drinks representing favorites
    Queries are not to be made directly on this class, but to instead use
    the User instance methods
    """
    __tablename__ = "UserIngredient"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                        primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'),
                              primary_key=True)


class IngredientToDrink(db.Model):
    """
    This is the join table between ingredients and drinks
    It was necessary to create a separate class, rather than a table, since we
    wanted to include an extra column (quantity) between each relationship
    """
    __tablename__ = "IngredientDrink"

    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'),
                              primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('Drink.id'),
                         primary_key=True)
    quantity = db.Column(db.String(200))


class Ingredient(db.Model):
    """
    The required variables of this class are
    The name
    The description
    The nutritional values (an array)
    """
    __tablename__ = "Ingredient"
    __searchable__ = ["name", "description"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    description = db.Column(db.String(10000))
    calories = db.Column(db.String(20))
    energy = db.Column(db.String(20))
    fats = db.Column(db.String(20))
    carbohydrates = db.Column(db.String(20))
    protein = db.Column(db.String(20))
    fiber = db.Column(db.String(20))
    sugars = db.Column(db.String(20))
    cholesterol = db.Column(db.String(20))
    sodium = db.Column(db.String(20))
    alcohol = db.Column(db.String(20))
    favorites = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    @staticmethod
    def search(query, limit=50):
        if query is None or not query.strip():
            return []

        and_term, or_term = parse_query(query)
        and_results = Ingredient.query.whoosh_search(and_term) \
                                      .limit(limit).all()
        or_results = Ingredient.query.whoosh_search(or_term) \
                                     .limit(limit).all()

        or_results = list(set(and_results).symmetric_difference(or_results))

        return parse_results(and_results, or_results)

    @staticmethod
    def get_drinks_by_id(id, limit):
        query = IngredientToDrink.query.filter_by(ingredient_id=id)
        drinks = []
        for count, row in enumerate(query):
            if limit > 0 and count >= limit:
                break
            drinks.append(Drink.query.filter_by(id=row.drink_id).first())

        return drinks

    @staticmethod
    def get_drinks_by_name(name, limit):
        id = Ingredient.query.filter_by(name=name).first().id
        return Ingredient.get_drinks_by_id(id, limit)

    def __repr__(self):
        return "<Ingredient %r>" % (self.name)

whooshalchemy.whoosh_index(app, Ingredient)


class Drink(db.Model):
    """
    The required variables of this class are
    The name
    The description
    The nutritional values (an array)
    """
    __tablename__ = "Drink"
    __searchable__ = ["name", "description", "recipe"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String(10000))
    recipe = db.Column(db.String(10000))
    favorites = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    @staticmethod
    def search(query, limit=50):
        if query is None or not query.strip():
            return []

        and_term, or_term = parse_query(query)
        and_results = Drink.query.whoosh_search(and_term) \
                                 .limit(limit).all()
        or_results = Drink.query.whoosh_search(or_term) \
                                .limit(limit).all()
        or_results = list(set(and_results).symmetric_difference(or_results))

        return parse_results(and_results, or_results)

    @staticmethod
    def get_ingredients_by_id(id):
        query = IngredientToDrink.query.filter_by(drink_id=id)
        quantities = []
        ingredients = []
        for row in query:
            quantities.append(row.quantity)
            ingredients.append(Ingredient.query.
                               filter_by(id=row.ingredient_id).first())

        return (quantities, ingredients)

    @staticmethod
    def get_ingredients_by_name(name):
        id = Drink.query.filter_by(name=name).first().id
        return Drink.get_ingredients_by_id(id)

    def __repr__(self):
        return "<Drink %r>" % (self.name)

whooshalchemy.whoosh_index(app, Drink)

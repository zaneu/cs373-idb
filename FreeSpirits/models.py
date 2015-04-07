# -*- coding: utf-8 -*-

from . import db

class User(db.Model):
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

    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return "<User %r>" % (self.name)
 

class IngredientToDrink(db.Model):
    """
    This is the join table between ingredients and drinks
    It was necessary to create a separate class, rather than a table, since we
    wanted to include an extra column (quantity) between each relationship
    """
    __tablename__ = "IngredientDrink"

    id            = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'), primary_key=True)
    drink_id      = db.Column(db.Integer, db.ForeignKey('Drink.id'), primary_key=True)
    quantity      = db.Column(db.String(200))


class Ingredient(db.Model):
    """
    The required variables of this class are
    The name
    The description
    The nutritional values (an array)
    """
    __tablename__ = "Ingredient"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), index=True, unique=True)
    description   = db.Column(db.String(2000))
    calories      = db.Column(db.String(20))
    energy        = db.Column(db.String(20))
    fats          = db.Column(db.String(20))
    carbohydrates = db.Column(db.String(20))
    protein       = db.Column(db.String(20))
    fiber         = db.Column(db.String(20))
    sugars        = db.Column(db.String(20))
    cholesterol   = db.Column(db.String(20))
    sodium        = db.Column(db.String(20))
    alcohol       = db.Column(db.String(20))

    def __repr__(self):
        return "<Ingredient %r>" % (self.name)


class Drink(db.Model):
    """
    The required variables of this class are
    The name
    The description
    The nutritional values (an array)
    """
    __tablename__ = "Drink"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), index=True, unique=True)
    description   = db.Column(db.String(2000))
    ingredients   = db.Column
    calories      = db.Column(db.String(20))
    energy        = db.Column(db.String(20))
    fats          = db.Column(db.String(20))
    carbohydrates = db.Column(db.String(20))
    protein       = db.Column(db.String(20))
    fiber         = db.Column(db.String(20))
    sugars        = db.Column(db.String(20))
    cholesterol   = db.Column(db.String(20))
    sodium        = db.Column(db.String(20))
    alcohol       = db.Column(db.String(20))


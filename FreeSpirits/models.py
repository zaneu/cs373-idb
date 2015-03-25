# -*- coding: utf-8 -*-

class User():
    """
    The User model
    As of now, this class is not related to the database at all
    This will be done in the later phases
    So, the instance variables will have to be replaced with Columns and so
    forth to accomodate for SQL-Alchemy

    The associations will be done by joint tables and are thus excluded here

    The required variables of this class are:
    the name
    the email
    potentially Facebook OAuth (TBD)
    """

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email


class Ingredient():
    """
    The required variables of this class are
    The name
    The description
    The nutritional values (an array)
    """

    def __init__(self, name=None, description=None, nutrition=None):
        self.name = name
        self.description = description
        self.nutrition = nutrition


class Drink():
    """
    The required variables of this class are
    The name
    The description
    The ingredients (dictionary of names and values)
    The nutritional values (an array)
    """

    def __init__(self, name=None, ingredients=None, nutrition=None):
        self.name = name
        self.ingredients = ingredients
        self.nutrition = nutrition

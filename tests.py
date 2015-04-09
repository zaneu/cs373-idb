# -*- coding: utf-8 -*-

import os

from flask import Flask

from FreeSpirits import app, db, test_client
from FreeSpirits.models import *
from flask.ext.testing import TestCase
from flask.ext.sqlalchemy import SQLAlchemy

import unittest

basedir = os.path.abspath(os.path.dirname(__file__))
test_client(basedir)
db.create_all()

class ModelTests(unittest.TestCase):
    """
    The main test suite
    This function creates a dummy sqlite3 database (test.db)
    """
    
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # =====
    # Tests
    # =====

    def test_add_default_ingredient(self):
        ingredient = Ingredient()
        db.session.add(ingredient)
        db.session.commit()

        self.assertTrue(ingredient in db.session)

    def test_add_ingredient_1(self):
        ingredient = Ingredient(name="Mint")
        db.session.add(ingredient)
        db.session.commit()

        self.assertTrue(ingredient in db.session)
        self.assertEqual(Ingredient.query.filter_by(name="Mint").first(), ingredient)

    def test_add_ingredient_2(self):
        ingredient = Ingredient(name="Rum", calories="120")
        db.session.add(ingredient)
        db.session.commit()

        self.assertTrue(ingredient in db.session)
        self.assertEqual(Ingredient.query.filter_by(calories="120").first(), ingredient)
    
    def test_add_ingredient_3(self):
        ingredient = Ingredient(name="Rum", calories="120", energy="100")
        db.session.add(ingredient)
        db.session.commit()

        self.assertTrue(ingredient in db.session)
        self.assertEqual(Ingredient.query.filter_by(energy="100").first(), ingredient)
    
    def test_add_default_drink(self):
        drink = Drink()
        db.session.add(drink)
        db.session.commit()

        self.assertTrue(drink in db.session)
    
    def test_add_drink_1(self):
        drink = Drink(name="Gin & Tonic")
        db.session.add(drink)
        db.session.commit()

        self.assertTrue(drink in db.session)
        self.assertEqual(Drink.query.filter_by(name="Gin & Tonic").first(), drink)
    
    def test_add_drink_2(self):
        drink = Drink(name="Gin & Tonic", recipe="Mix Gin and Tonic. Stir slowly")
        db.session.add(drink)
        db.session.commit()

        self.assertTrue(drink in db.session)
        self.assertEqual(Drink.query.filter_by(recipe="Mix Gin and Tonic. Stir slowly").first(), drink)

    def test_add_drink_3(self):
        drink = Drink(name="Gin & Tonic", recipe="Mix Gin and Tonic. Stir slowly")
        db.session.add(drink)
        db.session.commit()

        self.assertTrue(drink in db.session)
        self.assertEqual(Drink.query.filter_by(name="Gin & Tonic").first(), drink)

    def test_add_default_user(self):
        user = User()
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user in db.session)

    def test_add_user_1(self):
        user = User(name="Paul")
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user in db.session)
        self.assertEqual(User.query.filter_by(name="Paul").first(), user)
    
    def test_add_user_2(self):
        user = User(name="Paul", email="pbae@utexas.edu")
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user in db.session)
        self.assertEqual(User.query.filter_by(email="pbae@utexas.edu").first(), user)

if __name__ == '__main__':
    unittest.main()


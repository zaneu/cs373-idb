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
    
    
if __name__ == '__main__':
    unittest.main()


# -*- coding: utf-8 -*-

from models import *
import unittest

class TestModels(unittest.TestCase):

    def test_user_default(self):
        u = User()
        self.assertEqual(u.name, None)
        self.assertEqual(u.email, None)

    def test_user_name(self):
        u = User("Paul")
        self.assertEqual(u.name, "Paul")
        self.assertEqual(u.email, None)
    
    def test_user_name_email(self):
        u = User("Paul", "pbae@utexas.edu")
        self.assertEqual(u.name, "Paul")
        self.assertEqual(u.email, "pbae@utexas.edu")

    def test_ingredient_default(self):
        i = Ingredient()
        self.assertEqual(i.name, None)
        self.assertEqual(i.description, None)
        self.assertEqual(i.nutrition, None)

    def test_ingredient_name(self):
        i = Ingredient("Lemon")
        self.assertEqual(i.name, "Lemon")
        self.assertEqual(i.description, None)
        self.assertEqual(i.nutrition, None)
    
    def test_ingredient_name_description(self):
        i = Ingredient("Lemon", "Very sour!")
        self.assertEqual(i.name, "Lemon")
        self.assertEqual(i.description, "Very sour!")
        self.assertEqual(i.nutrition, None)

    def test_drink_default(self):
        d = Drink()
        self.assertEqual(d.name, None)
        self.assertEqual(d.ingredients, None)
        self.assertEqual(d.nutrition, None)

    def test_drink_name(self):
        d = Drink("Caribou Lou")
        self.assertEqual(d.name, "Caribou Lou")
        self.assertEqual(d.ingredients, None)
        self.assertEqual(d.nutrition, None)
    
    def test_drink_name_description(self):
        ingredients = {
            "151 Rum": "3 / 2 parts", 
            "Malibu coconut Rum": "1 part", 
            "Pineapple juice": "5 parts" 
        }

        d = Drink("Caribou Lou", ingredients)

        self.assertEqual(d.name, "Caribou Lou")
        self.assertEqual(d.ingredients, ingredients)
        self.assertEqual(d.nutrition, None)

if __name__ == '__main__':
    unittest.main()


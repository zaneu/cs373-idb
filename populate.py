# -*- coding: utf-8 -*-
"""
Populates the database in app.db
This relies on the files data/ingredients.json and data/drinks.json
Users are not populated from this database
"""

import json
from FreeSpirits import db
from FreeSpirits.models import Ingredient
from FreeSpirits.models import Drink
from FreeSpirits.models import IngredientToDrink
from sqlalchemy import func
from clint.textui import progress

print("Dropping all tables")
db.drop_all()
print("Creating all tables")
db.create_all()

print("Loading data/ingredients.json")
f = open("data/ingredients.json")
ingredients = json.load(f)
ingredient_table = {}
f.close()

for value in progress.bar(ingredients):
    ingredient = Ingredient(
            name=value["name"],
            description=value["description"],
            calories=value["calories"],
            energy=value["energy"],
            fats=value["fats"],
            carbohydrates=value["carbohydrates"],
            protein=value["protein"],
            fiber=value["fiber"],
            sugars=value["sugars"],
            cholesterol=value["cholesterol"],
            sodium=value["sodium"],
            alcohol=value["alcohol"]
    )

    db.session.add(ingredient)
    ingredient_table[value["id"]] = ingredient

print("Committing ingredients")
db.session.commit()

print("Loading data/drinks.json")
f = open("data/drinks.json")
drinks = json.load(f)
f.close()

count = 1
drink_count = 1

for value in progress.bar(drinks):
    drink = Drink(
            name=value["name"],
            description=value["description"],
            recipe=value["recipe"]
    )

    db.session.add(drink)
    db.session.commit()

    for ingredient_id in value["ingredients"]:
        ingredient_quantity = value["ingredients"][ingredient_id]
        ingredient = ingredient_table[ingredient_id]

        link = IngredientToDrink(id=count, ingredient_id=ingredient.id, drink_id=drink.id, quantity=ingredient_quantity)
        db.session.add(link)
        count += 1

print("Committing drinks")
db.session.commit()

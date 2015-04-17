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
from FreeSpirits.models import User
from FreeSpirits.models import IngredientToDrink
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
        id=drink_count,
        name=value["name"],
        description=value["description"],
        recipe=value["recipe"]
    )

    db.session.add(drink)

    for ingredient_id in value["ingredients"]:
        ingredient_quantity = value["ingredients"][ingredient_id]
        ingredient = ingredient_table[ingredient_id]

        link = IngredientToDrink(id=count,
                                 ingredient_id=ingredient.id,
                                 drink_id=drink_count,
                                 quantity=ingredient_quantity)
        db.session.add(link)
        count += 1

    drink_count += 1

print("Committing drinks")
db.session.commit()

print("Loading dummy users")
users = [
    {"name": "Paul Bae", "email": "pbae@utexas.edu"},
    {"name": "Larry Liu", "email": "liudi1990@gmail.com"},
    {"name": "Zane Urbanski", "email": "urbanski@utexas.edu"},
    {"name": "Ali Homafar", "email": "home.isfar@gmail.com"},
    {"name": "Menglin Brown", "email": "menglinbrown@utexas.edu"},
    {"name": "Jin Tang", "email": "jindtang@utexas.edu"}
]

for value in progress.bar(users):
    user = User(
        name=value["name"],
        email=value["email"]
    )

    db.session.add(user)

print("Committing users")
db.session.commit()

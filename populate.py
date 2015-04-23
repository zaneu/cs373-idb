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
        alcohol=value["alcohol"],
        favorites=0
    )

    db.session.add(ingredient)
    ingredient_table[value["id"]] = ingredient

print("Committing ingredients")
db.session.commit()

print("Loading data/drinks.json")
f = open("data/drinks.json")
drinks = json.load(f)
f.close()

drink_count = 1
drinks_listing = []
ingredients_listing = []

for value in progress.bar(drinks):
    drink = Drink(
        id=drink_count,
        name=value["name"],
        description=value["description"],
        recipe=value["recipe"],
        favorites=0
    )

    db.session.add(drink)

    drinks_listing.append(drink)
    ingredients_listing.append(value["ingredients"])

    drink_count += 1

print("Committing drinks")
db.session.commit()

print("Loading the many to many from Drink to Ingredient")
count = 1
for drink, ingredients in progress.bar(list(zip(drinks_listing,
                                                ingredients_listing))):
    for ingredient_id in ingredients:
        ingredient_quantity = ingredients[ingredient_id]
        ingredient = ingredient_table[ingredient_id]

        link = IngredientToDrink(id=count,
                                 ingredient_id=ingredient.id,
                                 drink_id=drink.id,
                                 quantity=ingredient_quantity)
        db.session.add(link)
        count += 1

print("Committing many to many from Drink to Ingredient")
db.session.commit()

print("Loading dummy users")
users = [
    {"first_name": "Paul", "last_name": "Bae",
     "email": "pbae@utexas.edu", "pass": "123"},
    {"first_name": "Larry", "last_name": "Liu",
     "email": "liudi1990@gmail.com", "pass": "132"},
    {"first_name": "Zane", "last_name": "Urbanski",
     "email": "urbanski@utexas.edu", "pass": "321"},
    {"first_name": "Ali", "last_name": "Homafar",
     "email": "home.isfar@gmail.com", "pass": "312"},
    {"first_name": "Menglin", "last_name": "Brown",
     "email": "menglinbrown@utexas.edu",
     "pass": "213"},
    {"first_name": "Jin", "last_name": "Tang",
     "email": "jindtang@utexas.edu", "pass": "231"}
]

for value in progress.bar(users):
    user = User(
        first_name=value["first_name"],
        last_name=value["last_name"],
        email=value["email"]
    )

    user.set_password(value["pass"])
    db.session.add(user)

print("Committing users")
db.session.commit()

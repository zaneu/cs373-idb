# -*- coding: utf-8 -*-

import json
from FreeSpirits import db
from FreeSpirits import Ingredient
from FreeSpirits import Drink
from FreeSpirits import IngredientToDrink

print("Dropping all tables")
db.drop_all()
print("Creating all tables")
db.create_all()

print("Loading data/ingredients.json")
ingredients = json.load(with f as open("data/ingredients.json"))

for key in ingredients:
    value = ingredients[key]
    Ingredient ingredient = Ingredient(
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
    print("Added ingredient: " + value["name"])

print("Committing ingredients")
db.session.commit()

print("Loading data/drinks.json")
drinks = json.load(with f as open("data/drinks.json"))

for key in drinks:
    value = drinks[key]

    Drink drink = Drink(
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

    for ingredient_name in value["ingredients"]:
        ingredient_quantity = value["ingredients"][ingredient_name]
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        link = IngredientToDrink(ingredient_id=ingredient.id, drink_id=drink.id, quantity=ingredient_quantity)
        db.session.add(link)

    db.session.add(drink)
    print("Added drink: " + value["name"])

print("Committing drinks")
db.session.commit()

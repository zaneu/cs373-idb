# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DrinkItem(scrapy.Item):
    """
    the Drink Item
    """

    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    recipe = scrapy.Field()
    ingredients = scrapy.Field()


class IngredientItem(scrapy.Item):
    """
    the ingredient item
    note that we override the id function here
    """

    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    nutrition = scrapy.Field()

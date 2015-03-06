from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from bs4 import BeautifulSoup
from free_spirits.items import IngredientItem

import re


class IngredientsSpider(CrawlSpider):
    name = "ingredients"
    allowed_domains = ["drinksmixer.com"]

    start_urls = [
        "http://www.drinksmixer.com/desc%d.html" % p for p in xrange(1, 1351)
    ]

    rules = (
        Rule(LinkExtractor(allow='http://www\.drinksmixer\.com/desc\d+\.html',), callback='parse_ingredient'),
    )

    def parse_ingredient(self, response):
        """
        parsing the ingredients
        we get the id of the ingredient simply by the url
        """

        ingredient = IngredientItem()
        soup = BeautifulSoup(response.body, "lxml")

        id          = re.findall(r'\d+', response.url)[0]
        title       = soup.find("title").contents[0].rstrip("information")
        description = soup.find("div", {"class": "pl"})

        ingredient['id']          = id
        ingredient['name']        = title.rstrip()
        ingredient['nutrition']   = {}
        ingredient['description'] = ""

        for x in description.contents:
            if x and type(x) is str:
                IngredientsSpider['description'] += x

        return ingredient

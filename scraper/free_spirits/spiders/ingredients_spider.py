from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

import bs4
from bs4 import BeautifulSoup
from free_spirits.items import IngredientItem
from common import *

import re

class IngredientsSpider(CrawlSpider):
    """
    the IngredientsSpider
    """

    name = "ingredients"
    allowed_domains = ["drinksmixer.com"]

    start_urls = [
        "http://www.drinksmixer.com/desc%d.html" % p for p in xrange(1, 2917)
    ]

    rules = (
        Rule(LinkExtractor(allow='http://www\.drinksmixer\.com/desc\d+\.html'),
             callback='parse_ingredient'),
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

        ingredient['id'] = id
        ingredient['name'] = title.rstrip()
        ingredient['description'] = "".join(filter(check_if_str,
                                                   description.contents))
        table = soup.find("table", {"id": "cl",
                                    "cellspacing": "1",
                                    "cellpadding": "0",
                                    "width": "98%",
                                    "border": "0"})
        if table:
            table = table.find("tr")

            # first remove the specifiers (calories, energy, fats)
            for s in table.find_all("td", {"width": "135", "valign": "top"}):
                s.extract()

            listing = table.find("td", {"valign": "top"})
            listing = listing.find("p", {"class": "l1a"})
            values  = values_from_listing(listing)

            ingredient["calories"]      = values[0] if len(values) > 0 else ""
            ingredient["energy"]        = values[1] if len(values) > 1 else ""
            ingredient["fats"]          = values[2] if len(values) > 2 else ""
            ingredient["carbohydrates"] = values[3] if len(values) > 3 else ""
            ingredient["protein"]       = values[4] if len(values) > 4 else ""

            listing = listing.findNext("p", {"class": "l1a"})
            values  = values_from_listing(listing)

            ingredient["fiber"]       = values[0] if len(values) > 0 else ""
            ingredient["sugars"]      = values[1] if len(values) > 1 else ""
            ingredient["cholesterol"] = values[2] if len(values) > 2 else ""
            ingredient["sodium"]      = values[3] if len(values) > 3 else ""
            ingredient["alcohol"]     = values[4] if len(values) > 4 else ""
        else:
            ingredient["calories"]      = ""
            ingredient["energy"]        = ""
            ingredient["fats"]          = ""
            ingredient["carbohydrates"] = ""
            ingredient["protein"]       = ""
            ingredient["fiber"]         = ""
            ingredient["sugars"]        = ""
            ingredient["cholesterol"]   = ""
            ingredient["sodium"]        = ""
            ingredient["alcohol"]       = ""

        return ingredient

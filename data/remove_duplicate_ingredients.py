#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

a = {}
f = open("ingredients.json")
ingredients = json.load(f)

for ingredient in ingredients:
    a[ingredient["id"]] = ingredient

print(json.dumps(list(a.values())))

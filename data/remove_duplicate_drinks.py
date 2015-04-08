#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

a = {}
f = open("drinks.json")
drinks = json.load(f)

for drink in drinks:
    a[drink["name"]] = drink

print(json.dumps(list(a.values())))

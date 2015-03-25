# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)

# late imports so dependencies are correct
from . import views

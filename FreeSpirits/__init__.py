# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

# late imports so dependencies are correct
from . import views
from . import models

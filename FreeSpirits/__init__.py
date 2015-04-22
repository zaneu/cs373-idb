# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object("config")
CsrfProtect(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# late imports so dependencies are correct
from . import views
from . import models
from . import api


def dummy_client(basedir):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    db = SQLAlchemy(app)

    from . import views
    from . import models
    from . import api

# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# configure sqlalchemy
# sqlite is used by default for development machines
# you can setup postgresql in the following link:
# https://wiki.archlinux.org/index.php/PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/free_spirits'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')

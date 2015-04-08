#config.py

import os

class Config (object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'fake-secret-key'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True


# Don't forget to export environment variables. At least that's how it works for now.
# e.g.
# export DATABASE_URL="postgresql://localhost/alih"
# APP_SETTINGS=config.DevelopmentConfig
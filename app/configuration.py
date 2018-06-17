# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = False
	TESTING = False
	#DATABASE_URI = 'sqlite:///application.db'
	DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
	BOOTSTRAP_FONTAWESOME = True
	SECRET_KEY = "MINHACHAVESECRETA"
	CSRF_ENABLED = True

	#Get your reCaptche key on: https://www.google.com/recaptcha/admin/create
	#RECAPTCHA_PUBLIC_KEY = "6LffFNwSAAAAAFcWVy__EnOCsNZcG2fVHFjTBvRP"
	#RECAPTCHA_PRIVATE_KEY = "6LffFNwSAAAAAO7UURCGI7qQ811SOSZlgU69rvv7"

class ProductionConfig(Config):
	DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True

"""
config.py

Author: Tim Duggan
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

Classes for providing environment configurations.
"""

# region Imports
import os
import datetime

# endregion


class Config(object):
    """
    Base class providing standard environemnt configuration variables.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "default_flask_secret"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "default_jwt_secret"
    DATABASE = os.environ.get("DATABASE_PATH") or "instance/imposter.sqlite"
    JWT_EXPIRATION_DELTA = datetime.timedelta(days=7)


class DevelopmentConfig(Config):
    """
    Development specific configuration class.
    """

    DEBUG = True


class ProductionConfig(Config):
    """
    Production specific configuration class.
    """

    DEBUG = False

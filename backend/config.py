import os
import datetime

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_flask_secret'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'default_jwt_secret'
    DATABASE = os.environ.get('DATABASE_PATH') or 'instance/imposter.sqlite'
    JWT_EXPIRATION_DELTA = datetime.timedelta(days=7)

# class DevelopmentConfig(Config):
#     DEBUG = True

# class ProductionConfig(Config):
#     DEBUG = False


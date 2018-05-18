import os

connections = {
    'postgresql': {
        'DATABASE_URI': 'postgresql://moses:password@localhost/electronics_shop',
        'TEST_DATABASE_URI': 'postgresql://moses:password@localhost/electronics_shop_test',
    },
    'sqlite': {
        'DATABASE_URI': 'sqlite:////',
        'TEST_DATABASE_URI': 'sqlite:////:memory:'
    }
}

default_connection = 'postgresql'


class Configuration:
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv('APP_SECRET')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class Development(Configuration):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = connections[default_connection]['DATABASE_URI']
    TESTING = False


class Production(Development):
    TESTING = False


class Testing(Development):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = connections[default_connection]['TEST_DATABASE_URI']


app_config = {
    "DEVELOPMENT": Development,
    "PRODUCTION": Production,
    "TESTING": Testing
}

default_config = app_config["DEVELOPMENT"]

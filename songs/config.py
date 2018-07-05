import os

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    MONGO_URI = 'mongodb://localhost:27017/testdb'
    SECRET_KEY = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV = 'dev'
    #MONGO_URI = 'mongodb://localhost:27017/devdb'
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/devdb')
    SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39f'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    ENV = 'testing'
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/testdb')
    SECRET_KEY = '792842bc-c4df-4de1-9177-d5207bd9faa6'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    ENV = 'prod'
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/proddb')
    SECRET_KEY = '8c0caeb1-6bb2-4d2d-b057-596b2dcab18e'


config = {
    "dev": "songs.config.DevelopmentConfig",
    "testing": "songs.config.StagingConfig",
    "prod": "songs.config.ProductionConfig",
    "default": "songs.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)

    print(config_name)

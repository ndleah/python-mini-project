import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-12345')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

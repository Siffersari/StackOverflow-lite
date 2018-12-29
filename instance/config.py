# Setting up app configurations

import os

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY", "default-to-key")
    DATABASE_URL = os.getenv("DATABASE_URL")


class DevConfig(Config):
    """ Inherits everything else but sets environment for devment"""
    DEBUG = True

class TestConfig(Config):
    """ Inherits also but sets debug for testing and enables testing """
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('DATABASE_TESTING_URL')

class DeployConfig(Config):
    """ For real world/ public environment setting """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevConfig,
    'testing': TestConfig,
    'deployment': DeployConfig
}
class Config(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    DB_USER = 'mqconsumer'
    DB_PASSWORD = 'catotothemoon'
    DB_HOST = '167.71.237.153'
    DB_DATABASE = 'raw_events'
    DB_PORT = '3306'

    MQ_BROKER_ADDRESS = "206.189.139.37"
    MQ_PORT = "30672"
    MQ_USER = "guest"
    MQ_PASSWORD = "guest"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

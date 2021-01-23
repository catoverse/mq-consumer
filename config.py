class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    DB_USER = 'cato_feed_app'
    DB_PASSWORD = 'Ciba$QqmRaLF2'
    DB_HOST = 'catofeedinstance.cofz0nxilsrq.ap-south-1.rds.amazonaws.com'
    DB_DATABASE = 'cato_raw_feed'
    DB_PORT = '3306'
    MQ_BROKER_ADDRESS = 'b-d30b2451-4e27-40bf-b4d8-8341beaddb72-1.mq.ap-south-1.amazonaws.com'
    MQ_PORT = '8883'
    MQ_USER = 'cato'
    MQ_PASSWORD = 'DLL7LjJFiub4NSA'
    MQ_CLIENT_NAME = 'MySQL-Writer'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

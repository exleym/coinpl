
class Config(object):
    SECRET_KEY = '<project secret key>'
    DB_HOST = 'mysql'
    DB_USERNAME = 'root'
    DB_PASSWORD = '<MYSQL_ROOT_PASSWORD from docker-compose.yml>'
    DATABASE_NAME = 'coinpl'
    DB_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        DB_USERNAME,
        DB_PASSWORD,
        DB_HOST,
        DATABASE_NAME
    )
    API_KEY = '<GDAX API Key>'
    API_SECRET = '<GDAX Secret>'
    API_PASS = '<GDAX API Passphrase>'
    DEBUG = True
    CREATE_DB = False


class ProductionConfig(Config):
    API_KEY = ''


class DevelopmentConfig(Config):
    API_KEY = ''


class TestingConfig(Config):
    API_KEY = ''
    SECRET_KEY = 'Project Secret Test Key XYZ'
    DB_URI = 'sqlite://'
    DEBUG = True
    CREATE_DB = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


config = {
    'prd': ProductionConfig,
    'dev': DevelopmentConfig,
    'test': TestingConfig
}
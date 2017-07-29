
class config(object):
    SECRET_KEY = 'GENERATE THIS LATER'
    DEBUG = True
    DB_USERNAME = 'root'
    DB_PASSWORD = 'rootpass'
    DATABASE_NAME = 'coinpl'
    DB_HOST = 'mysql'
    DB_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        DB_USERNAME,
        DB_PASSWORD,
        DB_HOST,
        DATABASE_NAME
    )
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True

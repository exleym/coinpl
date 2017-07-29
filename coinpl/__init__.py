from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from coinpl.models import Wallet
from settings import config

def create_app(**config_overrides):
    app = Flask(__name__)
    app.config.from_object(config)

    # apply overrides for tests
    app.config.update(config_overrides)

    # import blueprints
    from coinpl.blueprints.main.views import main
    from coinpl.blueprints.api_v1.views import api_v1

    # register blueprints
    app.register_blueprint(main)
    app.register_blueprint(api_v1)

    return app


def get_db(app):
    if not hasattr(g, 'dbcon'):
        g.dbcon = connect(app)
    return g.dbcon


def get_session(app):
    Session = sessionmaker(bind=get_db(app))
    return Session()


def connect(app):
    eng = create_engine(config.DB_URI)
    return eng

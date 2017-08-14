from flask import Flask, g
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from coinpl.models import Base, User, Wallet
from settings import config

def create_app(env='prd', **config_overrides):
    app = Flask(__name__)
    app.config.from_object(config[env])

    # apply overrides for tests
    app.config.update(config_overrides)

    login_manager = LoginManager()
    bootstrap = Bootstrap()
    bootstrap.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = '/auth/login'

    # import blueprints
    from coinpl.blueprints.main import main
    from coinpl.blueprints.api_v1 import api_v1
    from coinpl.blueprints.auth.views import auth

    # register blueprints
    app.register_blueprint(api_v1)
    app.register_blueprint(auth)
    app.register_blueprint(main)

    with app.app_context():
        get_db(app)

    if app.config['CREATE_DB']:
        eng = get_db(app)
        from coinpl.models import Base
        Base.metadata.create_all(bind=eng)

    @login_manager.user_loader
    def load_user(user_id):
        session = get_session(app)
        return session.query(User).filter(User.id == user_id).first()

    return app


def get_db(app):
    if not hasattr(g, 'dbcon'):
        g.dbcon = connect(app)
    return g.dbcon


def get_session(app):
    Session = sessionmaker(bind=get_db(app))
    return Session()


def connect(app):
    if os.getenv('DB_URI'):
       eng = create_engine(os.getenv('DB_URI'))
    else:
        eng = create_engine(app.config['DB_URI'])
    if app.config['CREATE_DB']:
        Base.metadata.create_all(eng)
    return eng

